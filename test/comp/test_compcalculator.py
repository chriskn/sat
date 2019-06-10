#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import javalang
from javalang.tree import ConstructorDeclaration, MethodDeclaration

import sat.comp.compcalculator as sut

_PATH_TO_TEST_DATA = os.path.join("data", "ComplDummy.java")
_METHODS_BY_NAME = dict()


class TestComplCalulator(unittest.TestCase):
    @classmethod
    def _filter_methods(cls, class_):
        return list(
            filter(
                lambda type: isinstance(type, ConstructorDeclaration)
                or isinstance(type, MethodDeclaration),
                class_,
            )
        )

    @classmethod
    def setUpClass(cls):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        testfile = os.path.join(cur_dir, _PATH_TO_TEST_DATA)
        with open(testfile, "r", encoding="utf-8") as input_file:
            file_content = input_file.read()
            ast = javalang.parse.parse(file_content)
            classes = getattr(ast, "types")
            for class_ in classes:
                methods = TestComplCalulator._filter_methods(class_.body)
                for method in methods:
                    _METHODS_BY_NAME[method.name] = method.body

    def test_compl_for_compl_example1(self):
        method = _METHODS_BY_NAME.get("complExample1")
        self.assertEqual(sut.complexity(method), 20)

    def test_compl_for_compl_example2(self):
        method = _METHODS_BY_NAME.get("complExample2")
        self.assertEqual(sut.complexity(method), 35)

    def test_compl_for_compl_example3(self):
        method = _METHODS_BY_NAME.get("complExample3")
        self.assertEqual(sut.complexity(method), 19)

    def test_compl_for_compl_example4(self):
        method = _METHODS_BY_NAME.get("complExample4")
        self.assertEqual(sut.complexity(method), 96)

    def test_compl_for_switch_example(self):
        method = _METHODS_BY_NAME.get("switchExample")
        self.assertEqual(sut.complexity(method), 1)

    def test_compl_for_if_in_loops(self):
        method = _METHODS_BY_NAME.get("ifInLoops")
        self.assertEqual(sut.complexity(method), 6)

    def test_compl_for_if_elseif_example(self):
        method = _METHODS_BY_NAME.get("ifElseifExample")
        self.assertEqual(sut.complexity(method), 5)

    def test_compl_for_do_while(self):
        method = _METHODS_BY_NAME.get("doWhileExample")
        self.assertEqual(sut.complexity(method), 3)


if __name__ == "__main__":
    unittest.main()
