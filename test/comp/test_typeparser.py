#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import javalang

import sat.comp.parser.typeparser as sut
from sat.app.workspace.domain import SourceFile


class TypeParserTest(unittest.TestCase):
    def test_parser_returns_empty_list_for_none_ast(self):
        result = sut.parse(SourceFile("", "", "", [], ""))
        self.assertEqual(len(result), 0)

    def test_parser_returns_class(self):
        input_ast = javalang.parse.parse("package dummy; class Test {}")
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")

    def test_parser_returns_enum(self):
        input_ast = javalang.parse.parse("package dummy; enum Test {}")
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")

    def test_parser_returns_interface(self):
        input_ast = javalang.parse.parse("package dummy; interface Test {}")
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")

    def test_parser_returns_nested_types(self):
        input_ast = javalang.parse.parse(
            """package dummy;
            class Class {
                class IClass {
                    enum IIEnum {
            }}}"""
        )
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Class")
        self.assertEqual(result[1].name, "IClass")
        self.assertEqual(result[2].name, "IIEnum")

    def test_parser_returns_private_classes(self):
        input_ast = javalang.parse.parse(
            """package dummy;
            private class pClass1 {}
            private class pClass2 {}
            class Class {}
        """
        )
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "pClass1")
        self.assertEqual(result[1].name, "pClass2")
        self.assertEqual(result[2].name, "Class")

    def test_parser_parses_empty_methods(self):
        input_ast = javalang.parse.parse(
            """package dummy;
            class Class {
                private static void staticFoo(){}
                private void foo(){}
            }
        """
        )
        result = sut.parse(SourceFile("", "", "", input_ast, ""))
        self.assertEqual(len(result), 1)
        methods = result[0].methods
        self.assertEqual(methods[0].name, "staticFoo")
        self.assertEqual(methods[1].name, "foo")
