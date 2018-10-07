#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import lang.java as javaParser
from domain import Package

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
                packagename = os.path.normpath(dirpath.replace(sourcefolder,""))
                packagename = ".".join(packagename.strip(os.sep).split(os.sep))
                sourcefiles = []
                for java_file in java_filenames:
                    sourcefile = javaParser.parse_java_sourcefile(os.path.join(dirpath,java_file))
                    if sourcefile:
                        sourcefiles.append(sourcefile)
                new_package = Package(packagename, dirpath, sourcefiles)
                source_packages.append(new_package)
        return source_packages
