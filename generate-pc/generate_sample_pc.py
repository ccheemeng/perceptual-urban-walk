import geopandas as gpd
import more_itertools
import pandas as pd
import shapely
from tqdm import tqdm

import argparse
import csv
import gc
import json
import math
import os
from pathlib import Path

def main(args):
    Path(args.out).mkdir(parents=True, exist_ok=True)
    total_samples = 0
    for root, dirs, files in os.walk(args.points):
        total_samples = len(files)
        batches = more_itertools.ichunked(files, args.batch_size)
        break

    points_gdf = gpd.GeoDataFrame(columns=["segmented-pc", "label", "geometry"], crs=3414)
    batch_num = 1
    total_batches = math.ceil(total_samples / args.batch_size)
    segmented_pcs = set()
    for batch in tqdm(batches):
        print(f""""
================ 
Batch {batch_num} of {total_batches} 
================\n
              """)
        sample_points = []
        sample_regions = {}
        prev_segmented_pcs = segmented_pcs
        segmented_pcs = set()
        for file in batch:
            x, y = map(lambda c: float(c), '.'.join(file.split('.')[:-1]).split('_'))
            if Path(os.path.join(args.out, f"{x}_{y}.csv")).exists():
                continue
            sample_points.append((x, y))
            with open(os.path.join(args.points, file), 'r') as fp:
                reader = csv.reader(fp)
                next(reader)
                for row in reader:
                    segmented_pcs.add(row[0])
            with open(os.path.join(args.regions, f"{x}_{y}.geojson"), 'r') as fp:
                sample_regions[(x, y)] = shapely.from_geojson(json.load(fp))
        num_points = len(points_gdf)
        points_gdf = points_gdf.loc[points_gdf["segmented-pc"].isin(segmented_pcs)]
        gc.collect()
        print(f"""
Rebuilding combined point cloud from 
{len(prev_segmented_pcs)} to {len(segmented_pcs)} 
individual point clouds\n
{len(points_gdf["segmented-pc"].unique())} of 
{len(prev_segmented_pcs)} point clouds retained\n
{len(points_gdf)} of {num_points} points retained\n
              """)
        
        points = []
        data = []
        for segmented_pc in tqdm(segmented_pcs):
            if segmented_pc in prev_segmented_pcs:
                continue
            with open(os.path.join(args.segmentations, f"{segmented_pc}.csv"), 'r') as fp:
                reader = csv.reader(fp)
                for row in reader:
                    label = row[3]
                    point = shapely.Point(row[0], row[1], row[2])
                    points.append(point)
                    data.append([segmented_pc, label])
        
        points_gdf = pd.concat((
            points_gdf,
            gpd.GeoDataFrame(data=data, geometry=points,
                             crs=3414, columns=["segmented-pc", "label"])
        ))
        points_gdf = points_gdf.reset_index(drop=True)
        gc.collect()

        print(points_gdf.head())
        print("Creating STRTree\n")
        points_gdf.sindex
        print("Querying point cloud\n")
        for xy, region in tqdm(sample_regions.items()):
            query = points_gdf.sindex.query(region, predicate="intersects")
            # pd.isin converts iterable to hash table
            within_gdf = points_gdf.loc[points_gdf.index.isin(query)]
            if not args.no_sample:
                n = args.sample_size
                if not args.write_small and n > len(within_gdf):
                    continue
                if n > len(within_gdf):
                    n = len(within_gdf)
                within_gdf = within_gdf.sample(n=n, replace=False, random_state=0)
            sample_points = []
            for index, row in within_gdf.iterrows():
                point = row["geometry"]
                label = row["label"]
                sample_points.append([point.x, point.y, point.z, label])
            with open(os.path.join(args.out, f"{xy[0]}_{xy[1]}.csv"), 'w') as fp:
                writer = csv.writer(fp)
                writer.writerows(sample_points)
        batch_num += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--points",
        required=True,
        type=str
    )
    parser.add_argument(
        "-r", "--regions",
        required=True,
        type=str
    )
    parser.add_argument(
        "-s", "--segmentations",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    parser.add_argument(
        "-b", "--batch-size",
        default=500,
        type=int
    )
    parser.add_argument(
        "--sample-size",
        default=65536,
        type=int
    )
    parser.add_argument(
        "--write-small",
        action="store_true"
    )
    parser.add_argument(
        "--no-sample",
        action="store_true"
    )
    args = parser.parse_args()
    main(args)