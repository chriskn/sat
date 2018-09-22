#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Project:
    def __init__(self, name, location, sourcePackages):
        self.name = name
        self.location = location
        self.sourcePackages = sourcePackages
    def __lt__(self,other):
        return self.name < other.name
    
    def getImports(self):
        imports = []
        for package in self.sourcePackages:
            imports.extend(package.getImports()) 
        return imports

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

class Package:
    def __init__(self, name, location, sourceFiles):
        self.name = name
        self.location = location
        self.sourceFiles = sourceFiles

    def getImports(self):
        imports = []
        for sourceFile in self.sourceFiles:
            for imp in sourceFile.imports:
                imports.append(imp)
        return imports

class SourceFile:
    def __init__(self, name, language, imports, loc, concreteClasses, abstractClasses, interfaces):
        self.name = name
        self.language = language
        self.imports = imports
        self.loc = loc
        self.concreteClasses = concreteClasses
        self.abstractClasses = abstractClasses
        self.interfaces = interfaces

