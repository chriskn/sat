#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import deps.repo.sourcerepo as repo
from deps.domain import Package


def parse_packages(sourcefolders):
    sourcepackages = []
    for sourcefolder in sourcefolders:
        sourcepackages.extend(_parse(sourcefolder))
    return sourcepackages


def _parse(sourcefolder):
    source_packages = []
    for package_path, _, files in os.walk(sourcefolder):
        java_filenames = [file for file in files if file.endswith(".java")]
        if java_filenames:
            packagename = os.path.normpath(
                package_path.replace(sourcefolder, ""))
            packagename = ".".join(packagename.strip(os.sep).split(os.sep))
            sourcefiles = repo.sourcefiles(
                java_filenames, package_path, packagename)
            new_package = Package(packagename, package_path, sourcefiles)
            source_packages.append(new_package)
    return source_packages
