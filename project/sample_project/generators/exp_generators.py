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

# 3rd party packages

# Project packages
import sierra.core.generators.exp_generators as exp_generators
from sierra.core.xml import XMLLuigi


class SimDefUniqueGenerator(exp_generators.SimDefUniqueGenerator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def generate(self, exp_def: XMLLuigi, random_seeds):
        super().generate(exp_def, random_seeds)
        self._generate_output(exp_def)

    def _generate_output(self, exp_def: XMLLuigi):
        exp_def.attr_change(".//loop_functions/foraging",
                            "output_dir",
                            os.path.join(self.exp_output_root, self.sim_output_dir, 'output'))


__api__ = [
    'SimDefUniqueGenerator',
]
