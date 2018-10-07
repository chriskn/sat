#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from argparse import RawTextHelpFormatter

_DEFAULT_IGNORED_PATH__SEGMENTS = ["bin", "target", "examples", "test"]
_VERSION = '%(prog)s 0.1.0'

class Cli:

    _parser = None

    def __init__(self, analysers):
        self._parser = argparse.ArgumentParser(
            formatter_class=RawTextHelpFormatter)
        analyser_names = [analyser.name() for analyser in analysers]
        required = self._parser.add_argument_group('required named arguments')
        required.add_argument('-a', dest='analysers', nargs='+',
                              choices=analyser_names, required=True, help='List of analysis to run')
        self._parser.add_argument('-w', dest='workingdir', default=os.getcwd(),
                                  help='Root folder for recursive analysis. Default is script location')
        self._parser.add_argument('-i', dest='ignored_path_segments', default=_DEFAULT_IGNORED_PATH__SEGMENTS, nargs='*',
                                  help="List of ignored path segements. Default is " +
                                  ", ".join(_DEFAULT_IGNORED_PATH__SEGMENTS) +
                                  ". Provide empty list to include all paths"
                                  )
        self._parser.add_argument(
            '-v', '--version', action='version', version=_VERSION)

    def parse(self):
        args = self._parser.parse_args()
        return args.workingdir, args.ignored_path_segments, args.analysers
