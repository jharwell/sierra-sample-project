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

# Core packages
import re
import logging
import typing as tp

# 3rd party packages

# Project packages


class ScenarioGeneratorParser:
    def __init__(self) -> None:
        self.scenario = None
        self.logger = logging.getLogger(__name__)

    def to_scenario_name(self, args) -> tp.Optional[str]:
        # Stage 5
        if args.scenario is None:
            return None

        # Scenario specified on cmdline
        self.logger.info("Parse scenario generator from cmdline specification '%s'",
                         args.scenario)

        res1 = re.search('LowBlockCount|HighBlockCount', args.scenario)
        assert res1 is not None,\
            "FATAL: Bad block count specification in '{0}'".format(args.scenario)
        res2 = re.search('[0-9]+x[0-9]+x[0-9]+', args.scenario)

        assert res2 is not None,\
            "FATAL: Bad arena_dim specification in '{0}'".format(args.scenario)

        self.scenario = res1.group(0) + "." + res2.group(0)
        return self.scenario

    def to_dict(self, scenario: str) -> tp.Dict[str, tp.Any]:
        x, y, z = scenario.split('+')[0].split('.')[1].split('x')
        count_type = scenario.split('.')[0]

        return {
            'arena_x': int(x),
            'arena_y': int(y),
            'arena_z': int(z),
            'scenario_tag': count_type
        }
