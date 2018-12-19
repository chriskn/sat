#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import lang.java as javaParser
from domain import SourceFile

class SourcefileParser: 

    def parse_sourcefiles(self, java_filenames, dirpath, packagename=""):
        sourcefiles = []
        for javafilename in java_filenames:
            sourcefile = self._parse(javafilename, dirpath, packagename)
            if sourcefile:
                sourcefiles.append(sourcefile)
        return sourcefiles
    
    def _parse(self, javafilename, dirpath, packagename=""):
        if javafilename.split(".")[1] == "java":
            return javaParser.parse_java_sourcefile(os.path.join(dirpath, javafilename), packagename)

