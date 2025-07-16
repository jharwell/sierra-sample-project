# Copyright 2022 John Harwell, All rights reserved.
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

"""Classes for the agent fuel level batch criteria.

Must be specified like <min>.<max>.C<Cardinality> on the
cmdline.

E.g., 1.9.C5 would give 5 experiments with max fuel levels of 1,3,5,7,9.
"""

# Core packages
import typing as tp
import re
import pathlib

# 3rd party packages
import implements
import numpy as np
from sierra.core.experiment import definition
from sierra.core import types
import sierra.core.variables.batch_criteria as bc
from sierra.core.graphs import bcbridge

# Project packages


@implements.implements(bcbridge.IGraphable)
class AgentFuel(bc.UnivarBatchCriteria):
    """A univariate range specifiying the  agent fuel. This class is a base
    class which should (almost) never be used on its own. Instead, the
    ``factory()`` function should be used to dynamically create derived classes
    expressing the user's desired types to disseminate.

    """

    def __init__(self,
                 cli_arg: str,
                 main_config: types.YAMLDict,
                 batch_input_root: pathlib.Path,
                 levels: tp.List[float]) -> None:
        bc.UnivarBatchCriteria.__init__(self,
                                        cli_arg,
                                        main_config,
                                        batch_input_root)

        self.levels = levels
        self.attr_changes = []  # type: tp.List

    def gen_attr_changelist(self) -> tp.List[definition.AttrChange]:
        if not self.attr_changes:
            chgs = [definition.AttrChangeSet(definition.AttrChange("fuel",
                                                                   "level",
                                                                   str(l)),
                                             definition.AttrChange("fuel",
                                                                   "type",
                                                                   "gasoline"))
                    for l in self.levels]
            self.attr_changes = chgs

        return self.attr_changes

    def gen_exp_names(self) -> tp.List[str]:
        changes = self.gen_attr_changelist()
        return ['exp' + str(x) for x in range(0, len(changes))]

    def graph_info(
        self,
        cmdopts: types.Cmdopts,
        batch_output_root: tp.Optional[pathlib.Path] = None,
        exp_names: tp.Optional[tp.List[str]] = None,
    ) -> bcbridge.GraphInfo:
        info = bcbridge.GraphInfo(
            cmdopts,
            batch_output_root,
            exp_names if exp_names else self.gen_exp_names(),
        )

        info.xticks = list(map(float, range(0, len(info.exp_names))))
        info.xticklabels = [str(s) for s in self.levels]
        info.xlabel = "Fuel levels"
        return info


class Parser():
    """
    Enforces the cmdline definition of the :class:`MaxAgentSpeed` batch
    criteria.
    """

    def __call__(self, arg: str) -> types.CLIArgSpec:
        """
        Returns:
            Dictionary with keys: min_speed, max_speed, cardinality

        """
        ret = {
            'min_fuel': str(),
            'max_fuel': str(),
            'cardinality': int()
        }

        sections = arg.split('.')

        # remove batch criteria variable name, leaving only the spec
        sections = sections[1:]
        assert len(sections) == 3, \
            ("Spec must have 3 sections separated by '.'; "
             f"have {len(sections)} from '{arg}'")

        # Parse min fuel
        res = re.search("[0-9]+", sections[0])
        assert res is not None, \
            "Bad min fuel in criteria section '{sections[0]}'"
        ret['min'] = int(res.group(0))

        # Parse max fuel
        res = re.search("[0-9]+", sections[1])
        assert res is not None, \
            "Bad max fuel in criteria section '{sections[1]}'"
        ret['max'] = int(res.group(0))

        # Parse cardinality
        res = re.search("C[0-9]+", sections[2])
        assert res is not None, \
            "Bad cardinality in criteria section '{sections[2]}'"

        ret['cardinality'] = int(res.group(0)[1:])

        return ret

    def to_fuels(self, attr: types.CLIArgSpec) -> tp.List[float]:
        """
        Generate the max fuels sizes for each experiment in a batch.
        """
        return [x for x in np.linspace(attr['min'],
                                       attr['max'],
                                       attr['cardinality'])]


def factory(cli_arg: str,
            main_config: types.YAMLDict,
            cmdopts: types.Cmdopts,
            batch_input_root: pathlib.Path,
            **kwargs):
    """
    Factory to create ``MaxAgentFuel`` derived classes from the command line
            definition.

    """
    parser = Parser()
    attr = parser(cli_arg)
    fuels = parser.to_fuels(attr)

    def __init__(self) -> None:
        AgentFuel.__init__(self,
                               cli_arg,
                               main_config,
                               batch_input_root,
                               fuels)

    return type(cli_arg,
                (AgentFuel,),
                {"__init__": __init__})


__api__ = [
    'AgentFuel'
]
