#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import deps.parser.javaparser as javaParser
from deps.domain import SourceFile

class SourcefileParser: 

    def parse_sourcefiles(self, java_filenames, package_path, packagename=""):
        sourcefiles = []
        for javafilename in java_filenames:
            sourcefile = self._parse(javafilename, package_path, packagename)
            if sourcefile:
                sourcefiles.append(sourcefile)
        return sourcefiles
    
    def _parse(self, javafilename, package_path, packagename=""):
        if javafilename.split(".")[1] == "java":
            return javaParser.parse_java_sourcefile(os.path.join(package_path, javafilename), packagename)

