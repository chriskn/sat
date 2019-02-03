#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from javalang.tree import (ClassDeclaration, ConstructorDeclaration,
                           EnumDeclaration, InterfaceDeclaration,
                           MethodDeclaration)

import java

from comp.domain import Method, Type
import comp.compcalculator as comp


def is_method(body_element):
    return isinstance(body_element, (MethodDeclaration, ConstructorDeclaration))


def is_type(type_):
    return isinstance(type_, (ClassDeclaration, InterfaceDeclaration, EnumDeclaration))


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


def _filter_types(node, types):
    children = node.children
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
        comp_method = Method(name, complexity)
        analysed_methods.append(comp_method)
    return analysed_methods
