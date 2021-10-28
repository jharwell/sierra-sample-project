# Copyright 2021 John Harwell, All rights reserved.
#
#  This file is part of SIERRA.
#
#  SIERRA is free software: you can redistribute it and/or modify it under the terms of the GNU
#  General Public License as published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  SIERRA is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  SIERRA.  If not, see <http://www.gnu.org/licenses/
#
"""
Command line parsing and validation for the :xref:`TITAN` project.
"""

# Core packages
import typing as tp

# 3rd party packages

# Project packages
import sierra.core.cmdline as cmd


class Cmdline(cmd.CoreCmdline):
    def __init__(self, bootstrap, stages: tp.List[int], for_sphinx: bool):
        super().__init__(bootstrap, stages)

    def init_multistage(self, for_sphinx: bool):
        super().init_multistage(for_sphinx)

        self.multistage.add_argument("--scenario",
                                     help="""

                                     Which scenario the swarm comprised of robots running the
                                     controller specified via ``--controller`` should be run in.

                                     Valid scenarios:

                                     - ``LowBlockCount``
                                     - ``HighBlockCount`

                                 """ + self.stage_usage_doc([1, 2, 3, 4]))

        self.multistage.add_argument("--controller",
                                     help="""

                                     Which controller robots should run.

                                     Valid controllers:

                                     - ``foraging.footbot_foraging``

                                 """ + self.stage_usage_doc([1, 2, 3, 4]))

    @staticmethod
    def cmdopts_update(cli_args, cmdopts: tp.Dict[str, str]):
        updates = {
            'scenario': cli_args.scenario,
            'controller': cli_args.controller,
        }
        cmdopts.update(updates)


class CmdlineValidator(cmd.CoreCmdlineValidator):
    pass
