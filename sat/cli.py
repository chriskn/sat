#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from argparse import RawTextHelpFormatter

_DEFAULT_IGNORED_PATH_SEGMENTS = ["bin", "target", "examples", "test"]
_VERSION = '%(prog)s 0.1.0'

class Cli:

    _parser = None

    def __init__(self, analysers):
        self._parser = argparse.ArgumentParser(
            formatter_class=RawTextHelpFormatter)
        analyser_names = [analyser.name() for analyser in analysers]
        subParsers = self._parser.add_subparsers(dest='cmd', metavar='analysis type')
        subParsers.required = True
        depsAnalysis = subParsers.add_parser("deps", help='Dependency analysis')
        requiredForDeps = depsAnalysis.add_argument_group()
        requiredForDeps.add_argument('-a', dest='abstractions', metavar='abstraction level', nargs='+', action='append',
                              choices=analyser_names, required=True, help='List of abstraction levels the analysis should run for')
        depsAnalysis.add_argument('-w', dest='workingdir' , metavar='workingdir', default=os.getcwd(),
                                  help='Root folder for recursive analysis. Default is script location')
        depsAnalysis.add_argument('-i', dest='ignored', metavar='ignored path segments', default=_DEFAULT_IGNORED_PATH_SEGMENTS, nargs='*',
                                  help="List of ignored path segements. Defaults: " +
                                  ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS) +
                                  ". Provide empty list to include all paths"
                                  )
        self._parser.add_argument(
            '-v', '--version', action='version', version=_VERSION)

    def parse(self):
        args = self._parser.parse_args()
        return args.workingdir, args.ignored, args.abstractions
