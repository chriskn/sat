#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Type():

    def __init__(self, path, name, methods=[]):
        self.path = path
        self.name = name
        self.methods = methods

class Method():

    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
