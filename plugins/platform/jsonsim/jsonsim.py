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
        description="Example JSON-driven simulator which generates random data.")
    parser.add_argument("--config", help="Configuration file for simulator.")
    args = parser.parse_args()

    config = json.load(open(args.config, 'r'))

    # Generate random data
    data = np.random.rand(int(config["exp_setup"]["n_datapoints"]), 5)
    df = pd.DataFrame(data, columns=[f"col{i}" for i in range(0, 5)])

    # Output to file. Semicolon separate is currently required by SIERRA.
    root = pathlib.Path(config['output_root'])
    subdir1 = root / "subdir1/subdir2"
    subdir2 = root / "subdir3"

    root.mkdir(parents=True, exist_ok=True)
    subdir1.mkdir(parents=True, exist_ok=True)
    subdir2.mkdir(parents=True, exist_ok=True)

    df.to_csv(root / 'output.csv', index=False, sep=',')
    df.to_csv(subdir1 / 'output.csv', index=False, sep=',')
    df.to_csv(subdir2 / 'output.csv', index=False, sep=',')


if __name__ == "__main__":
    main()
