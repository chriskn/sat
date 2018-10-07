#!/usr/bin/env python
# -*- coding: utf-8 -*-

from javalang.tree import Import
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration
from javalang.tree import FieldDeclaration
from javalang.tree import EnumDeclaration
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
from javalang.parser import JavaSyntaxError
from domain import SourceFile, Declaration, Method, Class, Enum, Interface

import javalang
import os
import re
import logging


classNamePattern = re.compile(r'.*\.[A-Z].*')
logger = logging.getLogger(__name__)


def parse_java_sourcefile(file):
    file_content = None
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        ast = javalang.parse.parse(file_content)
    except FileNotFoundError as error:
        logger.warn(str(error))
        return
    except JavaSyntaxError:
        logger.warn("Could not parse java file %s" % file)
        return
    package_imports = set()
    for imp in ast.imports:
        if classNamePattern.match(imp.path):
            package = re.split(r'\.[A-Z]', imp.path, maxsplit=1)[0]
            package_imports.add(package)
        else:
            package_imports.add(imp.path)
    concrete_classes = [parse_class(type) for type in ast.types if isinstance(
        type, ClassDeclaration) and 'abstract' not in type.modifiers]
    abstract_classes = [parse_class(type) for type in ast.types if isinstance(
        type, ClassDeclaration) and 'abstract' in type.modifiers]
    interfaces = [parse_interface(type) for type in ast.types if isinstance(
        type, InterfaceDeclaration)]
    enums = [parse_enum(type)
             for type in ast.types if isinstance(type, EnumDeclaration)]
    filename, extension = os.path.splitext(os.path.basename(file))
    non_empty_lines = [
        line for line in file_content.splitlines() if line.strip()]
    loc = len(non_empty_lines)
    return SourceFile(filename, extension[1:], package_imports, loc, concrete_classes, abstract_classes, interfaces, enums)


def parse_enum(enum):
    name = enum.name
    constants = [constant.name for constant in enum.body.constants]
    modifiers = enum.modifiers
    return Enum(name, constants, modifiers)


def parse_interface(interface):
    name = interface.name
    extends = interface.extends
    modifiers = interface.modifiers
    attributes = [parse_attribute(attribute)
                  for attribute in filter_attributes(interface.body)]
    methods = [parse_method(methode)
               for methode in filter_methods(interface.body)]
    return Interface(name, methods, attributes, extends, modifiers)


def parse_class(clazz):
    modifiers = clazz.modifiers
    implements = clazz.implements
    extends = clazz.extends
    name = clazz.name
    attributes = [parse_attribute(attribute)
                  for attribute in filter_attributes(clazz.body)]
    methods = [parse_method(methode) for methode in filter_methods(clazz.body)]
    return Class(name, methods, attributes, implements, extends, modifiers)


def filter_methods(body):
    return list(filter(lambda type: isinstance(type, ConstructorDeclaration) or isinstance(type, MethodDeclaration), body))


def filter_attributes(body):
    return list(filter(lambda type: isinstance(type, FieldDeclaration) or isinstance(type, EnumDeclaration), body))


def parse_attribute(attribute):
    if isinstance(attribute, EnumDeclaration):
        return parse_enum(attribute)
    type_name = attribute.type.name
    name = attribute.declarators[0].name
    modifiers = attribute.modifiers
    return Declaration(name, type_name, modifiers)


def parse_method(method):
    modifiers = method.modifiers
    name = method.name
    returnType = ""
    if type(method) == MethodDeclaration:
        returnType = method.return_type.name if method.return_type else ""
    parameter = [parse_parameter(param) for param in method.parameters]
    return Method(name, returnType, modifiers, parameter)


def parse_parameter(param):
    modifiers = param.modifiers
    name = param.name
    type_name = param.type.name
    return Declaration(name, type_name, modifiers)
