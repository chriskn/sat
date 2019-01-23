#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys

from app.analyserrepo import AnalyserRepo
from app.cli import Cli

_LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format=_LOG_FORMAT, datefmt='%d-%m-%Y %H:%M:%S')
_OUTPUT_FOLDER_NAME = datetime.datetime.now().strftime("%d%m%y_%H-%M-%S")


def run_deps_analysers(analysernames, deps_analysers_by_name, workingdir, ignored_path_segments, outputdir):
    for analyser_name in analysernames:
        analyser = deps_analysers_by_name[analyser_name]()
        analyser.load_data(workingdir, ignored_path_segments)
        analyser.analyse(ignored_path_segments)
        analyser.write_results(outputdir)


def run_change_analysers(analysernames, change_analysers_by_name, workingdir, ignored_path_segments, outputdir, since):
    for analyser_name in analysernames:
        analyser = change_analysers_by_name[analyser_name](since)
        analyser.load_data(workingdir, ignored_path_segments)
        analyser.analyse(ignored_path_segments)
        analyser.write_results(outputdir)


def run_comp_analysers(analysernames, comp_analysers_by_name, workingdir, ignored_path_segments, outputdir):
    for analyser_name in analysernames:
        analyser = comp_analysers_by_name[analyser_name]()
        analyser.load_data(workingdir, ignored_path_segments)
        analyser.analyse(ignored_path_segments)
        analyser.write_results(outputdir)


if __name__ == '__main__':
    logger = logging.getLogger("SAT")

    deps_analysers_by_name = AnalyserRepo.deps_analyser_classes_by_name()
    change_analysers_by_name = AnalyserRepo.change_analyser_classes_by_name()
    comp_analysers_by_name = AnalyserRepo.comp_analyser_classes_by_name()

    cli = Cli(deps_analysers_by_name.keys(),
              change_analysers_by_name.keys(), comp_analysers_by_name)
    workingdir, ignored_path_segments, analyser_group, analysers, outputbasedir, since = cli.parse()
    outputdir = os.path.join(outputbasedir, "sat", _OUTPUT_FOLDER_NAME)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    logger.info("Ignoring directory paths containing one of the following strings %s",
                ignored_path_segments)
    logger.info("Using directory %s as working directory", workingdir)
    logger.info("Using directory %s as output directory", outputdir)
    logger.info("Running the following analysers: %s", ", ".join(analysers))

    if analyser_group == "deps":
        run_deps_analysers(analysers, deps_analysers_by_name,
                           workingdir, ignored_path_segments, outputdir)
    if analyser_group == "changes":
        run_change_analysers(analysers, change_analysers_by_name,
                             workingdir, ignored_path_segments, outputdir, since)
    if analyser_group == "comp":
        run_comp_analysers(analysers, comp_analysers_by_name,
                           workingdir, ignored_path_segments, outputdir)
