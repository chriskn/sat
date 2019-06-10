#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sat.deps.repo.sourcerepo as repo
from sat.deps.domain import Package


def parse_packages(sourcefolders):
    sourcepackages = []
    for sourcefolder in sourcefolders:
        sourcepackages.extend(_parse_sourcefolder(sourcefolder))
    return sourcepackages


def _parse_sourcefolder(sourcefolder):
    source_packages = []
    for package_path, _, files in os.walk(sourcefolder):
        java_filenames = [file for file in files if file.endswith(".java")]
        if java_filenames:
            new_package = _parse_package(package_path, sourcefolder, java_filenames)
            source_packages.append(new_package)
    return source_packages


def _parse_package(package_path, sourcefolder, java_filenames):
    packagename = os.path.normpath(package_path.replace(sourcefolder, ""))
    packagename = ".".join(packagename.strip(os.sep).split(os.sep))
    sourcefiles = repo.sourcefiles(java_filenames, package_path, packagename)
    return Package(packagename, package_path, sourcefiles)
