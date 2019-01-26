#!/usr/bin/env python
# -*- coding: utf-8 -*-
import java
import javalang
from javalang.parser import JavaSyntaxError
from javalang.tree import (ClassDeclaration, ConstructorDeclaration,
                           EnumDeclaration, InterfaceDeclaration,
                           MethodDeclaration)

import comp.compcalculator as comp
import os
from comp.domain import Type, Method


def is_method(body_element):
    return isinstance(
        body_element, ConstructorDeclaration) or isinstance(
        body_element, MethodDeclaration)


def is_type(type):
    return isinstance(type, ClassDeclaration) or isinstance(
        type, InterfaceDeclaration) or isinstance(type, EnumDeclaration)


def parse(java_file):
    parsed_types = []
    ast = java.parse(java_file)
    if ast:
        types = _filter_types(ast, list())
        for ast_type in types:
            analysed_methods = _parse_methods(ast_type)
            path = os.path.normpath(java_file)
            ast_type = Type(path, ast_type.name, analysed_methods)
            parsed_types.append(ast_type)
    return parsed_types


def _filter_types(child, types):
    children = child.children
    for child in children:
        if isinstance(child, list):
            for ele in child:
                if is_type(ele):
                    types.append(ele)
                    _filter_types(ele, types)
    return types


def _parse_methods(ast_type):
    methods = list(filter(is_method, ast_type.body))
    analysed_methods = []
    for method in methods:
        name = method.name
        body = method.body
        complexity = comp.complexity(body) if body else 0
        compMethod = Method(name, complexity)
        analysed_methods.append(compMethod)
    return analysed_methods
