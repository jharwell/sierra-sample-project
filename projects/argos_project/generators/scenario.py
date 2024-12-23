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
from sierra.plugins.platform.argos.variables import arena_shape
from sierra.plugins.platform.argos.generators import platform


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
    res = re.search('LowBlockCount|HighBlockCount', scenario)
    assert res is not None, f"Bad scenario name in {scenario}"
    scenario = res.group(0)

    mapping = {
        'LowBlockCount': 'low_block_count_foraging',
        'HighBlockCount': 'high_block_count_foraging'
    }
    return mapping[scenario]


def for_all_foraging_exp(spec: spec.ExperimentSpec,
                         controller: str,
                         cmdopts: types.Cmdopts,
                         expdef_template_fpath: pathlib.Path) -> definition.BaseExpDef:
    exp_def = platform.for_all_exp(spec,
                                   controller,
                                   cmdopts,
                                   expdef_template_fpath)

    # Generate physics engine definitions.
    platform.generate_physics(exp_def,
                              spec,
                              cmdopts,
                              cmdopts['physics_engine_type2D'],
                              cmdopts['physics_n_engines'],
                              [spec.arena_dim])

    # Generate arena shap definitions
    arena = arena_shape.ArenaShape([spec.arena_dim])
    platform.generate_arena_shape(exp_def, spec, arena)
    return exp_def

# High/low block count scenarios are actually the same in this simple project;
# checking it here and using it to choose which generator to use is shown as an
# example of what can be done.


def low_block_count_foraging(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_foraging_exp(*args, **kwargs)


def high_block_count_foraging(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_foraging_exp(*args, **kwargs)
