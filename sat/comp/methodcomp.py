#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xls
from analysis.analysis import Analysis
from comp.domain import Method
from comp.domain import Type
import scanner
import javalang
import comp.compcalculator as comp
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
from javalang.tree import ClassDeclaration
from javalang.tree import InterfaceDeclaration
from javalang.tree import EnumDeclaration
from javalang.parser import JavaSyntaxError


class MethodComp(Analysis):

    @staticmethod
    def name():
        return "methods"

    def __init__(self):
        self._types = []
        self._data = []

    def load_data(self, workingdir, ignored_path_segments):
        files = scanner.find_java_source_files(
            workingdir, ignored_path_segments)
        for file in files:
            ast = self._parse_javafile(file)
            if ast:
                types = self._filter_types(ast.types)
                for type_ in types:
                    methods = self._filter_methods(type_.body)
                    self._data.append([file, type_.name, methods])

    def _parse_javafile(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                ast = javalang.parse.parse(file_content)
                return ast
        except FileNotFoundError as error:
            self._logger.warn(str(error))
        except JavaSyntaxError:
            self._logger.warn("Could not parse java file %s. Invalid syntax" % file)


    def analyse(self, ignoredPathSegments):
        for data in self._data:
            path = data[0]
            type_name = data[1]
            methods = data[2]
            analysed_methods = []
            for method in methods:
                name = method.name
                body = method.body
                if body:
                    complexity = comp.complexity(body)
                    compMethod = Method(name, complexity)
                    analysed_methods.append(compMethod)
            type_ = Type(path, type_name, analysed_methods)
            self._types.append(type_)

    def write_results(self, outputdir):
        self._write_report(outputdir)

    def _write_report(self, outputdir):
        rows = []
        head = ["Method", "Cognitive Complexity", "Path"]
        for type_ in self._types:
            for method in type_.methods:
                rows.append([method.name, method.complexity, type_.path])
        rows.sort(key=lambda x: x[1], reverse=True)
        rows.insert(0,head)
        filepath = os.path.join(
            outputdir, "cognitive_complexity_per_method.xls")
        sheet_name = "Method Complexity"
        xls.write_xls(sheet_name, rows, filepath)
    
    

    def _filter_methods(self, tle):
        return list(filter(lambda type: isinstance(type, ConstructorDeclaration) or isinstance(type, MethodDeclaration), tle))

    def _filter_types(self, content):
        return list(filter(lambda type: isinstance(type, ClassDeclaration) or isinstance(type, InterfaceDeclaration) or isinstance(type, EnumDeclaration), content))
