#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import argparse
from argparse import RawTextHelpFormatter

_DEFAULT_IGNORED_PATH_SEGMENTS = ["bin", "target", "examples", "test"]
_VERSION = '%(prog)s 0.1.0'


class Cli:

    def __init__(self, deps_analysers, change_analysers, loc_analysers):
        self._parser = argparse.ArgumentParser(
            formatter_class=RawTextHelpFormatter)
        analyser_types = self._parser.add_subparsers(
            dest='analysis_type', metavar='analyser types')
        analyser_types.required = True
        self._add_deps_analysers(analyser_types, deps_analysers)
        self._add_change_analysers(analyser_types, change_analysers)
        self._add_comp_analysers(analyser_types, loc_analysers)

        self._parser.add_argument(
            '-v', '--version', action='version', version=_VERSION)

    def _add_comp_analysers(self, analyser_types, locanalyser_names):
        locanalyers = analyser_types.add_parser(
            "comp", help="Complexity analysers")
        required_for_comp = locanalyers.add_argument_group()
        required_for_comp.add_argument(
            '-a',
            dest='analysers',
            metavar='analysers',
            nargs='+',
            choices=locanalyser_names,
            required=True,
            help='List of analysers')
        locanalyers.add_argument(
            '-w',
            dest='workingdir',
            metavar='workingdir',
            default=os.getcwd(),
            help='Root folder for recursive analysers. Default is script location')
        locanalyers.add_argument(
            '-o',
            dest='outputdir',
            metavar='outputdir',
            default=os.getcwd(),
            help='Root folder for analysers results. Default is script location')
        locanalyers.add_argument(
            '-i',
            dest='ignored',
            metavar='ignored path segments',
            default=_DEFAULT_IGNORED_PATH_SEGMENTS,
            nargs='*',
            help="List of ignored path segements. Defaults: " +
            ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS) +
            ". Provide empty list to include all paths")
        locanalyers.set_defaults(since="")

    def _add_deps_analysers(self, analyser_types, depsanalyser_names):
        depsanalysers = analyser_types.add_parser(
            "deps", help='Dependency analysers')
        required_for_deps = depsanalysers.add_argument_group()
        required_for_deps.add_argument(
            '-a',
            dest='analysers',
            metavar='analysers',
            nargs='+',
            choices=depsanalyser_names,
            required=True,
            help='List of analysers')
        depsanalysers.add_argument(
            '-w',
            dest='workingdir',
            metavar='workingdir',
            default=os.getcwd(),
            help='Root folder for recursive analysers. Default is script location')
        depsanalysers.add_argument(
            '-o',
            dest='outputdir',
            metavar='outputdir',
            default=os.getcwd(),
            help='Root folder for analysers results. Default is script location')
        depsanalysers.add_argument(
            '-i',
            dest='ignored',
            metavar='ignored path segments',
            default=_DEFAULT_IGNORED_PATH_SEGMENTS,
            nargs='*',
            help="List of ignored path segements. Defaults: " +
            ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS) +
            ". Provide empty list to include all paths")
        depsanalysers.set_defaults(since="")

    def _add_change_analysers(self, analyser_types, changeanalyser_names):
        changeanalysers = analyser_types.add_parser(
            "changes", help='Change analysers')
        required_for_change = changeanalysers.add_argument_group()
        required_for_change.add_argument(
            '-a',
            dest='analysers',
            metavar='analysers',
            nargs='+',
            choices=changeanalyser_names,
            required=True,
            help='List of analysers')
        required_for_change.add_argument(
            '-s',
            dest='since',
            metavar='since',
            default=None,
            required=True,
            help='Date since when the changes were made in ISO 8601. Examples: 2009-06-30, 2009-06-30T18:30:00')
        changeanalysers.add_argument(
            '-w',
            dest='workingdir',
            metavar='workingdir',
            default=os.getcwd(),
            help='Root folder for recursive analysers. Default is script location')
        changeanalysers.add_argument(
            '-o',
            dest='outputdir',
            metavar='outputdir',
            default=os.getcwd(),
            help='Root folder for analysers results. Default is script location')
        changeanalysers.set_defaults(ignored="")

    def parse(self):
        args = self._parser.parse_args()
        return args.workingdir, args.ignored, args.analysis_type, args.analysers, args.outputdir, args.since
