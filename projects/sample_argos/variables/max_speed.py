# Copyright 2022 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

"""Classes for the max robot speed batch criteria.

Must be specified like <min>.<max>.C<Cardinality> on the
cmdline.

E.g., 1.9.C5 would give 5 experiments with max speeds of 1,3,5,7,9.
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
import sierra.core.variables.batch_criteria as bc
from sierra.core import types
from sierra.core.graphs import bcbridge
from sierra.core.variables import builtin

@implements.implements(bcbridge.IGraphable)
class MaxRobotSpeed(bc.UnivarBatchCriteria):
    """A univariate range specifiying the max robot speed. 
    """

    def __init__(
        self,
        cli_arg: str,
        main_config: types.YAMLDict,
        batch_input_root: pathlib.Path,
        speeds: list[float],
    ) -> None:
        bc.UnivarBatchCriteria.__init__(self, cli_arg, main_config, batch_input_root)

        self.speeds = speeds
        self.attr_changes = []  # type: list

    def gen_attr_changelist(self) -> list[definition.AttrChange]:
        if not self.attr_changes:
            chgs = [
                definition.AttrChangeSet(
                    definition.AttrChange(".//wheel_turning", "max_speed", str(s))
                )
                for s in self.speeds
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
        info.xticklabels = [str(s) for s in self.speeds]
        info.xlabel = "Max robot speeds"
        return info


def _parse(arg: str) -> list[float]:
    """Generate the max agent speeds for each experiment in a batch."""

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
    Factory to create :class:`MaxRobotSpeed` classes from the command line
    definition.
    """
    speeds = _parse(cli_arg)

    return MaxRobotSpeed(cli_arg, main_config, batch_input_root, speeds)


__api__ = ["MaxRobotSpeed"]
