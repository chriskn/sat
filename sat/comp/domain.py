#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913

from sat.app.workspace.domain import Package as WPackage
from sat.app.workspace.domain import Project as WProject
from sat.app.workspace.domain import SourceFile as WSourcefile
from enum import Enum


class Project(WProject):
    def __init__(self, abs_path, rel_path, name, packages):
        WProject.__init__(self, abs_path, rel_path, name, packages)
        self.complexity = sum(package.complexity for package in packages)


class Package(WPackage):
    def __init__(self, abs_path, rel_path, name, sourcefiles, proj_name):
        WPackage.__init__(self, abs_path, rel_path, name, sourcefiles, proj_name)
        self.types = []
        for sfile in sourcefiles:
            self.types.extend(sfile.types)
        self.complexity = sum(type_.complexity for type_ in self.types)


class SourceFile(WSourcefile):
    def __init__(self, abs_path, rel_path, name, types, ast=None):
        WSourcefile.__init__(self, abs_path, rel_path, name, ast)
        self.types = types


class TopLevelType(Enum):
    CLASS = 1
    ABSTRACT_CLASS = 2
    INTERFACE = 3
    ENUM = 4


class TopLevelElement:
    def __init__(self, path, top_level_type, name, methods):
        self.path = path
        self.type = top_level_type
        self.name = name
        self.methods = methods
        self.complexity = sum(method.complexity for method in methods)
        self.num_statements = sum(method.num_statements for method in methods)


class Method:
    def __init__(self, name, complexity, num_statements):
        self.name = name
        self.complexity = complexity
        self.num_statements = num_statements
