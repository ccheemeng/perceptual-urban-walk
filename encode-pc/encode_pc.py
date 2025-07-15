RADIUS = 100

import pandas as pd
import torch

import argparse
import importlib
import json
import os
from pathlib import Path

LabelledPointCloudDataset = importlib\
    .import_module("labelled-pointnet-autoencoder.datasets")\
    .LabelledPointCloudDataset
LabelledPointNetAE = importlib\
    .import_module("labelled-pointnet-autoencoder.models")\
    .LabelledPointNetAE

class EncodeDataset(LabelledPointCloudDataset):
    #override
    def __getitem__(self, idx):
        df = pd.read_csv(self.fps[idx], header=0,
                         names=['x', 'y', 'z', "label"])
        if self.max_points:
            df = df.sample(self.max_points)
        centroid = df[['x', 'y', 'z']].mean().values
        points = torch.tensor(
            (df[['x', 'y', 'z']].values - centroid) / self.radius,
            dtype=torch.float32
        )
        labels_df = df["label"].values
        labels = torch.zeros(len(df), self.c, dtype=torch.float32)
        labels[range(len(labels_df)), labels_df] = 1
        tensor = torch.cat((points, labels), dim=1)
        tensor = tensor.transpose(0, 1)
        return '.'.join(self.fps[idx].split('/')[-1].split('.')[:-1]), tensor

class EncodeAE(LabelledPointNetAE):
    #override
    def forward(self, x):
        x1, _ = self.encoder1(x)
        return x1

def main(args):
    device = args.device
    n = args.max_points
    c = args.num_classes
    dataset = EncodeDataset(args.dataset, c,
                            radius=RADIUS, max_points=n)
    loader = torch.utils.data.DataLoader(dataset, 1, shuffle=False)
    model = EncodeAE(n, c)
    model.load_state_dict(
        torch.load(args.weights,
                   weights_only=True, map_location=torch.device(device)))
    model.to(device)
    model.eval()

    Path(args.out).mkdir(parents=True, exist_ok=True)
    for batch in loader:
        name, x = batch
        out = os.path.join(args.out, f"{name[0]}.json")
        if Path(out).exists():
            continue
        print(name)
        encoding = model(x[:, :3, :].to(device))
        with open(out, 'w') as fp:
            json.dump(encoding[0].cpu().tolist(), fp)

if __name__ == "__main__":
    deviceDefault = "cuda" if torch.cuda.is_available() else "cpu"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dataset",
        required=True,
        type=str
    )
    parser.add_argument(
        "-w", "--weights",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    parser.add_argument(
        "--device",
        default=deviceDefault,
        type=str
    )
    parser.add_argument(
        "-n", "--max-points",
        default=16384,
        type=int
    )
    parser.add_argument(
        "-c", "--num-classes",
        default=19,
        type=int
    )
    args = parser.parse_args()
    main(args)