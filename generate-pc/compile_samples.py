import geopandas as gpd
import shapely

import argparse
import json
import os

def main(args):
    ids = []
    points = []
    regions = []
    for root, dirs, files in os.walk(args.sample_pc):
        for file in files:
            id = '.'.join(file.split('.')[:-1])
            ids.append(id)
            points.append(shapely.Point([float(x) for x in id.split('_')[:2]]))
            with open(os.path.join(args.regions, f"{id}.geojson"), 'r') as fp:
                regions.append(shapely.from_geojson(json.load(fp)))
        break

    name = args.name
    if name == None:
        name = os.path.basename(os.path.dirname(args.out))
    points_gdf = gpd.GeoDataFrame(index=ids, geometry=points, crs=3414)
    regions_gdf = gpd.GeoDataFrame(index=ids, geometry=regions, crs=3414)
    with open(os.path.join(args.out, f"{name}-points.geojson"), 'w') as fp:
        json.dump(points_gdf.to_geo_dict(), fp)
    with open(os.path.join(args.out, f"{name}-regions.geojson"), 'w') as fp:
        json.dump(regions_gdf.to_geo_dict(), fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--sample-pc",
        required=True,
        type=str
    )
    parser.add_argument(
        "-r", "--regions",
        required=True,
        type=str
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