#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#
"""Example YAML-driven simulator.

Emulates a structured/categorical experiment. Emits:
  * signal-trace.csv (root + nested sensor dir): deterministic reference signal
    + noisy channels, for stacked_line + histogram graphs and collation.
  * classification.csv: a story-telling confusion matrix (CM- graph).
  * networks/*.graphml: a family of scale-free graphs plotted via the imagize
    section (NW- graphs), one per generated topology.

Determinism contract: signal-trace 'reference' and 'baseline' are pure functions
of 'clock' (regression anchors); everything else is seeded per run so the set of
runs is reproducible while each run differs (real conf95/bw/iqr spread bands).
"""

# Core packages
import argparse
import yaml
import pathlib

# 3rd party packages
import pandas as pd
import numpy as np
import networkx as nx

# Project packages


def _run_seed(config: dict) -> int:
    for key in ("random_seed", "seed", "run_seed"):
        if key in config:
            return int(config[key])
    return 7


def _signal_trace(n, rng):
    clock = np.arange(n)
    t = clock / max(n - 1, 1) * 2.0 * np.pi
    reference = np.sin(t)  # deterministic
    baseline = np.cos(t)  # deterministic
    measured = reference + rng.normal(0.0, 0.25, size=n)
    drift = reference + np.linspace(0.0, 0.8, n) + rng.normal(0.0, 0.10, size=n)
    raw = reference + rng.standard_t(df=3, size=n) * 0.20
    return pd.DataFrame(
        {
            "clock": clock,
            "reference": reference,
            "measured": measured,
            "drift": drift,
            "baseline": baseline,
            "raw": raw,
        }
    )


def _classification(rng):
    """Diagonal-dominant confusion matrix with SYSTEMATIC off-diagonal
    confusions (0<->1, 3<->8), so the CM- heatmap tells a story."""
    classes = [i for i in range(10)]
    confused = {0: 1, 1: 0, 3: 8, 8: 3}
    rows = []
    for ai, actual in enumerate(classes):
        for pi, predicted in enumerate(classes):
            if ai == pi:
                count = int(rng.randint(70, 95))
            elif confused.get(ai) == pi:
                count = int(rng.randint(20, 35))
            else:
                count = int(rng.randint(1, 6))
            for _ in range(count):
                rows.append({"Actual_Class": actual, "Predicted_Class": predicted})
    df = pd.DataFrame(rows)
    df["Index"] = range(len(df))
    return df.set_index("Index")


def _networks(seed, count=5):
    """A family of scale-free (Barabasi-Albert) graphs of growing size, written
    into a directory the imagize section iterates. Each carries node/edge
    attributes the NW- generator maps to size/color/width. Scale-free (rather
    than the old Erdos-Renyi) gives clear hubs + a long tail, which the layout
    algorithms render attractively."""
    graphs = []
    for i in range(count):
        n_nodes = 15 + i * 8
        G = nx.barabasi_albert_graph(n_nodes, 2, seed=seed + i)
        G.graph["name"] = f"scale-free-{i:02d}"
        for node in G.nodes():
            deg = G.degree[node]
            G.nodes[node]["degree"] = deg
            G.nodes[node]["group"] = deg % 4
        for u, v in G.edges():
            G.edges[u, v]["weight"] = float(G.degree[u] * G.degree[v])
        graphs.append(G)
    return graphs


def _tsne(rng, n_per_class=40):
    """High-dimensional points with latent cluster structure, for the t-SNE
    (SP-) graph. Several well-separated classes live in an 8-D feature space;
    each class is a gaussian blob around a distinct centroid with a little
    overlap, so the embedding recovers clean-but-not-trivial clusters (the
    classic t-SNE showcase). Seeded per run, so runs differ while the set is
    reproducible."""
    cols = [
        "throughput",
        "latency",
        "energy",
        "path_eff",
        "collisions",
        "coverage",
        "convergence",
        "load_balance",
    ]
    # one centroid per class in the 8-D feature space
    centroids = {
        "greedy": [85, 120, 4.2, 0.55, 8.5, 72, 40, 0.45],
        "stigmergy": [62, 210, 2.1, 0.82, 1.2, 91, 130, 0.88],
        "flocking": [74, 160, 3.0, 0.71, 3.4, 85, 75, 0.79],
        "auction": [90, 95, 5.6, 0.63, 6.1, 78, 55, 0.61],
        "random": [30, 340, 6.8, 0.31, 9.9, 48, 200, 0.22],
    }
    spread = np.array([9, 28, 0.7, 0.06, 1.3, 6, 22, 0.08])

    frames = []
    for label, mu in centroids.items():
        pts = rng.normal(
            np.asarray(mu, dtype=float), spread, size=(n_per_class, len(cols))
        )
        pts[:, 3] = np.clip(pts[:, 3], 0.0, 1.0)  # path_eff
        pts[:, 5] = np.clip(pts[:, 5], 0.0, 100.0)  # coverage
        pts[:, 7] = np.clip(pts[:, 7], 0.0, 1.0)  # load_balance
        pts = np.maximum(pts, 0.0)
        sub = pd.DataFrame(pts, columns=cols)
        sub["controller"] = label
        frames.append(sub)

    df = pd.concat(frames, ignore_index=True)
    df = df.round(3)
    df["Index"] = range(len(df))
    return df.set_index("Index")


def main():
    parser = argparse.ArgumentParser(
        description="Example YAML-driven simulator which generates showcase data."
    )
    parser.add_argument("--config", help="Configuration file for simulator.")
    args = parser.parse_args()

    config = yaml.safe_load(open(args.config, "r"))
    rng = np.random.RandomState(_run_seed(config))
    n = 50

    root = pathlib.Path(config["output_root"])
    nested = root / "sensors/primary"
    for d in (root, nested):
        d.mkdir(parents=True, exist_ok=True)

    # signal-trace at root + one nested sensor dir (nested one is what collation
    # lifts for its multi-source join).
    trace = _signal_trace(n, rng)
    trace.to_csv(root / "signal-trace.csv", index=False)
    trace.to_csv(nested / "signal-trace.csv", index=False)

    _classification(rng).to_csv(root / "classification.csv")
    _tsne(rng).to_csv(root / "alg-behavior.csv")

    # Directory of graphs for the imagize network plots.
    netdir = root / "networks"
    netdir.mkdir(exist_ok=True)
    for i, G in enumerate(_networks(_run_seed(config))):
        nx.write_graphml(G, f"{netdir}/network_{i:03d}.graphml")


if __name__ == "__main__":
    main()
