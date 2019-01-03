#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Type():

    def __init__(self, path, name, methods=[]):
        self.path = path
        self.name = name
        self.methods = methods

    def complexity(self):
        complexity = 0
        for method in self.methods:
            complexity += method.complexity
        return complexity


class Method():

    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
