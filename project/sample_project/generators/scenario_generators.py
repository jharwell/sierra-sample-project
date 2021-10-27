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

# Project packages
from sierra.core.xml import XMLLuigi
from sierra.core.generators.scenario_generator import ARGoSScenarioGenerator


class ForagingScenarioGenerator(ARGoSScenarioGenerator):
    def __init__(self, *args, **kwargs) -> None:
        ARGoSScenarioGenerator.__init__(self, *args, **kwargs)

    def generate(self) -> XMLLuigi:
        exp_def = super().generate()

        # Generate and apply robot count definitions
        self.generate_n_robots(exp_def)

        return exp_def


# High/low block count scenarios are actually the same in this simple project; checking
# it here and using it to choose which generator to use is shown as an example of what can be
# done.

class LowBlockCountGenerator(ForagingScenarioGenerator):
    pass


class HighBlockCountGenerator(ForagingScenarioGenerator):
    pass


def gen_generator_name(scenario_name: str) -> str:
    res = re.search('LowBlockCount|HighBlockCount', scenario_name)
    assert res is not None, "Bad scenario name in {0}".format(scenario_name)
    scenario = res.group(0)

    return scenario + 'Generator'
