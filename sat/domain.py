#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Project:

    def __init__(self, name, location, source_packages):
        self.name = name
        self.location = location
        self.source_packages = source_packages

    def __lt__(self, other):
        return self.name < other.name

    def imports(self):
        imports = []
        for package in self.source_packages:
            imports.extend(package.imports())
        return imports


class Bundle:

    def __init__(self, path, name, version, exported_packages, imported_packages, required_bundles, num_dependencies):
        self.path = path.strip(" ")
        self.name = name.strip(" ")
        self.version = version.strip(" ")
        self.exported_packages = exported_packages
        self.imported_packages = imported_packages
        self.required_bundles = required_bundles
        self.num_dependencies = num_dependencies

    def __repr__(self):
        return " ".join([self.name, self.version])

    def __hash__(self):
        return (self.name.lower()+self.version).__hash__()

    def __eq__(self, other):
        return self.name.lower() == other.name.lower() and self.version == other.version


class Package:

    def __init__(self, name, location, sourcefiles):
        self.name = name
        self.location = location
        self.sourcefiles = sourcefiles

    def imports(self):
        imports = []
        for sourceFile in self.sourcefiles:
            for imp in sourceFile.imports:
                imports.append(imp)
        return imports


class SourceFile:

    def __init__(self, name, language, imports, loc, concrete_classes, abstract_classes, interfaces, enums):
        self.name = name
        self.language = language
        self.imports = imports
        self.loc = loc
        self.concrete_classes = concrete_classes
        self.abstract_classes = abstract_classes
        self.interfaces = interfaces
        self.enums = enums


class Interface():

    def __init__(self, name, methods, attributes, extends, modifiers):
        self.name = name
        self.methods = methods
        self.attributes = attributes
        self.extends = extends
        self.modifiers = modifiers


class Enum():

    def __init__(self, name, constants, modifiers):
        self.name = name
        self.constants = constants
        self.modifiers = modifiers
        self.typename = "enum"


class Class():

    def __init__(self, name, methods, attributes, implements, extends, modifiers):
        self.name = name
        self.methods = methods
        self.attributes = attributes
        self.implements = implements
        self.extends = extends
        self.modifiers = modifiers


class Method():

    def __init__(self, name, return_type_name, modifiers, parameters):
        self.name = name
        self.return_type_name = return_type_name
        self.modifiers = modifiers
        self.parameters = parameters


class Declaration():

    def __init__(self, name, type_name, modifiers):
        self.name = name
        self.typename = type_name
        self.modifiers = modifiers


class Change():

    def __init__(self, lines_added, lines_removed, filename):
        self.lines_added = lines_added
        self.lines_removed = lines_removed
        self.filename = filename
