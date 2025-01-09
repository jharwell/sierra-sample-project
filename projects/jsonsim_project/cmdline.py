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
Command line parsing and validation for the the sample ARGoS-based project.
"""

# Core packages
import typing as tp
import argparse

# 3rd party packages

# Project packages
import sierra.core.cmdline as cmd
from sierra.core import types, hpc


class Cmdline(cmd.CoreCmdline):
    def __init__(self,
                 parents: tp.List[argparse.ArgumentParser],
                 stages: tp.List[int]):
        super().__init__(parents=parents, stages=stages)

    def init_multistage(self):
        super().init_multistage()

        self.multistage.add_argument("--scenario",
                                     help="""

                                     Which scenario the swarm comprised of
                                     robots running the controller specified via
                                     ``--controller`` should be run in.

                                     Valid scenarios:

                                     - ``scenario1``
                                     - ``scenario2``

                                 """ + self.stage_usage_doc([1, 2, 3, 4]))

        self.multistage.add_argument("--controller",
                                     choices=['default.default'],
                                     help="""

                                     Which controller agents should run.

                                     Valid controllers:

                                     - ``default.default``

                                 """ + self.stage_usage_doc([1, 2, 3, 4]))


def to_cmdopts(args: argparse.Namespace) -> types.Cmdopts:
    # This makes all HPC arguments available when using this platform
    opts = hpc.cmdline.to_cmdopts(args)

    updates = {
        'scenario': args.scenario,
        'controller': args.controller,
    }
    opts |= updates

    return opts
