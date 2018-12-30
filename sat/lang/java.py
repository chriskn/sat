#!/usr/bin/env python
# -*- coding: utf-8 -*-

import javalang
from javalang.tree import CompilationUnit
from javalang.tree import Import
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration
from javalang.tree import FieldDeclaration
from javalang.tree import EnumDeclaration
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
from javalang.parser import JavaSyntaxError

import os
import re
import logging

from domain import SourceFile, Declaration, Method, Class, Enum, Interface


logger = logging.getLogger(__name__)

def parse_java_sourcefile(file, packagename=""):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
            ast = javalang.parse.parse(file_content)
    except FileNotFoundError as error:
        logger.warn(str(error))
        return
    except JavaSyntaxError:
        logger.warn("Could not parse java file %s. Invalid syntax" % file)
        return
    package_imports = set()
    [package_imports.add(imp.path) for imp in ast.imports]
    concrete_classes = [parse_class(type, packagename) for type in ast.types if isinstance(
        type, ClassDeclaration) and 'abstract' not in type.modifiers]
    abstract_classes = [parse_class(type, packagename, "abstract") for type in ast.types if isinstance(
        type, ClassDeclaration) and 'abstract' in type.modifiers]
    interfaces = [parse_interface(type, packagename) for type in ast.types if isinstance(
        type, InterfaceDeclaration)]
    enums = [parse_enum(type, packagename)
             for type in ast.types if isinstance(type, EnumDeclaration)]
    filename, extension = os.path.splitext(os.path.basename(file))
    return SourceFile(filename, extension[1:], package_imports, concrete_classes, abstract_classes, interfaces, enums)


def parse_enum(enum, packagename=""):
    name = enum.name
    constants = [constant.name for constant in enum.body.constants]
    modifiers = enum.modifiers
    return Enum(name, _getFQN(packagename, name), constants, modifiers)


def parse_interface(interface, packagename=""):
    name = interface.name
    extends = [interface.name for interface in interface.extends] if interface.extends else ""
    modifiers = interface.modifiers
    attributes = [_parse_attribute(attribute)
                  for attribute in _filter_attributes(interface.body)]
    methods = [_parse_method(methode)
               for methode in _filter_methods(interface.body)]
    return Interface(name, _getFQN(packagename, name), methods, attributes, extends, modifiers)


def parse_class(clazz, packagename="", stereotype=""):
    modifiers = clazz.modifiers
    implements = [impl.name for impl in clazz.implements] if clazz.implements else []
    extends = clazz.extends.name if clazz.extends else ""
    name = clazz.name
    attributes = [_parse_attribute(attribute)
                  for attribute in _filter_attributes(clazz.body)]
    methods = [_parse_method(methode)
               for methode in _filter_methods(clazz.body)]
    return Class(name, _getFQN(packagename, name), methods, attributes, implements, extends, modifiers, stereotype)


def _getFQN(packagename, name):
    if packagename:
        return packagename+"."+name
    else:
        return name


def _filter_methods(body):
    return list(filter(lambda type: isinstance(type, ConstructorDeclaration) or isinstance(type, MethodDeclaration), body))


def _filter_attributes(body):
    return list(filter(lambda type: isinstance(type, FieldDeclaration) or isinstance(type, EnumDeclaration), body))


def _parse_attribute(attribute):
    if isinstance(attribute, EnumDeclaration):
        return parse_enum(attribute)
    type_name = attribute.type.name
    name = attribute.declarators[0].name
    modifiers = attribute.modifiers
    return Declaration(name, type_name, modifiers)


def _parse_method(method):
    modifiers = method.modifiers
    name = method.name
    returnType = ""
    if type(method) == MethodDeclaration:
        returnType = method.return_type.name if method.return_type else ""
    parameter = [_parse_parameter(param) for param in method.parameters]
    return Method(name, returnType, modifiers, parameter)


def _parse_parameter(param):
    modifiers = param.modifiers
    name = param.name
    type_name = param.type.name
    return Declaration(name, type_name, modifiers)
