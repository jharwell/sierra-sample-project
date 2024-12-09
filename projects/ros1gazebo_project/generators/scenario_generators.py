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

# 3rd party packages
from sierra.core.experiment import definition
from sierra.plugins.platform.ros1gazebo.generators import platform_generators

# Project packages


class HouseWorldScenarioGenerator(platform_generators.PlatformExpDefGenerator):
    def __init__(self, *args, **kwargs) -> None:
        platform_generators.PlatformExpDefGenerator.__init__(self,
                                                             *args,
                                                             **kwargs)

    def generate(self) -> definition.BaseExpDef:
        exp_def = super().generate()

        return exp_def


def gen_generator_name(scenario_name: str) -> str:
    res = re.search('HouseWorld', scenario_name)
    assert res is not None, f"Bad scenario name in {scenario_name}"
    scenario = res.group(0)

    return scenario + 'ScenarioGenerator'
