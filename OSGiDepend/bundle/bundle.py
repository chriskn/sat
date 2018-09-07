#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Bundle:
    
    def __init__(self, path, name, version, exportedPackages, importedPackages, requiredBundles, numberOfDependencies):
        self.path = path.strip(" ")
        self.name = name.strip(" ")
        self.version = version.strip(" ")
        self.exportedPackages = exportedPackages
        self.importedPackages = importedPackages
        self.requiredBundles = requiredBundles
        self.numberOfDependencies = numberOfDependencies

    def __repr__(self):
        return " ".join([self.name, self.version])

    def __hash__(self):
        return (self.name.lower()+self.version).__hash__()

    def __eq__(self, other):
        return self.name.lower() == other.name.lower() and self.version == other.version