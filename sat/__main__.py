#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=W0621,C0103

import datetime
import logging
import os
import sys

from sat.changes.changeexecuter import ChangeExecuter
from sat.comp.compexecuter import CompExecuter
from sat.deps.depsexecuter import DepsExecuter

from sat.app.execution import cli

_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format=_LOG_FORMAT,
    datefmt="%d-%m-%Y %H:%M:%S",
)
_OUTPUT_FOLDER_NAME = datetime.datetime.now().strftime("%d%m%y_%H-%M-%S")

_EXECUTERS = [DepsExecuter, ChangeExecuter, CompExecuter]


def _init_executer(parsed_args, outputdir):
    if parsed_args.executer == DepsExecuter.args().name:
        return DepsExecuter(parsed_args.workingdir, parsed_args.ignored, outputdir)
    if parsed_args.executer == ChangeExecuter.args().name:
        return ChangeExecuter(
            parsed_args.workingdir, parsed_args.ignored, outputdir, parsed_args.since
        )
    if parsed_args.executer == CompExecuter.args().name:
        return CompExecuter(parsed_args.workingdir, parsed_args.ignored, outputdir)
    return None


if __name__ == "__main__":
    cli.run_cli([executer.args() for executer in _EXECUTERS])
    parsed_args = cli.parse()

    outputdir = os.path.join(parsed_args.outputdir, "sat", _OUTPUT_FOLDER_NAME)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    logger = logging.getLogger("SAT")
    logger.info("Ignored paths %s", parsed_args.ignored)
    logger.info("Using directory %s as working directory", parsed_args.workingdir)
    logger.info("Using directory %s as output directory", parsed_args.outputdir)
    logger.info("Running the following analysers: %s", ", ".join(parsed_args.analysers))

    executer = _init_executer(parsed_args, outputdir)
    executer.execute(parsed_args.analysers)
