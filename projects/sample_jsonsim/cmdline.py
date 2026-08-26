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
from sierra.core import types
from sierra.plugins import PluginCmdline


def build(
    parents: list[argparse.ArgumentParser], stages: list[int]
) -> PluginCmdline:
    """
    Get a cmdline for the JSONSIM sample project.
    """
    cmdline = PluginCmdline(parents, stages)
    cmdline.multistage.add_argument(
        "--scenario",
        choices=["cleanroom", "fieldtest"],
        help="""
             Which scenario the controller specified via ``--controller`` should
             be run in.

             Valid scenarios:

                 - ``cleanroom`` - Testing in a laboratory setting.

                 - ``fieldtest`` - Testing in the messy real world.
             """
        + cmdline.stage_usage_doc([1, 2, 3, 4, 5]),
    )

    cmdline.multistage.add_argument(
        "--controller",
        choices=["signal.kalman", "signal.lowpass", "signal.bandpass", "signal.bandstop"],
        help="""
             Which controller should be used.

             Valid controllers:

                 - ``signal.kalman`` - Kalman filter based filtering.

                 - ``sigmal.lowpass`` - Low-pass filtering.

                 - ``sigmal.bandpass`` - Band-pass filtering.

                 - ``sigmal.bandstop`` - Band-stop filtering.
             """
        + cmdline.stage_usage_doc([1, 2, 3, 4, 5]),
    )

    return cmdline


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    return {
        "scenario": args.scenario,
        "controller": args.controller,
    }
