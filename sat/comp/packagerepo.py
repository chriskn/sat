#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import comp.compcalculator as comp
import comp.typerepo as typerepo
import scanner
from comp.domain import Package

_packages = dict()
_logger = logging.getLogger("PackageRepo")


def packages(workingdir, ignored_path_segments):
    key = workingdir+"".join(ignored_path_segments)
    packages = _packages.get(key)
    if packages:
        return packages
    types = typerepo.types(workingdir, ignored_path_segments)
    relativepaths_for_package_paths = scanner.find_packages(
        workingdir, ignored_path_segments)
    packages = _parse_packages(relativepaths_for_package_paths, types)
    _packages[key] = packages
    return packages


def _parse_packages(packagepaths, types):
    _logger.info("Parsing Packages.")
    packages = []
    for full_package_path, rel_package_path in packagepaths.items():
        package_name = rel_package_path.replace(os.sep, ".")
        types_for_package = []
        for type_ in types:
            if _is_under_package(type_, full_package_path):
                types_for_package.append(type_)
        package = Package(full_package_path, package_name, types_for_package)
        packages.append(package)
    return packages


def _is_under_package(type_, package_path):
    type_directory = os.path.normpath(
        os.path.dirname(type_.path))
    norm_package_path = os.path.normpath(package_path)
    if type_directory.endswith(norm_package_path):
        return True
    return False
