OBSERVER_RADIUS = 100
STREET_WIDTH = 80
TOLERANCE = 1E-15

import geopandas as gpd
import networkx as nx
import shapely

import argparse
import csv
import json
import math
import os
from pathlib import Path
from typing import List

def graphInPolygon(G: nx.Graph, polygon: shapely.Polygon) -> nx.Graph:
    GNew = nx.Graph()
    for n1, n2 in G.edges():
        p1 = G.nodes[n1]["point"]
        p2 = G.nodes[n2]["point"]
        line = shapely.LineString([p1, p2])
        intersection = line.intersection(polygon)
        intersections = []
        if intersection.geom_type == "LineString":
            intersections = [intersection]
        elif intersection.geom_type == "MultiLineString":
            intersections = intersection.lines
        elif intersection.geom_type == "GeometryCollection":
            intersections = filter(lambda x: x.geom_type == "LineString",
                                   intersection.geoms)
        else:
            continue
        i = 0
        for linestring in intersections:
            nodes = []
            for coordinate in linestring.coords:
                point = shapely.Point(coordinate)
                if point.equals_exact(p1, TOLERANCE):
                    nodes.append(n1)
                    GNew.add_node(n1, point=p1)
                elif point.equals_exact(p2, TOLERANCE):
                    nodes.append(n2)
                    GNew.add_node(n2, point=p2)
                else:
                    nodes.append(f"{n1}-{n2}-{i}")
                    GNew.add_node(f"{n1}-{n2}-{i}", point=point)
                i += 1
            for j in range(len(nodes[:-1])):
                if nodes[j] in G.nodes and nodes[j + 1] in G.nodes:
                    length = G[nodes[j]][nodes[j + 1]]["weight"]
                else:
                    length = GNew.nodes[nodes[j]]["point"]\
                        .distance(GNew.nodes[nodes[j + 1]]["point"])
                GNew.add_edge(nodes[j], nodes[j + 1], weight=length)
    return GNew

def main(args):
    name = args.name
    if name == None:
        name = os.path.basename(os.path.dirname(args.out))
    
    points = {}
    with open(args.points, 'r') as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            points[str(row[0])] = shapely.Point([float(x) for x in row[1:3]])
    
    with open(args.adjacencies, 'r') as fp:
        adjacencyList = json.load(fp)

    with open(args.boundary, 'r') as fp:
        boundary = gpd.read_file(fp)
    boundaryOffset = boundary.iloc[0]["geometry"].buffer(-1 * OBSERVER_RADIUS)

    G = nx.from_dict_of_lists(adjacencyList)
    for node, point in points.items():
        G.nodes[node]["point"] = point
    for n1, n2 in G.edges():
        length = G.nodes[n1]["point"].distance(G.nodes[n2]["point"])
        G[n1][n2]["weight"] = length

    GOffset = graphInPolygon(G, boundaryOffset)

    pointsDir = os.path.join(args.out, f"{name}-sample-points")
    regionsDir = os.path.join(args.out, f"{name}-sample-regions")
    Path(pointsDir).mkdir(parents=True, exist_ok=True)
    Path(regionsDir).mkdir(parents=True, exist_ok=True)

    numQueries = args.num_queries
    totalLength = GOffset.size(weight="weight")
    for n1, n2 in GOffset.edges():
        length = GOffset[n1][n2]["weight"]
        n = math.ceil((length / totalLength) * numQueries)
        p1 = GOffset.nodes[n1]["point"]
        p2 = GOffset.nodes[n2]["point"]
        dx = (p2.x - p1.x) / n
        dy = (p2.y - p2.y) / n
        for i in range(n):
            x = dx * (i + 0.5) + p1.x
            y = dy * (i + 0.5) + p1.y
            queryPoint = shapely.Point([x, y])
            queryRadius = queryPoint.buffer(OBSERVER_RADIUS)
            GCircle = graphInPolygon(G, queryRadius)
            nearest = None
            distance = math.inf
            for node in GCircle.nodes():
                currDistance = queryPoint.distance(GCircle.nodes[node]["point"])
                if currDistance < distance:
                    nearest = node
                    distance = currDistance
            GQuery = GCircle\
                .subgraph(nx.node_connected_component(GCircle, nearest))\
                .copy()
            linestrings = []
            for o1, o2 in GQuery.edges():
                q1 = GQuery.nodes[o1]["point"]
                q2 = GQuery.nodes[o2]["point"]
                linestrings.append(shapely.LineString([q1, q2]))
            multilinestring = shapely.MultiLineString(linestrings)
            streetBuffer = multilinestring.buffer(STREET_WIDTH / 2)
            queryRegion = streetBuffer.intersection(queryRadius)
            ids = []
            for id, point in points.items():
                if point.within(queryPoint.buffer(2 * OBSERVER_RADIUS)):
                    ids.append([id, point.x, point.y,
                                point.z if point.has_z else None])
            with open(os.path.join(pointsDir, f"{x}_{y}.csv"), 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(["id", 'x', 'y', 'z'])
                writer.writerows(ids)
            with open(os.path.join(regionsDir, f"{x}_{y}.geojson"), 'w') as fp:
                json.dump(shapely.to_geojson(queryRegion), fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--adjacencies",
        required=True,
        type=str
    )
    parser.add_argument(
        "-p", "--points",
        required=True,
        type=str
    )
    parser.add_argument(
        "-b", "--boundary",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    parser.add_argument(
        "--name",
        required=False,
        type=str
    )
    parser.add_argument(
        "-n", "--num-queries",
        default=1024,
        type=int
    )
    args = parser.parse_args()
    main(args)