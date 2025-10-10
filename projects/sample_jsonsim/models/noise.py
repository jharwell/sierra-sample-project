#
# Copyright 2025 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages
import typing as tp

# 3rd party packages
import implements
import pandas as pd
import numpy as np

# Project packages
from sierra.core.models.interface import IIntraExpModel1D, IInterExpModel1D
from sierra.core.variables import batch_criteria as bc
from sierra.core import types, exproot, batchroot


@implements.implements(IIntraExpModel1D)
class NoisyModel:
    def __init__(self, params: types.YAMLDict) -> None:
        pass

    def run(
        self,
        criteria: bc.XVarBatchCriteria,
        exp_num: int,
        cmdopts: types.Cmdopts,
        pathset: exproot.PathSet,
    ) -> tp.List[pd.DataFrame]:
        data = np.random.normal(loc=0, scale=1, size=(50, 1)) * 80
        return [pd.DataFrame(data, columns=["model"])]

    def should_run(
        self, criteria: bc.XVarBatchCriteria, cmdopts: types.Cmdopts, exp_num: int
    ) -> bool:
        return True

    def __repr__(self) -> str:
        return "Noisy Model"


@implements.implements(IInterExpModel1D)
class LessNoisyModel:
    def __init__(self, params: types.YAMLDict) -> None:
        pass

    def run(
        self,
        criteria: bc.XVarBatchCriteria,
        cmdopts: types.Cmdopts,
        pathset: batchroot.PathSet,
    ) -> tp.List[pd.DataFrame]:
        exp_dirnames = criteria.gen_exp_names()
        data = np.random.normal(loc=0, scale=0.01, size=(len(exp_dirnames))) * 80

        df = pd.DataFrame(data, index=exp_dirnames)
        df.index.name = "Experiment ID"
        return [df]

    def should_run(
        self, criteria: bc.XVarBatchCriteria, cmdopts: types.Cmdopts
    ) -> bool:
        return True

    def __repr__(self) -> str:
        return "Less Noisy Model"
