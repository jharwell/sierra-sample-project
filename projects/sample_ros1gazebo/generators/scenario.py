# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

# Core packages
import re
import typing as tp

# 3rd party packages
from sierra.core.experiment import definition
from sierra.plugins.engine.ros1gazebo.generators import engine

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


def houseworld_all_exp(*args, **kwargs) -> definition.BaseExpDef:
    return engine.for_all_exp(*args, **kwargs)


def to_generator_name(scenario: str) -> str:
    res = re.search('HouseWorld', scenario)
    assert res is not None, f"Bad scenario name in {scenario}"
    scenario = res.group(0)

    mapping = {
        'HouseWorld': 'houseworld_all_exp'
    }
    return mapping[scenario]
