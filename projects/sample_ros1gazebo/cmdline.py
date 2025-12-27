# Copyright 2021 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT
#
"""
Command line parsing and validation for ROS+Gazebo-based sample project.
"""

# Core packages
import typing as tp
import argparse

# 3rd party packages

# Project packages
from sierra.core import types
from sierra.plugins import PluginCmdline

def build(
    parents: list[argparse.ArgumentParser], stages: list[int]
) -> PluginCmdline:
    """
    Get a cmdline for the ROS1+Gazebo sample project.
    """
    cmdline = PluginCmdline(parents, stages)
    cmdline.multistage.add_argument("--scenario",
                                     help="""
                                          Which scenario the system comprised of
                                          robots running the controller
                                          specified via ``--controller`` should
                                          be run in.

                                          Valid scenarios:

                                              - ``HouseWorld.AxBxC``
                                          """ + cmdline.stage_usage_doc([1, 2, 3, 4]))

    cmdline.multistage.add_argument("--controller",
                                     choices=['turtlebot3.wander'],
                                     help="""

                                     Which controller robots should run.

                                 """ + cmdline.stage_usage_doc([1, 2, 3, 4]))

    return cmdline

def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    return {
        'scenario': args.scenario,
        'controller': args.controller,
    }
