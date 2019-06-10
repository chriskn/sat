#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import deps.parser.javaparser as javaParser


def parse_sourcefiles(java_filenames, package_path, packagename=""):
    sourcefiles = []
    for java_filename in java_filenames:
        sourcefile = _parse(java_filename, package_path, packagename)
        if sourcefile:
            sourcefiles.append(sourcefile)
    return sourcefiles


def _parse(java_filename, package_path, packagename=""):
    if java_filename.split(".")[1] == "java":
        return javaParser.parse_java_sourcefile(
            os.path.join(package_path, java_filename), packagename
        )
    return None
