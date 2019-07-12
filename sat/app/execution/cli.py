#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import argparse
from argparse import RawTextHelpFormatter

_DEFAULT_IGNORED_PATH_SEGMENTS = ["bin", "target", "examples", "test"]
_VERSION = "%(prog)s 0.1.0"
_PARENT_PARSER = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)


def run_cli(executer_args):
    init_parent_parser()
    executers = _PARENT_PARSER.add_subparsers(
        dest="executer", metavar="executer", required=True
    )
    for args in executer_args:
        _add_executer(executers, args)

    # _add_deps_analysers(analyser_types, deps_analysers)
    # _add_change_analysers(analyser_types, change_analysers)
    # _add_comp_analysers(analyser_types, loc_analysers)


def init_parent_parser():
    _PARENT_PARSER.add_argument(
        "-w",
        dest="workingdir",
        metavar="workingdir",
        default=os.getcwd(),
        help="Root folder for recursive analysers. Default is script location",
    )
    _PARENT_PARSER.add_argument(
        "-i",
        dest="ignored",
        metavar="ignored path segments",
        default=_DEFAULT_IGNORED_PATH_SEGMENTS,
        nargs="*",
        help="List of ignored path segements. Defaults: "
        + ", ".join(_DEFAULT_IGNORED_PATH_SEGMENTS)
        + ". Provide empty list to include all paths",
    )
    _PARENT_PARSER.add_argument(
        "-o",
        dest="outputdir",
        metavar="outputdir",
        default=os.getcwd(),
        help="Root folder for analysers results. Default is script location",
    )
    _PARENT_PARSER.add_argument("-v", "--version", action="version", version=_VERSION)


def _add_executer(executers, executer_args):
    executer = executers.add_parser(executer_args.name, help=executer_args.description)
    arguments = executer.add_argument_group()
    _add_analyser_arg(arguments, executer_args.analyser_names)
    for option in executer_args.options:
        arguments.add_argument(
            option.argument,
            dest=option.dest,
            metavar=option.dest,
            default=option.default,
            required=option.required,
            help=option.help,
        )


def _add_analyser_arg(group, analyser_names):
    group.add_argument(
        "-a",
        dest="analysers",
        metavar="analysers",
        nargs="+",
        choices=analyser_names,
        required=True,
        help="List of analysers %s" % analyser_names,
    )


def parse():
    return _PARENT_PARSER.parse_args()
