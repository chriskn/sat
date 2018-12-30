#!/usr/bin/env python
# -*- coding: utf-8 -*-

from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
import javalang
import comp.compcalculator as sut
import unittest
import os

_TEST_DATA = "test\\comp\\data\\ComplDummy.java"
_METHODS_BY_NAME = dict()


class TestComplCalulator(unittest.TestCase):

    @classmethod
    def _filter_methods(cls, class_):
        return list(filter(
            lambda type: isinstance(type, ConstructorDeclaration)
            or isinstance(type, MethodDeclaration), class_))

    @classmethod
    def setUpClass(cls):
        testfile = os.path.join(os.getcwd(), _TEST_DATA)
        with open(testfile, 'r', encoding='utf-8') as f:
            file_content = f.read()
            ast = javalang.parse.parse(file_content)
            classes = ast.types
            for class_ in classes:
                methods = TestComplCalulator._filter_methods(class_.body)
                for method in methods:
                    _METHODS_BY_NAME[method.name] = method.body

    def test_compl_for_complExample1(self):
        method = _METHODS_BY_NAME.get("complExample1")
        self.assertEqual(sut.complexitivity(method), 20)

    def test_compl_for_complExample2(self):
        method = _METHODS_BY_NAME.get("complExample2")
        self.assertEqual(sut.complexitivity(method), 35)

    def test_compl_for_complExample3(self):
        method = _METHODS_BY_NAME.get("complExample3")
        self.assertEqual(sut.complexitivity(method), 19)

    def test_compl_for_switchExample(self):
        method = _METHODS_BY_NAME.get("switchExample")
        self.assertEqual(sut.complexitivity(method), 1)

    def test_compl_for_ifInLoops(self):
        method = _METHODS_BY_NAME.get("ifInLoops")
        self.assertEqual(sut.complexitivity(method), 6)

    def test_compl_for_ifElseifExample(self):
        method = _METHODS_BY_NAME.get("ifElseifExample")
        self.assertEqual(sut.complexitivity(method), 5)


if __name__ == '__main__':
    unittest.main()
