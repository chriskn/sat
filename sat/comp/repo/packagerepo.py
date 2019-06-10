#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sat.scanner as scanner

import sat.comp.repo.typerepo as typerepo
from sat.comp.parser import packageparser

_PACKAGES = dict()


def packages(workingdir, ignored_path_segments):
    workingdir_key = workingdir + "".join(ignored_path_segments)
    analysed_packages = _PACKAGES.get(workingdir_key)
    if analysed_packages:
        return analysed_packages
    types = typerepo.types(workingdir, ignored_path_segments)
    relativepaths_for_package_paths = scanner.find_packages(
        workingdir, ignored_path_segments
    )
    analysed_packages = packageparser.parse_packages(
        relativepaths_for_package_paths, types
    )
    _PACKAGES[workingdir_key] = analysed_packages
    return analysed_packages
