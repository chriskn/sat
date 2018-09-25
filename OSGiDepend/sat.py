#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import Cli
from analysis.bundleanalysis import BundleAnalyser
from analysis.projectanalysis import ProjectAnalyser
from analysis.plainjavaanalysis import PlainJavaAnalyser
from analysis.git import GitChanges
import logging, sys

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT, datefmt='%d-%m-%Y %H:%M:%S')

ANALYSERS = [PlainJavaAnalyser(), ProjectAnalyser(), BundleAnalyser(), GitChanges()]
ANALYSERS_BY_NAME = dict()
for analyser in ANALYSERS:
    ANALYSERS_BY_NAME[analyser.getName()] = analyser


if __name__ == '__main__':
    logger = logging.getLogger("SAT")
    cli = Cli(ANALYSERS)
    workingDir, ignoredPathSegments, analysers = cli.parse()
    logger.info("Ignoring directory paths containing one of the following strings %s" % ignoredPathSegments)
    logger.info("Using directory %s as working directory" % workingDir)
    logger.info("Running the following analysis: %s" % ", ".join(analysers))
    for analyserName in analysers: 
        analyser = ANALYSERS_BY_NAME[analyserName]
        analyser.loadData(workingDir, ignoredPathSegments)    
        analyser.analyse(ignoredPathSegments)    
        analyser.writeResults(workingDir)    
