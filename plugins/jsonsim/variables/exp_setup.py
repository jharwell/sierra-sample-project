# Copyright 2025 John Harwell, All rights reserved.
#
#  SPDX-License-Identifier: MIT

"""Classes for the ``--exp-setup`` cmdline option for the JSONSIM engine.

"""

# Core packages
import typing as tp

# 3rd party packages
import implements

# Project packages
from sierra.core.variables.base_variable import IBaseVariable
from sierra.core.experiment import definition
from sierra.core import config
from sierra.core.variables import exp_setup


@implements.implements(IBaseVariable)
class ExpSetup():
    """
    Defines the experimental setup for JSONSIM experiments.

    Attributes:
        n_secs_per_run: The :term:`Experimental Run` duration in seconds, NOT
                        :term:`Ticks <Tick>` or timesteps.

        n_datapoints: How many datapoints to capture during the experimental
                      run.

    """

    def __init__(self,
                 n_secs_per_run: int,
                 n_datapoints: int) -> None:
        self.n_secs_per_run = n_secs_per_run
        self.n_datapoints = n_datapoints

        self.element_chgs = None

    def gen_attr_changelist(self) -> tp.List[definition.AttrChangeSet]:
        if not self.element_chgs:
            self.element_chgs = definition.AttrChangeSet(
                definition.AttrChange("$.exp_setup",
                                      "length",
                                      self.n_secs_per_run),
                definition.AttrChange("$.exp_setup",
                                      "n_datapoints",
                                      self.n_datapoints)
            )

        return [self.element_chgs]

    def gen_tag_rmlist(self) -> tp.List[definition.ElementRmList]:
        return []

    def gen_element_addlist(self) -> tp.List[definition.ElementAddList]:
        return []

    def gen_files(self) -> None:
        pass


def factory(arg: str) -> ExpSetup:
    """Create an :class:`ExpSetup` derived class from the command line definition.

    Arguments:

       arg: The value of ``--exp-setup``.

    """
    attr = exp_setup.parse(arg, {'n_secs_per_run': config.kROS['n_secs_per_run'],
                    'n_ticks_per_sec': config.kROS['n_ticks_per_sec'],
                     'n_datapoints': config.kExperimentalRunData['n_datapoints_1D']})

    def __init__(self: ExpSetup) -> None:
        ExpSetup.__init__(self,
                          attr["n_secs_per_run"],
                          attr['n_datapoints'])

    return type(attr['pretty_name'],
                (ExpSetup,),
                {"__init__": __init__})  # type: ignore


__all__ = [
    'ExpSetup',


]
