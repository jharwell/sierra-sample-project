#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages
import argparse
import yaml
import pathlib

# 3rd party packages
import pandas as pd
import numpy as np

# Project packages


def main():
    parser = argparse.ArgumentParser(
        description="Example YAML-driven simulator which generates random data."
    )
    parser.add_argument("--config", help="Configuration file for simulator.")

    args = parser.parse_args()

    config = yaml.safe_load(open(args.config, "r"))

    # Generate random 1D data
    data_1D = np.random.normal(loc=0, scale=0.5, size=(int(config["exp_setup"]["n_datapoints"]), 5))

    df1D = pd.DataFrame(data_1D, columns=[f"col{i}" for i in range(0, 5)])

    # Output to file
    root = pathlib.Path(config["output_root"])
    subdir1 = root / "subdir1/subdir2"
    subdir2 = root / "subdir3"

    root.mkdir(parents=True, exist_ok=True)
    subdir1.mkdir(parents=True, exist_ok=True)
    subdir2.mkdir(parents=True, exist_ok=True)

    print(root)
    df1D.to_csv(root / "output1D.csv", index=False)
    df1D.to_csv(subdir1 / "output1D.csv", index=False)
    df1D.to_csv(subdir2 / "output1D.csv", index=False)


if __name__ == "__main__":
    main()
