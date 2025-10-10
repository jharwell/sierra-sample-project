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

# 3rd party packages
from sierra.core.experiment import definition
from sierra.plugins.engine.ros1robot.generators import engine

# Project packages


def to_dict(scenario: str) -> tp.Dict[str, tp.Any]:
    x, y, z = scenario.split('+')[0].split('.')[1].split('x')
    count_type = scenario.split('.')[0]

    return {
        'arena_x': int(x),
        'arena_y': int(y),
        'arena_z': int(z),
        'scenario_tag': count_type
    }


def outdoorworld_all_exp(*args, **kwargs) -> definition.BaseExpDef:
    return engine.for_all_exp(*args, **kwargs)


def to_generator_name(scenario_name: str) -> str:
    res = re.search('OutdoorWorld', scenario_name)
    assert res is not None, f"Bad scenario name in {scenario_name}"
    scenario = res.group(0)

    mapping = {
        'OutdoorWorld': 'outdoorworld_all_exp'
    }
    return mapping[scenario]
