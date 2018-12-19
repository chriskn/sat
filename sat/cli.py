#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from argparse import RawTextHelpFormatter

_DEFAULT_IGNORED_PATH_SEGMENTS = ["bin", "target", "examples", "test"]
_VERSION = '%(prog)s 0.1.0'


class Cli:

    def __init__(self, deps_analysers, change_analysers):
        self._parser = argparse.ArgumentParser(
            formatter_class=RawTextHelpFormatter)
        analyser_types = self._parser.add_subparsers(
            dest='analysis_type', metavar='analyser types')
        analyser_types.required = True
        self._add_deps_analysers(analyser_types, deps_analysers)
        self._add_change_analysers(analyser_types, change_analysers)
        self._parser.add_argument(
            '-v', '--version', action='version', version=_VERSION)

    def _add_deps_analysers(self, analyser_types, depsanalyser_names):
        depsanalysers = analyser_types.add_parser(
            "deps", help='Dependency analysers')
        requiredForDeps = depsanalysers.add_argument_group()
        requiredForDeps.add_argument('-a', dest='analysers', metavar='analysers', nargs='+',
                                     choices=depsanalyser_names, required=True, help='List of analysers')
        depsanalysers.add_argument('-w', dest='workingdir', metavar='workingdir', default=os.getcwd(),
                                   help='Root folder for recursive analysers. Default is script location')
        depsanalysers.add_argument('-o', dest='outputdir', metavar='outputdir', default=os.getcwd(),
                                   help='Root folder for analysers results. Default is script location')
        depsanalysers.add_argument('-i', dest='ignored', metavar='ignored path segments', default=_DEFAULT_IGNORED_PATH_SEGMENTS, nargs='*',
                                   help="List of ignored path segements. Defaults: " +
                                   ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS) +
                                   ". Provide empty list to include all paths"
                                   )
        depsanalysers.set_defaults(since="")

    def _add_change_analysers(self, analyser_types, changeanalyser_names):
        changeanalysers = analyser_types.add_parser(
            "changes", help='Change analysers')
        requiredForChange = changeanalysers.add_argument_group()
        requiredForChange.add_argument('-a', dest='analysers', metavar='analysers', nargs='+',
                                       choices=changeanalyser_names, required=True, help='List of analysers')
        requiredForChange.add_argument('-s', dest='since', metavar='since', default=None, required=True,
                                       help='Date since when the changes were made in ISO 8601. Examples: 2009-06-30, 2009-06-30T18:30:00')
        changeanalysers.add_argument('-w', dest='workingdir', metavar='workingdir', default=os.getcwd(),
                                     help='Root folder for recursive analysers. Default is script location')
        changeanalysers.add_argument('-o', dest='outputdir', metavar='outputdir', default=os.getcwd(),
                                     help='Root folder for analysers results. Default is script location')
        changeanalysers.add_argument('-i', dest='ignored', metavar='ignored path segments', default=_DEFAULT_IGNORED_PATH_SEGMENTS, nargs='*',
                                     help="List of ignored path segements. Defaults: " +
                                     ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS) +
                                     ". Provide empty list to include all paths"
                                     )

    def parse(self):
        args = self._parser.parse_args()
        return args.workingdir, args.ignored, args.analysis_type, args.analysers, args.outputdir, args.since
      
