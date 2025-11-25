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
import networkx as nx

# Project packages


def main():
    parser = argparse.ArgumentParser(
        description="Example YAML-driven simulator which generates random data."
    )
    parser.add_argument("--config", help="Configuration file for simulator.")

    args = parser.parse_args()

    config = yaml.safe_load(open(args.config, "r"))

    # Generate random 1D data
    data_1D = np.random.normal(loc=0, scale=0.5, size=(50, 5))

    df1D = pd.DataFrame(data_1D, columns=[f"col{i}" for i in range(0, 5)])

    # Output to file
    root = pathlib.Path(config["output_root"])
    subdir1 = root / "subdir1/subdir2"
    subdir2 = root / "subdir3"

    root.mkdir(parents=True, exist_ok=True)
    subdir1.mkdir(parents=True, exist_ok=True)
    subdir2.mkdir(parents=True, exist_ok=True)

    df1D.to_csv(root / "output1D.csv", index=False)
    df1D.to_csv(subdir1 / "output1D.csv", index=False)
    df1D.to_csv(subdir2 / "output1D.csv", index=False)

    # Create directory for output files if it doesn't exist
    graph_dir = root / 'erdos_renyi'
    graph_dir.mkdir(exist_ok=True)

    # Parameters
    start_nodes = 5  # Starting number of nodes
    num_graphs = 10  # Number of graphs to generate
    edge_probability = 0.3  # Probability of edge creation in random graph

    # Generate graphs
    for i in range(num_graphs):
        num_nodes = start_nodes + i

        # Generate a random graph (Erdős-Rényi model)
        #
        # Other generator options:
        # G = nx.barabasi_albert_graph(num_nodes, 2)  # Scale-free network
        # G = nx.watts_strogatz_graph(num_nodes, 4, 0.3)  # Small-world network
        G = nx.erdos_renyi_graph(num_nodes, edge_probability)

        # Add some metadata to the graph
        G.graph['num_nodes'] = num_nodes
        G.graph['num_edges'] = G.number_of_edges()
        G.graph['graph_id'] = i

        # Add node attributes (optional)
        for node in G.nodes():
            G.nodes[node]['degree'] = G.degree(node)

        # Write to GraphML file with numeric name
        filename = f'{graph_dir}/erdos_renyi_{i:03d}.graphml'
        nx.write_graphml(G, filename)


if __name__ == "__main__":
    main()
