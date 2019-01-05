#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Project():

    def __init__(self, path, name, packages):
        self.path = path
        self.name = name
        self.packages = packages
        self.complexity = sum(package.complexity for package in packages)

class Package():

    def __init__(self, path, name, types):
        self.path = path
        self.name = name
        self.types = types
        self.complexity = sum(type_.complexity for type_ in types)

class Type():

    def __init__(self, path, name, methods):
        self.path = path
        self.name = name
        self.methods = methods
        self.complexity = sum(method.complexity for method in methods)


class Method():

    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
