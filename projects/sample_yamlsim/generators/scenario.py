# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

# Core packages
import re
import typing as tp
import pathlib

# 3rd party packages

# Project packages
from sierra.core.experiment import definition, spec
from sierra.core import types

from plugins.yamlsim.generators import engine


def to_dict(scenario: str) -> tp.Dict[str, tp.Any]:
    count_type = scenario.split('.')[0]

    return {
        'arena_x': 0,
        'arena_y': 0,
        'arena_z': 0,
        'scenario_tag': count_type
    }


def to_generator_name(scenario: str) -> str:
    res = re.search('scenario1|scenario2', scenario)
    assert res is not None, f"Bad scenario name in {scenario}"
    scenario = res.group(0)

    mapping = {
        'scenario1': 'generate_fizzbuzz1',
        'scenario2': 'generate_fizzbuzz22'
    }
    return mapping[scenario]


def for_all_fizzbuzz(spec: spec.ExperimentSpec,
                   controller: str,
                   cmdopts: types.Cmdopts,
                   expdef_template_fpath: pathlib.Path) -> definition.BaseExpDef:
    exp_def = engine.for_all_exp(spec,
                                   controller,
                                   cmdopts,
                                   expdef_template_fpath)

    return exp_def


def generate_fizzbuzz1(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_fizzbuzz(*args, **kwargs)


def generate_fizzbuzz2(*args, **kwargs) -> definition.BaseExpDef:
    return for_all_fizzbuzz(*args, **kwargs)
