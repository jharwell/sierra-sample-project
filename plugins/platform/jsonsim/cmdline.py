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
from sierra.core import types, config, hpc
import sierra.core.cmdline as cmd


class PlatformCmdline(cmd.BaseCmdline):
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

        self.parser.add_argument("--exec-path",
                                 help="""

                                     The path to the JSONSIM executable
                                     script. Since the script is part of this
                                     sample repo and not actually installed
                                     anywhere, and THIS sample repo isn't
                                     installed anywhere either, this is the best
                                     way to specify the path to avoid hardcoding
                                     it in plugin.py

                                     """)


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    """Update cmdopts with ARGoS-specific cmdline options.

    """
    opts = hpc.cmdline.to_cmdopts(args)

    self_updates = {
        # Stage 1
        'executable_path': args.exec_path
    }

    opts |= self_updates
    return opts
