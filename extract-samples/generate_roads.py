import argparse
import csv
import json
import math
import os
from pathlib import Path
from queue import PriorityQueue
from typing import List, Self

class Point:
    def __init__(self, coords: List[float]):
        self.coords = coords

    def getCoords(self) -> List[float]:
        return self.coords
    
    def l2Distance2To(self, other: Self) -> float:
        l2Dist2 = 0
        for i in range(min(len(self.coords), len(other.coords))):
            if self.coords[i] == None or other.coords[i] == None:
                continue
            l2Dist2 += pow(self.coords[i] - other.coords[i], 2)
        return l2Dist2

def main(args: argparse.Namespace) -> None:
    points = {}
    with open(args.coords, 'r') as fp:
        reader = csv.reader(fp)
        if args.has_header:
            next(reader)
        i = 0
        for row in reader:
            point: Point
            if args.use_z:
                point = Point([
                    float(row[args.x_idx]),
                    float(row[args.y_idx]),
                    float(row[args.z_idx])
                        if row[args.z_idx] != None and row[args.z_idx] != ''
                        else None
                ])
            else:
                point = Point([
                    float(row[args.x_idx]),
                    float(row[args.y_idx])
                ])
            id =  str(i)
            if args.use_id:
                id = row[args.id_idx]
            else:
                i += 1
            points[id] = point
    if not points:
        return
    
    maxSqDist = pow(args.max_edge_len, 2)
    edges = []
    adjacencySet = {}
    for key in points.keys():
        adjacencySet[key] = set()
    seen = set()
    heap = PriorityQueue()
    for node in points.keys():
        heap.put((0, node, node))
        break

    q1 = math.floor(0.25 * len(points))
    q2 = math.floor(0.5 * len(points))
    q3 = math.floor(0.75 * len(points))
    while len(seen) < len(points):
        if len(seen) == q1:
            print("25% complete")
        if len(seen) == q2:
            print("50% complete")
        if len(seen) == q3:
            print("75% complete")
        sqDist, curr, i = heap.get()
        if i in seen:
            continue
        seen.add(i)
        if curr != i and sqDist <= maxSqDist:
            adjacencySet[curr].add(i)
            adjacencySet[i].add(curr)
            edges.append([curr, i])
        for j in points.keys():
            if not j in seen:
                sqDist = points[i].l2Distance2To(points[j])
                heap.put((sqDist, i, j))
    print("100% complete")

    adjacencyList = {}
    for k, v in adjacencySet.items():
        adjacencyList[k] = list(v)

    name = args.name
    if name == None:
        name = os.path.basename(os.path.dirname(args.out))
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(args.out, f"{name}-points.csv"), 'w') as fp:
        writer = csv.writer(fp)
        header = ["id", 'x', 'y']
        if args.use_z:
            header.append('z')
        writer.writerow(header)
        for node, point in points.items():
            row = [node]
            row.extend(point.getCoords())
            writer.writerow(row)
    with open(os.path.join(args.out, f"{name}-adjacencies.json"), 'w') as fp:
        json.dump(adjacencyList, fp)
    with open(os.path.join(args.out, f"{name}-edges.csv"), 'w') as fp:
        writer = csv.writer(fp)
        writer.writerows(edges)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--coords",
        required=True,
        type=str
    )
    parser.add_argument(
        "--has-header",
        action="store_true"
    )
    parser.add_argument(
        "--use-id",
        action="store_true"
    )
    parser.add_argument(
        "--use-z",
        action="store_true"
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    parser.add_argument(
        "-n", "--name",
        required=False,
        type=str
    )
    parser.add_argument(
        "-i", "--id-idx",
        default=0,
        type=int
    )
    parser.add_argument(
        "-x", "--x-idx",
        default=1,
        type=int
    )
    parser.add_argument(
        "-y", "--y-idx",
        default=2,
        type=int
    )
    parser.add_argument(
        "-z", "--z-idx",
        default=3,
        type=int
    )
    parser.add_argument(
        "-l", "--max-edge-len",
        default=15.0,
        type=float
    )
    args = parser.parse_args()
    main(args)