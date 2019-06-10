#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import scanner
import comp.parser.typeparser as parser

_TYPES = dict()
_LOGGER = logging.getLogger("TypeRepo")


def types(workingdir, ignored_path_segments):
    key = workingdir + "".join(ignored_path_segments)
    analysed_types = _TYPES.get(key)
    if not analysed_types:
        analysed_types = _parse_types(workingdir, ignored_path_segments)
        _TYPES[key] = analysed_types
    return analysed_types


def _parse_types(workingdir, ignored_path_segments):
    _LOGGER.info("Parsing Types.")
    files = scanner.find_java_source_files(workingdir, ignored_path_segments)
    parsed_types = []
    for java_file in files:
        parsed_types.extend(parser.parse(java_file))
    return parsed_types
