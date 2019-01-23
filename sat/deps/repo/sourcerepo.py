#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deps.parser.sourcefileparser import SourcefileParser

_sourcefiles = None
_parser = SourcefileParser()

def sourcefiles(path, javafile, packagename=""):
    global _sourcefiles
    if _sourcefiles:
        return _sourcefiles
    else:
       _sourcefiles = _parser.parse_sourcefiles(path, javafile, packagename)
       return _sourcefiles