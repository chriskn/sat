#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from domain import Package
import source.sourcerepo as repo


class PackageParser:

    def parse_packages(self, sourcefolders):
        sourcepackages = []
        for sourcefolder in sourcefolders:
            sourcepackages.extend(self._parse(sourcefolder))
        return sourcepackages

    def _parse(self, sourcefolder):
        source_packages = []
        for dirpath, dirname, files in os.walk(sourcefolder):
            java_filenames = [file for file in files if file.endswith(".java")]
            if java_filenames:
                packagename = os.path.normpath(
                    dirpath.replace(sourcefolder, ""))
                packagename = ".".join(packagename.strip(os.sep).split(os.sep))
                sourcefiles = repo.sourcefiles(java_filenames, dirpath, packagename)
                new_package = Package(packagename, dirpath, sourcefiles)
                source_packages.append(new_package)
        return source_packages
