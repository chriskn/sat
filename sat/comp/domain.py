#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913

from sat.app.workspace.domain import Package as WPackage
from sat.app.workspace.domain import Project as WProject
from sat.app.workspace.domain import SourceFile as WSourcefile


class Project(WProject):
    def __init__(self, abs_path, rel_path, name, packages):
        WProject.__init__(self, abs_path, rel_path, name, packages)
        self.complexity = sum(package.complexity for package in packages)


class Package(WPackage):
    def __init__(self, abs_path, rel_path, name, sourcefiles):
        WPackage.__init__(self, abs_path, rel_path, name, sourcefiles)
        self.types = []
        for sfile in sourcefiles:
            self.types.extend(sfile.types)
        self.complexity = sum(type_.complexity for type_ in self.types)


class SourceFile(WSourcefile):
    def __init__(self, abs_path, rel_path, name, types, ast=None):
        WSourcefile.__init__(self, abs_path, rel_path, name, ast)
        self.types = types


class Type:
    def __init__(self, path, name, methods):
        self.path = path
        self.name = name
        self.methods = methods
        self.complexity = sum(method.complexity for method in methods)


class Method:
    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
