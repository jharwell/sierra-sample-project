#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages
import argparse
import json
import pathlib

# 3rd party packages
import pandas as pd
import numpy as np

# Project packages


def main():
    parser = argparse.ArgumentParser(
        description="Example JSON-driven simulator which generates random data."
    )
    parser.add_argument("--config", help="Configuration file for simulator.")
    parser.add_argument("--distribution", help="Distribution of generated data.")

    args = parser.parse_args()

    config = json.load(open(args.config, "r"))

    # Generate random 1D data
    if args.distribution == "gaussian":
        data_1D = np.random.normal(
            loc=0, scale=0.5, size=(int(config["exp_setup"]["n_datapoints"]), 5)
        )
    elif args.distribution == "binomial":
        data_1D = np.random.binomial(
            n=int(config["exp_setup"]["n_datapoints"]) * 5,
            p=0.3,
            size=(int(config["exp_setup"]["n_datapoints"]), 5),
        )

    df1D = pd.DataFrame(data_1D, columns=[f"col{i}" for i in range(0, 5)])

    data2D = []
    for i in range(0, 8):
        for j in range(0, 6):
            data2D.append(
                {
                    "x": i,
                    "y": j,
                    "z": np.random.rand(1)[0],
                }
            )

    df2D = pd.DataFrame(data2D)

    # Output to file. Semicolon separate is currently required by SIERRA.
    root = pathlib.Path(config["output_root"])
    subdir1 = root / "subdir1/subdir2"
    subdir2 = root / "subdir3"

    root.mkdir(parents=True, exist_ok=True)
    subdir1.mkdir(parents=True, exist_ok=True)
    subdir2.mkdir(parents=True, exist_ok=True)

    df1D.to_csv(root / "output1D.csv", index=False)
    df1D.to_csv(subdir1 / "output1D.csv", index=False)
    df1D.to_csv(subdir2 / "output1D.csv", index=False)
    df2D.to_csv(root / "output2D.csv", index=False)
    df2D.to_csv(subdir1 / "output2D.csv", index=False)
    df2D.to_csv(subdir2 / "output2D.csv", index=False)


if __name__ == "__main__":
    main()
