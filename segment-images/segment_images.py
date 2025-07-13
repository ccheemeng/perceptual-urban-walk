from mmcv import imread
from mmseg.apis import inference_model, init_model, show_result_pyplot
from numpy import argmax
from torch.cuda import is_available

from argparse import ArgumentParser
from json import dump
from os import getcwd, walk
from os.path import basename, dirname, join
from pathlib import Path
from urllib.request import urlretrieve 

def main(args):
    inputDir = args.input
    outputDir = args.out
    name = args.name
    if name == None:
        name = basename(dirname(outputDir))
    segmentationDir = f"{name}-segmented"
    visualisationDir = f"{name}-segmented-visualised"
    
    if args.checkpoint:
        checkpoint = args.checkpoint
    elif Path(join(getcwd(), args.checkpoint_url.split('/')[-1])).is_file():
        checkpoint = args.checkpoint_url.split('/')[-1]
    else:
        print("downloading")
        checkpoint = urlretrieve(args.checkpoint_url,
                                 args.checkpoint_url.split('/')[-1])
    config = args.config
    device = args.device
    model = init_model(config, checkpoint, device=device)

    noViz = args.no_viz
    Path(join(outputDir, segmentationDir)).mkdir(parents=True, exist_ok=True)
    if not noViz:
        Path(join(outputDir, visualisationDir))\
            .mkdir(parents=True, exist_ok=True)

    for dirpath, dirames, filenames in walk(join(inputDir)):
        for filename in filenames:
            imageName = '.'.join(filename.split('.')[:-1])
            imagePath = join(inputDir, filename)
            segmentationPath = join(outputDir, segmentationDir,
                                    f"{imageName}.json")
            visualisationPath = join(outputDir, visualisationDir,
                                     f"{imageName}.jpg")
            if Path(segmentationPath).is_file():
                continue

            image = imread(imagePath)
            result = inference_model(model, image)
            segmentation = argmax(result.seg_logits.data.cpu(), axis=0).tolist()
            with open(segmentationPath, 'w') as fp:
                dump(segmentation, fp)
            if not noViz:
                show_result_pyplot(model, image, result,
                    show=False, out_file=visualisationPath, opacity=0.5)

if __name__ == "__main__":
    deviceDefault = "cuda" if is_available() else "cpu"
    parser = ArgumentParser()
    parser.add_argument(
        "--config", type=str, required=True
    )
    parser.add_argument(
        "--checkpoint", type=str, required=False
    )
    parser.add_argument(
        "--checkpoint-url", type=str, required=False
    )
    parser.add_argument(
        "-i", "--input", type=str, required=True
    )
    parser.add_argument(
        "-o", "--out", type=str, required=True
    )
    parser.add_argument(
        "-n", "--name", type=str, required=False
    )
    parser.add_argument(
        "--no-viz", action="store_true"
    )
    parser.add_argument(
        "-d", "--device", type=str, default=deviceDefault
    )
    args = parser.parse_args()
    main(args)