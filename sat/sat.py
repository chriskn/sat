#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import Cli
from analysis.bundleanalysis import BundleAnalyser
from analysis.projectanalysis import ProjectAnalyser
from analysis.plainjavaanalysis import PlainJavaAnalyser
from analysis.git import GitChanges
import logging
import sys
import datetime
import os

LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format=LOG_FORMAT, datefmt='%d-%m-%Y %H:%M:%S')

ANALYSERS = [PlainJavaAnalyser(), ProjectAnalyser(),
             BundleAnalyser(), GitChanges()]
ANALYSERS_BY_NAME = dict()
for analyser in ANALYSERS:
    ANALYSERS_BY_NAME[analyser.name()] = analyser

_OUTPUT_FOLDER_NAME = datetime.datetime.now().strftime("%d%m%y_%H-%M-%S")

if __name__ == '__main__':
    logger = logging.getLogger("SAT")
    cli = Cli(ANALYSERS)
    workingdir, ignored_path_segments, analysers = cli.parse()
    logger.info("Ignoring directory paths containing one of the following strings %s",
                ignored_path_segments)
    logger.info("Using directory %s as working directory", workingdir)
    logger.info("Running the following analysis: %s", ", ".join(analysers))

    output_folder = os.path.join(workingdir, "sat", _OUTPUT_FOLDER_NAME)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for analyser_name in analysers:
        analyser = ANALYSERS_BY_NAME[analyser_name]
        analyser.load_data(workingdir, ignored_path_segments)
        analyser.analyse(ignored_path_segments)
        analyser.write_results(output_folder)
