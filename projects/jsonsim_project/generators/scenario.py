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
import re
import typing as tp
import pathlib

# 3rd party packages

# Project packages
from sierra.core.experiment import definition, spec
from sierra.core import types

from jsonsim.generators import platform


def to_dict(scenario: str) -> tp.Dict[str, tp.Any]:
    x, y, z = scenario.split('+')[0].split('.')[1].split('x')
    count_type = scenario.split('.')[0]

    return {
        'arena_x': int(x),
        'arena_y': int(y),
        'arena_z': int(z),
        'scenario_tag': count_type
    }


def to_generator_name(scenario: str) -> str:
    res = re.search('scenario1|scenario2', scenario)
    assert res is not None, f"Bad scenario name in {scenario}"
    scenario = res.group(0)

    mapping = {
        'scenario1': 'generate_pewpew1',
        'scenario2': 'generate_pewpew2'
    }
    return mapping[scenario]


def for_all_pewpew(spec: spec.ExperimentSpec,
                   controller: str,
                   cmdopts: types.Cmdopts,
                   expdef_template_fpath: pathlib.Path) -> definition.BaseExpDef:
    exp_def = platform.for_all_exp(spec,
                                   controller,
                                   cmdopts,
                                   expdef_template_fpath)

    return exp_def


def generate_pewpew1(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_pewpew(*args, **kwargs)


def generate_pewpew2(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_pewpew(*args, **kwargs)
