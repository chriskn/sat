#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from sat.comp.domain import Package

_LOGGER = logging.getLogger("PackageParser")


def parse_packages(packagepaths, types):
    _LOGGER.info("Parsing Packages.")
    parsed_packages = []
    for full_package_path, rel_package_path in packagepaths.items():
        package = _parse_package(rel_package_path, types, full_package_path)
        parsed_packages.append(package)
    return parsed_packages


def _parse_package(rel_package_path, types, full_package_path):
    package_name = rel_package_path.replace(os.sep, ".")
    types_for_package = []
    for type_ in types:
        if _is_under_package(type_, full_package_path):
            types_for_package.append(type_)
    package = Package(full_package_path, package_name, types_for_package)
    return package


def _is_under_package(type_, package_path):
    type_directory = os.path.normpath(os.path.dirname(type_.path))
    norm_package_path = os.path.normpath(package_path)
    if type_directory.endswith(norm_package_path):
        return True
    return False
