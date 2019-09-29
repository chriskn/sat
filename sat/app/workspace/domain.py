#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint:disable=R0903,R0913


class Identifiable:
    def __init__(self, abs_path, rel_path, name):
        self.abs_path = abs_path
        self.rel_path = rel_path
        self.name = name

    def __lt__(self, other):
        return self.name < other.name


class Project(Identifiable):
    def __init__(self, abs_path, rel_path, name, packages):
        Identifiable.__init__(self, abs_path, rel_path, name)
        self.packages = packages


class Package(Identifiable):
    def __init__(self, abs_path, rel_path, name, sourcefiles, proj_name=""):
        Identifiable.__init__(self, abs_path, rel_path, name)
        self.sourcefiles = sourcefiles
        self.proj_name = proj_name


class SourceFile(Identifiable):
    def __init__(self, abs_path, rel_path, name, ast, packagename=""):
        Identifiable.__init__(self, abs_path, rel_path, name)
        self.ast = ast
        self.packagename = packagename


class Bundle(Identifiable):
    def __init__(
        self,
        abs_path,
        rel_path,
        name,
        version,
        exported_packages,
        imported_packages,
        required_bundles,
        num_dependencies,
    ):
        Identifiable.__init__(self, abs_path, rel_path, name)
        self.version = version.strip(" ")
        self.exported_packages = exported_packages
        self.imported_packages = imported_packages
        self.required_bundles = required_bundles
        self.num_dependencies = num_dependencies
