# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

# Core packages
import pathlib

# 3rd party packages

# Project packages
from sierra.core.experiment import definition
from sierra.core import types
from plugins.yamlsim.generators import engine

def for_single_exp_run(
        exp_def: definition.BaseExpDef,
        run_num: int,
        run_output_path: pathlib.Path,
        launch_stem_path: pathlib.Path,
        random_seed: int,
        cmdopts: types.Cmdopts) -> definition.BaseExpDef:

    exp_def = engine.for_single_exp_run(exp_def,
                                          run_num,
                                          run_output_path,
                                          launch_stem_path,
                                          random_seed,
                                          cmdopts)
    return exp_def


__api__ = [
    'for_single_exp_run',
]
