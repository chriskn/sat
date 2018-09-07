#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import Cli
from bundle.bundleanalyser import BundleAnalyser

ANALYSERS = [BundleAnalyser()]

if __name__ == '__main__':
    cli = Cli()
    workingDir, ignoredPathSegments = cli.parse()
    print("Ignoring directory path which contain one of the following strings %s" % ignoredPathSegments)
    print("Scanning for bundles in directory %s..." % workingDir)
    for analyser in ANALYSERS: analyser.analyse(workingDir, ignoredPathSegments)    
    for analyser in ANALYSERS: analyser.writeResults(workingDir)    
