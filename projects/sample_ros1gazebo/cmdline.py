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
    parents: tp.List[argparse.ArgumentParser], stages: tp.List[int]
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
