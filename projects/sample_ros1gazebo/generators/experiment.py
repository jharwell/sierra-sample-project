# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

# Core packages

# 3rd party packages

# Project packages
from sierra.plugins.engine.ros1gazebo.generators import engine
from sierra.core.experiment import definition


def for_single_exp_run(*args, **kwargs) -> definition.BaseExpDef:
    return engine.for_single_exp_run(*args, **kwargs)


def for_all_exp(*args, **kwargs) -> definition.BaseExpDef:
    return engine.for_all_exp(*args, **kwargs)


__api__ = [
    'for_single_exp_run',
    'for_all_exp',
]
