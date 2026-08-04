#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#
"""Trivial foraging models used to exercise stage-4 model running and stage-5
model collation/overlay in the smoke tests.

These are deliberately simple: they produce well-formed model output of the
correct shape so that the model pipeline (stage 4) and the compare plugin's
model collation + overlay (stage 5) can be exercised end-to-end. They are not
intended to be accurate predictions of anything.
"""

# Core packages
import typing as tp

# 3rd party packages
import polars as pl
import numpy as np

# Project packages
from sierra.core.models.interface import IIntraExpModel1D, IInterExpModel1D
from sierra.core.variables import batch_criteria as bc
from sierra.core import types, exproot, batchroot


class FoodModelIntra(IIntraExpModel1D):
    """Intra-experiment model producing a 1D time series for a single
    experiment. Exists so that stage-4 model running has an intra-exp model to
    execute; its output is not collated in stage 5."""

    def __init__(self, params: types.YAMLDict) -> None:
        pass

    def run(
        self,
        criteria: bc.XVarBatchCriteria,
        exp_num: int,
        cmdopts: types.Cmdopts,
        pathset: exproot.PathSet,
    ) -> list[pl.DataFrame]:
        data = np.linspace(0, 100, num=50).reshape(50, 1)
        return [pl.DataFrame(data, schema=["model"])]

    def should_run(
        self, criteria: bc.XVarBatchCriteria, cmdopts: types.Cmdopts, exp_num: int
    ) -> bool:
        return True

    def __repr__(self) -> str:
        return "Foraging Intra Model"


class FoodModelInter(IInterExpModel1D):
    """Inter-experiment model producing one prediction per experiment in the
    batch. This is the model whose output is collated by the compare plugin
    (into ``-cc-models/`` / ``-sc-models/``) and overlaid on the comparison
    graphs. It targets the ``food-counts`` and ``swarm-energy`` measures (see
    ``config/models.yaml``), matching the ``src`` of the inter-controller and
    inter-scenario comparison graphs.

    """

    def __init__(self, params: types.YAMLDict) -> None:
        pass

    def run(
        self,
        criteria: bc.XVarBatchCriteria,
        cmdopts: types.Cmdopts,
        pathset: batchroot.PathSet,
    ) -> list[pl.DataFrame]:
        exp_dirnames = criteria.gen_exp_names()
        n = len(exp_dirnames)

        # One dataframe per target listed in models.yaml, in the same order.
        # Each has an 'Experiment ID' index column plus a single value column
        # with one row per experiment, matching what the comparator expects.
        dfs = []
        for scale in (10.0, 5.0):
            data = np.linspace(0, scale * n, num=n)
            dfs.append(
                pl.DataFrame({"Experiment ID": exp_dirnames, "col_0": data})
            )
        return dfs

    def should_run(
        self, criteria: bc.XVarBatchCriteria, cmdopts: types.Cmdopts
    ) -> bool:
        return True

    def __repr__(self) -> str:
        return "Foraging Inter Model"
