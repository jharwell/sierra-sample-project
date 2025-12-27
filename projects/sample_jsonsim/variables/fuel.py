# Copyright 2022 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

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

# Project packages
from sierra.core.experiment import definition
from sierra.core import types
import sierra.core.variables.batch_criteria as bc
from sierra.core.graphs import bcbridge
from sierra.core.variables import builtin

@implements.implements(bcbridge.IGraphable)
class AgentFuel(bc.UnivarBatchCriteria):
    """A univariate range specifiying the  agent fuel. 

    """

    def __init__(
        self,
        cli_arg: str,
        main_config: types.YAMLDict,
        batch_input_root: pathlib.Path,
        levels: list[float],
    ) -> None:
        bc.UnivarBatchCriteria.__init__(self, cli_arg, main_config, batch_input_root)

        self.levels = levels
        self.attr_changes = []  # type: list

    def gen_attr_changelist(self) -> list[definition.AttrChange]:
        if not self.attr_changes:
            chgs = [
                definition.AttrChangeSet(
                    definition.AttrChange("fuel", "level", str(l)),
                    definition.AttrChange("fuel", "type", "gasoline"),
                )
                for l in self.levels
            ]
            self.attr_changes = chgs

        return self.attr_changes

    def gen_exp_names(self) -> list[str]:
        changes = self.gen_attr_changelist()
        return ["exp" + str(x) for x in range(0, len(changes))]

    def graph_info(
        self,
        cmdopts: types.Cmdopts,
        batch_output_root: tp.Optional[pathlib.Path] = None,
        exp_names: tp.Optional[list[str]] = None,
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


def _parse(arg: str) -> list[float]:
    """Generate the agent fuel levels for each experiment in a batch."""

    # remove batch criteria variable name, leaving only the spec
    sections = arg.split(".")[1:]

    return builtin.linspace_parse(".".join(sections), 1.0)

def factory(
    cli_arg: str,
    main_config: types.YAMLDict,
    cmdopts: types.Cmdopts,
    batch_input_root: pathlib.Path,
    **kwargs,
):
    """
    Factory to create :class:`AgentFuel` classes from the command line
    definition.
    """
    fuels = _parse(cli_arg)

    return AgentFuel(cli_arg, main_config, batch_input_root, fuels)


__api__ = ["AgentFuel"]
