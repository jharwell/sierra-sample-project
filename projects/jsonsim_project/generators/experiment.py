# Copyright 2021 John Harwell, All rights reserved.
#
#  This file is part of SIERRA.
#
#  SIERRA is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  SIERRA is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  SIERRA.  If not, see <http://www.gnu.org/licenses/

# Core packages
import os
import pathlib

# 3rd party packages

# Project packages
from sierra.core.experiment import definition
from sierra.core import types
from jsonsim.generators import platform


def for_single_exp_run(
        exp_def: definition.BaseExpDef,
        run_num: int,
        run_output_path: pathlib.Path,
        launch_stem_path: pathlib.Path,
        random_seed: int,
        cmdopts: types.Cmdopts) -> definition.BaseExpDef:

    exp_def = platform.for_single_exp_run(exp_def,
                                          run_num,
                                          run_output_path,
                                          launch_stem_path,
                                          random_seed,
                                          cmdopts)
    return exp_def


__api__ = [
    'for_single_exp_run',
]
