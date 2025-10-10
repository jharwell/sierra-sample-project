#
# Copyright 2024 John Harwell, All rights reserved.
#
# SPDX-License Identifier: MIT
#

# Core packages
import typing as tp
import argparse
import logging
import pathlib
import psutil

# 3rd party packages
import implements

# Project packages
from sierra.core.experiment import bindings, definition
from sierra.core.variables import batch_criteria as bc
from sierra.core import types
from sierra.plugins.execenv import hpc
from sierra.plugins.execenv import prefectserver
from plugins.jsonsim import cmdline

_logger = logging.getLogger(__name__)


@implements.implements(bindings.IExpShellCmdsGenerator)
class ExpShellCmdsGenerator:
    """A class that conforms to
    :class:`~sierra.core.experiment.bindings.IExpShellCmdsGenerator`.
    """

    def __init__(self, cmdopts: types.Cmdopts, exp_num: int) -> None:
        pass

    def pre_exp_cmds(self) -> tp.List[types.ShellCmdSpec]:
        return []

    def exec_exp_cmds(self, exec_opts: types.StrDict) -> tp.List[types.ShellCmdSpec]:
        return []

    def post_exp_cmds(self) -> tp.List[types.ShellCmdSpec]:
        return []


@implements.implements(bindings.IExpRunShellCmdsGenerator)
class ExpRunShellCmdsGenerator:
    """A class that conforms to
    :class:`~sierra.core.experiment.bindings.IExpRunShellCmdsGenerator`.
    """

    def __init__(
        self,
        cmdopts: types.Cmdopts,
        criteria: bc.XVarBatchCriteria,
        n_agents: int,
        exp_num: int,
    ) -> None:
        self.executable_path = cmdopts["jsonsim_path"]
        self.gen_dist = cmdopts["gen_dist"]

        pass

    def pre_run_cmds(
        self, host: str, input_fpath: pathlib.Path, run_num: int
    ) -> tp.List[types.ShellCmdSpec]:
        return []

    def exec_run_cmds(
        self, host: str, input_fpath: pathlib.Path, run_num: int
    ) -> tp.List[types.ShellCmdSpec]:
        cmd = f"python3 {self.executable_path} --config {input_fpath}.json --distribution={self.gen_dist}"
        return [
            types.ShellCmdSpec(
                cmd=cmd,
                shell=True,
                wait=True,
            )
        ]

    def post_run_cmds(
        self, host: str, run_output_root: pathlib.Path
    ) -> tp.List[types.ShellCmdSpec]:
        return []


@implements.implements(bindings.IExpConfigurer)
class ExpConfigurer:
    def __init__(self, cmdopts: types.Cmdopts) -> None:
        self.cmdopts = cmdopts

    def for_exp_run(
        self, exp_input_root: pathlib.Path, run_output_root: pathlib.Path
    ) -> None:
        pass

    def for_exp(self, exp_input_root: pathlib.Path) -> None:
        pass

    def parallelism_paradigm(self) -> str:
        return "per-batch"


def cmdline_parser() -> argparse.ArgumentParser:
    """
    Get a cmdline parser supporting the engine. The returned parser
    should extend :class:`~sierra.core.cmdline.BaseCmdline`.

    This example extends :class:`~sierra.core.cmdline.BaseCmdline` with:

    - :class:`~sierra.core.hpc.cmdline.HPCCmdline` (HPC common)
    - :class:`~cmd.EngineCmdline` (engine specifics)

    assuming this engine can run on HPC environments.
    """
    # Initialize all stages and return the initialized
    # parser to SIERRA for use.

    parser1 = hpc.cmdline.HPCCmdline([-1, 1, 2, 3, 4, 5]).parser
    parser2 = prefectserver.cmdline.PrefectCmdline([-1, 1, 2, 3, 4, 5]).parser
    return cmdline.EngineCmdline(
        parents=[parser1, parser2], stages=[-1, 1, 2, 3, 4, 5]
    ).parser


def population_size_from_pickle(
    exp_def: tp.Union[definition.AttrChangeSet, definition.ElementAddList],
    main_config: types.YAMLDict,
    cmdopts: types.Cmdopts,
) -> int:
    """
    Given an experiment definition, main configuration, and cmdopts,
    get the # agents in the experiment.Size can be obtained from added
    tags or changed attributes; engine specific.

    Arguments:

        exp_def: *Part* of the pickled experiment definition object.

        main_config: Main project configuration.

        cmdopts: Dictionary of parsed cmdline options.

    """
    return 1


def population_size_from_def(
    exp_def: definition.BaseExpDef, main_config: types.YAMLDict, cmdopts: types.Cmdopts
) -> int:
    """
    Arguments:

        exp_def: The *entire* experiment definition object.

    """
    return 1


def cmdline_postparse_configure(
    execenv: str, args: argparse.Namespace
) -> argparse.Namespace:
    """
    Configure cmdline args after parsing for the engine.

    This sets arguments appropriately depending on what environment
    is selected with ``--execenv``.

    - hpc.local

    - prefectserver.local

    - prefectserver.dockerremote

    """

    # No configuration needed for stages 3-5
    if not any(stage in args.pipeline for stage in [1, 2]):
        return args

    if execenv == "hpc.local":
        return _configure_hpc_local(args)
    elif execenv == "prefectserver.local":
        return _configure_prefectserver_local(args)
    elif execenv == "prefectserver.dockerremote":
        return args

    _logger.warning(f"'{execenv}' unsupported on JSONSIM--may crash unexpectedly!")
    return args


def _configure_prefectserver_local(args: argparse.Namespace) -> argparse.Namespace:
    _logger.debug("Configuring for Prefect local execution")

    if args.exec_jobs_per_node is None:
        parallel_jobs = int(psutil.cpu_count())

        # Make sure we don't oversubscribe cores
        args.exec_jobs_per_node = min(args.n_runs, parallel_jobs)

    _logger.debug("Allocated %s parallel runs/node", args.exec_jobs_per_node)

    return args


def _configure_hpc_local(args: argparse.Namespace) -> argparse.Namespace:
    _logger.debug("Configuring for HPC local execution")

    if args.exec_jobs_per_node is None:
        parallel_jobs = int(psutil.cpu_count())

        # Make sure we don't oversubscribe cores--each simulation needs at
        # least 1 core.
        args.exec_jobs_per_node = min(args.n_runs, parallel_jobs)

    _logger.debug("Allocated %s parallel runs/node", args.exec_jobs_per_node)

    return args
