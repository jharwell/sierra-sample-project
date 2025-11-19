# Copyright 2025 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT
"""
Command line parsing and validation for the the sample YAML-based project.
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
    Get a cmdline for the YAMLSIM sample project.
    """
    cmdline = PluginCmdline(parents, stages)
    cmdline.multistage.add_argument(
        "--scenario",
        help="""
             Which scenario the controller specified via ``--controller`` should
             be run in.

             Valid scenarios:

                 - ``scenario1``

                 - ``scenario2``
             """
        + cmdline.stage_usage_doc([1, 2, 3, 4]),
    )

    cmdline.multistage.add_argument(
        "--controller",
        choices=["default.default", "default.default2"],
        help="""
             Which controller should be used.

             Valid controllers:

                 - ``default.default``

                 - ``default.default2``
             """
        + cmdline.stage_usage_doc([1, 2, 3, 4]),
    )

    return cmdline


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    return {
        "scenario": args.scenario,
        "controller": args.controller,
    }
