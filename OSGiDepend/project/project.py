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

class Package:
    def __init__(self, name, location, sourceFiles):
        self.name = name
        self.location = location
        self.sourceFiles = sourceFiles
        #self.loc = loc

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
'''
packages = [
    Package("a", ["a","b","c","f","f"]),
    Package("b", ["b","c","a","f","e"]),
    Package("c", ["b","c","f","a"]),
    Package("d", ["b","c","c","f","f"]),
    Package("e", ["b","c","f","f"]),
    Package("f", ["b","c","c","f"]),
    Package("g", ["b","c","f"]),
    Package("h", ["b","c","h"]),
]
'''
