import joblib
import pandas as pd

import argparse
import json
import os
from pathlib import Path

def main(args):
    with open(args.scaler, "rb") as fp:
        scaler = joblib.load(fp)
    with open(args.pca, "rb") as fp:
        pca = joblib.load(fp)
    with open(args.kmeans, "rb") as fp:
        kmeans = joblib.load(fp)

    encodings = {}
    for root, dirs, files in os.walk(args.encodings):
        for file in files:
            with open(os.path.join(args.encodings, file), 'r') as fp:
                encodings[
                    '_'.join('.'.join(file.split('.')[:-1]).split('_')[:2])
                ] = json.load(fp)
        break
    encodings_df = pd.DataFrame.from_dict(encodings, orient="index")
    cluster_df = encodings_df.iloc[:,0:0]

    X = encodings_df.values
    X = scaler.transform(X)
    X = pca.transform(X)
    clusters = kmeans.predict(X)
    cluster_df["cluster"] = clusters
    Path(os.path.dirname(args.out)).mkdir(parents=True, exist_ok=True)
    cluster_df.to_csv(args.out, columns=["cluster"], index=True, index_label="id")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--scaler",
        required=True,
        type=str
    )
    parser.add_argument(
        "-p", "--pca",
        required=True,
        type=str
    )
    parser.add_argument(
        "-k", "--kmeans",
        required=True,
        type=str
    )
    parser.add_argument(
        "-e", "--encodings",
        required=True,
        type=str
    )
    parser.add_argument(
        "-o", "--out",
        required=True,
        type=str
    )
    args = parser.parse_args()
    main(args)