# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT
#
"""
Command line parsing and validation for the :term:`ARGoS`.
"""

# Core packages
import typing as tp
import argparse

# 3rd party packages

# Project packages
from sierra.core import types, config
import sierra.core.cmdline as cmd
from sierra.plugins.execenv import hpc

class EngineCmdline(cmd.BaseCmdline):
    """Defines extensions to :class:`~sierra.core.cmdline.CoreCmdline` for JSONSIM.

    """

    def __init__(self,
                 parents: tp.Optional[tp.List[argparse.ArgumentParser]],
                 stages: tp.List[int]) -> None:

        if parents is not None:
            self.parser = argparse.ArgumentParser(add_help=False,
                                                  parents=parents,
                                                  allow_abbrev=False)
        else:
            self.parser = argparse.ArgumentParser(add_help=False,
                                                  allow_abbrev=False)

        self.parser.add_argument("--jsonsim-path",
                                 help="""

                                     The path to the JSONSIM executable
                                     script. Since the script is part of this
                                     sample repo and not actually installed
                                     anywhere, and THIS sample repo isn't
                                     installed anywhere either, this is the best
                                     way to specify the path to avoid hardcoding
                                     it in plugin.py

                                     """,
                                 required=True)

        self.scaffold_cli()
        self.init_cli(stages)

    def scaffold_cli(self) -> None:
        self.stage1_exp = self.parser.add_argument_group(
            'Stage1: Experiment generation')

    def init_cli(self, stages: tp.List[int]) -> None:
        if 1 in stages:
            self.init_stage1()

    def init_stage1(self) -> None:
        # Experiment options

        self.stage1_exp.add_argument("--exp-setup",
                                     help="""

                                     Defines experiment run length, # of
                                     datapoints to capture/capture interval for
                                     each simulation. See
                                     :ref:`usage/vars/expsetup` for a full
                                     description.

                            """ + self.stage_usage_doc([1]),
                                     default="exp_setup.T10.K5.{0}".format(
                                         config.kExperimentalRunData['n_datapoints_1D']))


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    """Update cmdopts with ARGoS-specific cmdline options.

    """
    opts = hpc.cmdline.to_cmdopts(args)
    print("HERE")
    self_updates = {
        # Stage 1
        'jsonsim_path': args.jsonsim_path,
        'exp_setup': args.exp_setup
    }

    opts |= self_updates
    return opts
