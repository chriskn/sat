#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Too few public methods, too many args, too many attributes
# pylint: disable=R0903,R0913,R0902

from sat.app.workspace.domain import Package as WPackage
from sat.app.workspace.domain import Project as WProject
from sat.app.workspace.domain import SourceFile as WSourceFile


class Project(WProject):
    def __init__(self, abs_path, rel_path, name, packages):
        WProject.__init__(self, abs_path, rel_path, name, packages)

    def imports(self):
        imports = []
        for package in self.packages:
            imports.extend(package.imports())
        return imports


class Package(WPackage):
    def __init__(self, abs_path, rel_path, name, sourcefiles):
        WPackage.__init__(self, abs_path, rel_path, name, sourcefiles)

    def imports(self):
        imports = []
        for sourcefile in self.sourcefiles:
            for imp in sourcefile.imports:
                imports.append(imp)
        return imports


class SourceFile(WSourceFile):
    def __init__(
        self,
        abs_path,
        rel_path,
        name,
        imports,
        concrete_classes,
        abstract_classes,
        interfaces,
        enums,
    ):
        WSourceFile.__init__(self, abs_path, rel_path, name, ast=None)
        self.imports = imports
        self.concrete_classes = concrete_classes
        self.abstract_classes = abstract_classes
        self.interfaces = interfaces
        self.enums = enums
        self.tles = self._top_level_elements()

    def _top_level_elements(self):
        tles = []
        tles.extend(self.concrete_classes)
        tles.extend(self.abstract_classes)
        tles.extend(self.interfaces)
        tles.extend(self.enums)
        return tles


class ToplevelElement:
    def __init__(self, stereotype, name, fqn, modifiers):
        self.stereotype = stereotype
        self.fqn = fqn
        self.name = name
        self.modifiers = modifiers


class Interface(ToplevelElement):
    def __init__(self, name, fqn, methods, attributes, extends, modifiers):
        ToplevelElement.__init__(self, "interface", name, fqn, modifiers)
        self.methods = methods
        self.attributes = attributes
        self.extends = extends


class Enum(ToplevelElement):
    def __init__(self, name, fqn, constants, modifiers):
        ToplevelElement.__init__(self, "enum", name, fqn, modifiers)
        self.typename = "enum"
        self.constants = constants


class Class(ToplevelElement):
    def __init__(
        self,
        name,
        fqn,
        methods,
        attributes,
        implements,
        extends,
        modifiers,
        stereotype="",
    ):
        ToplevelElement.__init__(self, stereotype, name, fqn, modifiers)
        self.methods = methods
        self.attributes = attributes
        self.implements = implements
        self.extends = extends


class Method:
    def __init__(self, name, return_type_name, modifiers, parameters):
        self.name = name
        self.return_type_name = return_type_name
        self.modifiers = modifiers
        self.parameters = parameters


class Declaration:
    def __init__(self, name, type_name, modifiers):
        self.name = name
        self.typename = type_name
        self.modifiers = modifiers
