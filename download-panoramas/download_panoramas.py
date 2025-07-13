from aiohttp import ClientSession, ClientTimeout
from geopandas import GeoDataFrame, read_file
from PIL import Image
from pyproj import Transformer
from shapely import Point
from streetlevel.streetview import find_panorama_async, get_panorama_async

from argparse import ArgumentParser
from asyncio import gather, run
from csv import writer
from math import pi, sqrt
from os import remove, walk
from os.path import basename, dirname, join
from pathlib import Path

def main(args):
    name = args.name
    if name == None:
        name = basename(dirname(args.out))
    rows = run(tasks(args))
    allPanos = set()
    ids = []
    points = []
    for row in rows:
        if row == None or row[0] in allPanos:
            continue
        allPanos.add(row[0])
        ids.append(row[0])
        if row[3]:
            points.append(Point(row[1], row[2], row[3]))
        else:
            points.append(Point(row[1], row[2]))
    panos = GeoDataFrame(data={"id": ids}, geometry=points, crs=3414)
    if args.boundary != None:
        boundary = read_file(args.boundary).to_crs(3414)
        panos = panos.clip(boundary, keep_geom_type=True)
    with open(join(args.out, f"{name}-coords.csv"), 'w') as fp:
        csvwriter = writer(fp)
        csvwriter.writerow(("id", 'x', 'y', 'z'))
        for index, row in panos.iterrows():
            point = row["geometry"]
            csvwriter.writerow((row["id"], point.x, point.y, point.z if point.has_z else None))
    inPanos = set(panos["id"])
    outPanos = allPanos.difference(inPanos)
    [remove(join(args.out, f"{name}-panos", f"{outPano}.jpg")) for outPano in outPanos]

async def tasks(args):
    if args.boundary != None:
        boundary = read_file(args.boundary).to_crs(3414)
        x1, y1, x2, y2 = boundary.total_bounds
    else:
        x1 = min(args.p1[0], args.p2[0])
        y1 = min(args.p1[1], args.p2[1])
        x2 = max(args.p1[0], args.p2[0])
        y2 = max(args.p1[1], args.p2[1])
    name = args.name
    if name == None:
        name = basename(dirname(args.out))
    radius = sqrt(2 * (args.res ** 2))
    transformerFwd = Transformer.from_crs(crs_from=3414, crs_to=4326, always_xy=True)
    transformerBack = Transformer.from_crs(crs_from=4326, crs_to=3414, always_xy=True)
    rows = []
    tasks = []
    Path(join(args.out, f"{name}-panos")).mkdir(parents=True, exist_ok=True)
    async with ClientSession(timeout=ClientTimeout(total=None), raise_for_status=True, trust_env=True) as session:
        x = x1
        while x <= x2:
            y = y1
            while y <= y2:
                lon, lat = transformerFwd.transform(x, y)
                tasks.append(getPano(lon, lat, session, radius, args.zoom, transformerBack, name))
                y += args.res
            x += args.res
        rows = await gather(*tasks)
    return rows

async def getPano(lon, lat, session, radius, zoom, transformerBack, name):
    pano = None
    try:
        pano = await find_panorama_async(lat, lon, session, radius=radius)
    except Exception as e:
        print(e)
    if pano == None or pano.heading == None:
        return
    image = None
    try:
        image = await get_panorama_async(pano, session, zoom=zoom)
    except Exception as e:
        print(e)
    if image == None:
        return
    panoX, panoY = transformerBack.transform(pano.lon, pano.lat)
    image = align_image(image, heading=pano.heading)
    image.save(join(args.out, f"{name}-panos", f"{pano.id}.jpg"))
    return (pano.id, panoX, panoY, pano.elevation)

def align_image(image, heading=0.0):
    input_image = image
    width, height = image.size
    crop_width = int(round(heading % (2 * pi) / (2 * pi) * width))
    image_right = input_image.crop((width - crop_width, 0, width, height)) # not effect-free, crops input_image too
    output_image = Image.new("RGB", (width, height))
    output_image.paste(image_right)
    output_image.paste(input_image, (crop_width, 0))
    return output_image

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--p1", type=float, nargs=2, required=False
    )
    parser.add_argument(
        "--p2", type=float, nargs=2, required=False
    )
    parser.add_argument(
        "-o", "--out", type=str, required=True
    )
    parser.add_argument(
        "-b", "--boundary", type=str, required=False
    )
    parser.add_argument(
        "-n", "--name", type=str, required=False
    )
    parser.add_argument(
        "-r", "--res", type=float, default=10.0
    )
    parser.add_argument(
        "-z", "--zoom", type=int, default=1
    )
    args = parser.parse_args()
    main(args)