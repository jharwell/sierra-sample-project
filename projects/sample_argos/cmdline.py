# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT
#
"""
Command line parsing and validation for the the sample ARGoS-based project.
"""

# Core packages
import typing as tp
import argparse

# 3rd party packages

# Project packages
from sierra.plugins import PluginCmdline
from sierra.core import types

def build(
    parents: list[argparse.ArgumentParser], stages: list[int]
) -> PluginCmdline:
    """
    Get a cmdline for the ARGoS sample project.
    """
    cmdline = PluginCmdline(parents, stages)
    cmdline.multistage.add_argument("--scenario",
                                     help="""

                                     Which scenario the swarm comprised of
                                     robots running the controller specified via
                                     ``--controller`` should be run in.

                                     Valid scenarios:

                                     - ``LowBlockCount.AxBxC``
                                     - ``HighBlockCount.AxBxC`

                                     where A,B,C are the arena dimensions.

                                 """ + cmdline.stage_usage_doc([1, 2, 3, 4]))

    cmdline.multistage.add_argument("--controller",
                                     choices=['foraging.footbot_foraging',
                                              'foraging.footbot_foraging_slow',
                                              'foraging.footbot_foraging2',
                                              'foraging.footbot_foraging_slow2'],
                                     help="""

                                     Which controller robots should run.

                                     Valid controllers:

                                     - ``foraging.footbot_foraging``

                                     - ``foraging.footbot_foraging_slow``

                                     - ``foraging.footbot_foraging2``

                                     - ``foraging.footbot_foraging_slow2``

                                 """ + cmdline.stage_usage_doc([1, 2, 3, 4]))

    return cmdline

def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    return {
        'scenario': args.scenario,
        'controller': args.controller,
    }
