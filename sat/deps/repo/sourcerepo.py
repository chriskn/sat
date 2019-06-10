#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sat.deps.parser.sourcefileparser as parser

_SOURCE_FILES = dict()


def sourcefiles(java_file_names, package_path, packagename=""):
    key = "".join(java_file_names) + package_path + packagename
    if _SOURCE_FILES.get(key):
        return _SOURCE_FILES.get(key)
    _SOURCE_FILES[key] = parser.parse_sourcefiles(
        java_file_names, package_path, packagename
    )
    return _SOURCE_FILES.get(key)
