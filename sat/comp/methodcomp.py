#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
import scanner
import javalang
import comp.compcalculator as comp
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration

class MethodComp(Analysis):

    @staticmethod
    def name():
        return "methods"

        # non_empty_lines = [
        # line for line in file_content.splitlines() if line.strip()]
        #loc = len(non_empty_lines)

    def load_data(self, workingdir, ignored_path_segments):
        files = scanner.find_java_source_files(
            workingdir, ignored_path_segments)
        self._file_contents = []
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                self._file_contents.append(file_content)
                ast = javalang.parse.parse(file_content)
                types = ast.types
                for t in types:
                    methods = self._filter_methods(t.body)
                    for method in methods:
                        body = method.body
                        name = method.name
                        if body:
                            compl = comp.complexitivity(body)
                            print(name+" : "+str(compl))

    def analyse(self, ignoredPathSegments):
        pass
        #self._logger.info("Analysing lines of code per file.")
        # for source in self._file_contents:
        # self._methods(source)

    def _filter_methods(self, class_):
        return list(filter(lambda type: isinstance(type, ConstructorDeclaration) or isinstance(type, MethodDeclaration), class_))

    def write_results(self, outputdir):
        pass

    def _write_report(self, outputdir):
        pass
