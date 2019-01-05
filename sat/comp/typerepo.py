#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import scanner
import comp.typeparser as parser
from comp.domain import Type


_types = dict()
_logger = logging.getLogger("TypeRepo")


def types(workingdir, ignored_path_segments):
    key = workingdir+"".join(ignored_path_segments)
    types = _types.get(key)
    if not types:
        types = _parse_types(workingdir, ignored_path_segments)
        _types[key] = types   
    return types


def _parse_types(workingdir, ignored_path_segments):
    _logger.info("Parsing Types.")
    files = scanner.find_java_source_files(
        workingdir, ignored_path_segments)
    parsed_types = []
    for java_file in files:
        parsed_types.extend(parser.parse(java_file))
    return parsed_types


