#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import scanner

import comp.repo.typerepo as typerepo
from comp.domain import Package

_PACKAGES = dict()
_LOGGER = logging.getLogger("PackageRepo")


def packages(workingdir, ignored_path_segments):
    key = workingdir + "".join(ignored_path_segments)
    analysed_packages = _PACKAGES.get(key)
    if analysed_packages:
        return analysed_packages
    types = typerepo.types(workingdir, ignored_path_segments)
    relativepaths_for_package_paths = scanner.find_packages(
        workingdir, ignored_path_segments)
    analysed_packages = _parse_packages(relativepaths_for_package_paths, types)
    _PACKAGES[key] = analysed_packages
    return analysed_packages


def _parse_packages(packagepaths, types):
    _LOGGER.info("Parsing Packages.")
    parsed_packages = []
    for full_package_path, rel_package_path in packagepaths.items():
        package_name = rel_package_path.replace(os.sep, ".")
        types_for_package = []
        for type_ in types:
            if _is_under_package(type_, full_package_path):
                types_for_package.append(type_)
        package = Package(full_package_path, package_name, types_for_package)
        parsed_packages.append(package)
    return parsed_packages


def _is_under_package(type_, package_path):
    type_directory = os.path.normpath(
        os.path.dirname(type_.path))
    norm_package_path = os.path.normpath(package_path)
    if type_directory.endswith(norm_package_path):
        return True
    return False
