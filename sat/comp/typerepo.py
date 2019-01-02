#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comp.domain import Method
from comp.domain import Type
import scanner
import javalang
import logging
import comp.compcalculator as comp
from javalang.parser import JavaSyntaxError
import comp.compcalculator as comp
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration
from javalang.tree import EnumDeclaration

_types = dict()
_logger = logging.getLogger("TypeRepo")


def types(workingdir, ignored_path_segments):
    types = _types.get(workingdir)
    if types:
        return types
    return _parse_types(workingdir, ignored_path_segments)


def _parse_types(workingdir, ignored_path_segments):
    files = scanner.find_java_source_files(
        workingdir, ignored_path_segments)
    parsed_types = []
    for file in files:
        ast = _parse_javafile(file)
        if ast:
            types = _filter_types(ast.types)
            for type_ in types:
                analysed_methods = _parse_methods(type_)
                type_ = Type(file, type_.name, analysed_methods)
                parsed_types.append(type_)
    _types[workingdir] = parsed_types
    return parsed_types


def _parse_methods(type_):
    methods = _filter_methods(type_.body)
    analysed_methods = []
    for method in methods:
        name = method.name
        body = method.body
        if body:
            complexity = comp.complexity(body)
            compMethod = Method(name, complexity)
            analysed_methods.append(compMethod)
    return analysed_methods

def _parse_javafile(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
            ast = javalang.parse.parse(file_content)
            return ast
    except FileNotFoundError as error:
        _logger.warn(str(error))
    except JavaSyntaxError:
        _logger.warn(
            "Could not parse java file %s. Invalid syntax" % file)


def _filter_methods(tle):
    return list(filter(lambda type: isinstance(type, ConstructorDeclaration) or isinstance(type, MethodDeclaration), tle))


def _filter_types(content):
    return list(filter(lambda type: isinstance(type, ClassDeclaration) or isinstance(type, InterfaceDeclaration) or isinstance(type, EnumDeclaration), content))
