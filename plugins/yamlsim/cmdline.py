# Copyright 2025 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT
#
"""
Command line parsing and validation for the YAMLSIM engine.
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
    Get a cmdline parser supporting the YAMLSIM engine.
    """
    cmdline = PluginCmdline(parents, stages)
    cmdline.stage1.add_argument(
        "--yamlsim-path",
        help="""
             The path to the yamlsim executable script.  Since the script is
             part of this sample repo and not actually installed anywhere, and
             THIS sample repo isn't installed anywhere either, this is the best
             way to specify the path to avoid hardcoding it in plugin.py
             """,
        required=True,
    )

    cmdline.stage1.add_argument(
        "--exp-setup",
        help="""
             Defines experiment run length, # of datapoints to capture/capture
             interval for each simulation.  See :ref:`usage/vars/expsetup` for a
             full description.
             """
        + cmdline.stage_usage_doc([1]),
        default="exp_setup.T10.K5",
    )
    return cmdline


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    """Update cmdopts with YAMLSIM-specific cmdline options."""
    return {
        # Stage 1
        "yamlsim_path": args.yamlsim_path,
        "exp_setup": args.exp_setup,
    }
