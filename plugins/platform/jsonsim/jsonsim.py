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

    # Generate random data
    data = np.random.rand(4, 4)
    df = pd.DataFrame(data, columns=[f"col{i}" for i in range(1, 5)])

    config = json.load(open(args.config, 'r'))

    # Output to file. Semicolon separate is currently required by SIERRA.
    root = pathlib.Path(config['output_root'])
    root.mkdir(parents=True, exist_ok=True)
    df.to_csv(root / 'output.csv', index=False, sep=';')


if __name__ == "__main__":
    main()
