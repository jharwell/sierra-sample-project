#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#
"""Example JSON-driven simulator.

Emulates a sensor / signal-processing experiment and emits data exercising the
full range of SIERRA's automatic graphs: stacked line (with spread bands +
model), heatmap, scatterplot (incl. Anscombe's quartet), and histograms
(log-normal, bimodal, Beta family).

Determinism contract: columns that are pure functions of ``clock`` (reference,
baseline), the whole Anscombe set, and the deterministic part of the 2D field
are noise-free and byte-stable across runs -- these anchor statistics
regression. All other channels are seeded PER RUN, so the set of runs is
reproducible (stats stable) while each run differs (real conf95/bw/iqr bands).
"""

# Core packages
import argparse
import json
import pathlib

# 3rd party packages
import pandas as pd
import numpy as np

# Project packages


def _run_seed(config: dict) -> int:
    """Per-run seed: runs differ (spread) but the set is reproducible."""
    for key in ("random_seed", "seed", "run_seed"):
        if key in config:
            return int(config[key])
    exp = config.get("exp_setup", {})
    for key in ("random_seed", "seed", "run_seed"):
        if key in exp:
            return int(exp[key])
    return 42


def _signal_trace(n, rng):
    """Time series: deterministic reference + noisy measurement channels."""
    clock = np.arange(n)
    t = clock / max(n - 1, 1) * 2.0 * np.pi
    reference = np.sin(t)                                      # deterministic
    baseline = np.cos(t)                                      # deterministic
    measured = reference + rng.normal(0.0, 0.25, size=n)      # noisy
    drift = reference + np.linspace(0.0, 0.8, n) + rng.normal(0.0, 0.10, size=n)
    raw = reference + rng.standard_t(df=3, size=n) * 0.20     # heavy-tailed
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


def _field_2d(rng):
    """A ripple / interference field: z = sin(sqrt(x^2+y^2)). Smooth,
    deterministic structure + light per-run jitter so inter-run stats aren't
    degenerate."""
    rows = []
    for i in range(0, 8):
        for j in range(0, 6):
            r = np.sqrt((i - 3.5) ** 2 + (j - 2.5) ** 2)
            z = np.sin(r) + rng.normal(0.0, 0.02)
            rows.append({"x": i, "y": j, "z": z})
    return pd.DataFrame(rows)


def _anscombe():
    """Anscombe's quartet: four (x,y) datasets with near-identical summary
    statistics but very different shapes. Fully deterministic (classic constants)
    -- doubles as a statistics-regression anchor. Renders as four SP- panels."""
    x_123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    x_4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
    return pd.DataFrame(
        {
            "x1": x_123,
            "y1": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
            "x2": x_123,
            "y2": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
            "x3": x_123,
            "y3": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
            "x4": x_4,
            "y4": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
        }
    )


def _dose_response(rng, n):
    """Strong linear relationship with heteroscedastic (fan-shaped) noise, so
    the SP- best-fit line is meaningful and the spread visibly grows with dose."""
    dose = np.sort(rng.uniform(0.0, 10.0, size=max(n, 60)))
    noise = rng.normal(0.0, 0.3 + 0.3 * dose)  # noise grows with dose
    response = 1.8 * dose + 2.0 + noise
    return pd.DataFrame({"dose": dose, "response": response})


def _distributions(rng, n):
    """Three histogram showcases."""
    m = max(n, 400)
    lognormal = pd.DataFrame({"samples": rng.lognormal(mean=0.0, sigma=0.6, size=m)})
    half = m // 2
    bimodal = pd.DataFrame(
        {
            "samples": np.concatenate(
                [rng.normal(-2.0, 0.5, size=half), rng.normal(2.5, 0.8, size=half)]
            )
        }
    )
    beta_family = pd.DataFrame(
        {
            "u_shaped": rng.beta(0.5, 0.5, size=m),
            "bell": rng.beta(5.0, 5.0, size=m),
            "j_shaped": rng.beta(2.0, 5.0, size=m),
            "uniform": rng.beta(1.0, 1.0, size=m),
        }
    )
    return {"lognormal": lognormal, "bimodal": bimodal, "beta-family": beta_family}


def main():
    parser = argparse.ArgumentParser(
        description="Example JSON-driven simulator which generates showcase data."
    )
    parser.add_argument("--config", help="Configuration file for simulator.")
    args = parser.parse_args()

    config = json.load(open(args.config, "r"))
    n = int(config["exp_setup"]["n_datapoints"])
    rng = np.random.RandomState(_run_seed(config))

    root = pathlib.Path(config["output_root"])
    primary = root / "sensors/primary"
    backup = root / "sensors/backup"
    for d in (root, primary, backup):
        d.mkdir(parents=True, exist_ok=True)

    trace = _signal_trace(n, rng)
    field = _field_2d(rng)
    for d in (root, primary, backup):
        trace.to_csv(d / "signal-trace.csv", index=False)
        field.to_csv(d / "field-2d.csv", index=False)

    _anscombe().to_csv(root / "anscombe.csv", index=False)
    _dose_response(rng, n).to_csv(root / "dose-response.csv", index=False)
    for name, df in _distributions(rng, n).items():
        df.to_csv(root / f"{name}.csv", index=False)


if __name__ == "__main__":
    main()
