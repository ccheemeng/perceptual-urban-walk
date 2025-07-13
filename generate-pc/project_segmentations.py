OBSERVER_RADIUS = 100

import geopandas as gpd
import shapely
import trimesh

import argparse
import csv
import json
import math
import os
from pathlib import Path

def pixel_to_point(x, y, img_width, img_height, length,
                   x_range=(-1.0, 1.0), y_range=(-1.0, 1.0), heading=0.0):
    pi = math.pi
    sin = math.sin
    cos = math.cos
    
    x0 = x_range[0]
    dx = x_range[1] - x0
    y0 = y_range[0]
    dy = y_range[1] - y0
    
    x_norm = ((x + 0.5) / img_width) * dx + x0
    y_norm = ((y + 0.5) / img_height) * dy + y0
    theta = -1.0 * pi * x_norm
    phi = -1.0 * pi / 2 * y_norm
    point = [
        -1.0 * length * sin(theta - heading) * cos(phi),
        length * cos(theta - heading) * cos(phi),
        length * sin(phi)
    ]
    
    return point

def geometryToPolygons(geometry: shapely.Geometry) -> list[shapely.Polygon]:
    if isinstance(geometry, shapely.Polygon):
        return [geometry]
    if isinstance(geometry, shapely.MultiPolygon):
        return list(geometry.geoms)
    if isinstance(geometry, shapely.GeometryCollection):
        newPolygons: list[shapely.Polygon] = list()
        for geom in geometry.geoms:
            newPolygons.extend(geometryToPolygons(geom))
        return newPolygons
    return list()

def main(args):
    points = {}
    with open(args.points, 'r') as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            points[row[0]] = shapely.Point([float(x) for x in row[1:3]])
    
    with open(args.buildings, 'r') as fp:
        buildingsGdf = gpd.read_file(fp).to_crs(3414)
    buildingGeoms = buildingsGdf["geometry"].values
    buildings = []
    for buildingGeom in buildingGeoms:
        buildings.extend(geometryToPolygons(buildingGeom))
    buildingMesh = trimesh.util.concatenate(filter(lambda m: m.is_volume,
        [trimesh.primitives.Extrusion(building, height=OBSERVER_RADIUS)
         for building in buildings]))
    rayMesh = trimesh.ray.ray_pyembree.RayMeshIntersector(buildingMesh)

    def projectSegmentation(id, point: shapely.Point, distance=OBSERVER_RADIUS):
        panoPc = []
        with open(os.path.join(args.segmentations, f"{id}.json"), 'r') as fp:
            segmentation = json.load(fp)
        img_height = len(segmentation)
        img_width = len(segmentation[0])
        ray_origins = []
        ray_directions = []
        labels = []
        for i in range(img_height):
            for j in range(img_width):
                label = segmentation[i][j]
                if args.filter_labels != None\
                    and (len(args.filter_labels) > 0\
                         and label in args.filter_labels):
                    continue
                ray_origins.append([point.x, point.y, 0])
                ray_directions.append(pixel_to_point(j, i,
                                                     img_width, img_height, 1))
                labels.append(label)
        if len(ray_origins) <= 0:
            return panoPc
        intersections = rayMesh.intersects_location(ray_origins, ray_directions,
                                                    multiple_hits=False)
        for i in range(len(intersections[1])):
            distance = shapely.distance(shapely.Point(point.x, point.y, 0),
                                        shapely.Point(intersections[0][i]))
            if distance > OBSERVER_RADIUS:
                continue
            label = labels[intersections[1][i]]
            intersection = intersections[0][i].tolist() + [label]
            panoPc.append(intersection)
        return panoPc

    def writeIntersections(id, point, fp):
        if Path(os.path.join(fp, f"{id}.csv")).exists():
            return
        print(f"processing {id}")
        panoPc = projectSegmentation(id, point)
        print(f"writing {id}")
        with open(os.path.join(fp, f"{id}.csv"), 'w') as afp:
            writer = csv.writer(afp)
            writer.writerows(panoPc)

    Path(args.out).mkdir(parents=True, exist_ok=True)
    k = 1
    for id, point in points.items():
        print(k, id, point)
        k += 1
        writeIntersections(id, point, args.out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--points",
        required=True,
        type=str
    )
    parser.add_argument(
        "-s", "--segmentations",
        required=True,
        type=str
    )
    parser.add_argument(
        "-b", "--buildings",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    parser.add_argument(
        "-f", "--filter-labels",
        nargs='*',
        required=False,
        type=int
    )
    args = parser.parse_args()
    main(args)