#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deps.parser.sourcefileparser import SourcefileParser

_sourcefiles = dict()
_parser = SourcefileParser()


def sourcefiles(java_file_names, package_path, packagename=""):
    global _sourcefiles
    key = "".join(java_file_names) + package_path + packagename
    if _sourcefiles.get(key):
        return _sourcefiles.get(key)
    _sourcefiles[key] = _parser.parse_sourcefiles(
        java_file_names, package_path, packagename)
    return _sourcefiles.get(key)
