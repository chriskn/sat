#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import javalang
import comp.typeparser as sut

class TypeParserTest(unittest.TestCase):


    @mock.patch("java.parse")
    def test_parser_returns_empty_list_for_none_ast(self, java_parser):
        java_parser.return_value = None
        result = sut.parse("")
        self.assertEqual(len(result), 0)

    @mock.patch("java.parse")
    def test_parser_returns_class(self, java_parser):
        input_ast = javalang.parse.parse("package dummy; class Test {}")
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")

    @mock.patch("java.parse")
    def test_parser_returns_enum(self, java_parser):
        input_ast = javalang.parse.parse("package dummy; enum Test {}")
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")
    
    @mock.patch("java.parse")
    def test_parser_returns_interface(self, java_parser):
        input_ast = javalang.parse.parse("package dummy; interface Test {}")
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test")

    @mock.patch("java.parse")
    def test_parser_returns_nested_types(self, java_parser):
        input_ast = javalang.parse.parse("""package dummy; 
            class Class {
                class IClass {
                    enum IIEnum {
            }}}""")
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Class")
        self.assertEqual(result[1].name, "IClass")
        self.assertEqual(result[2].name, "IIEnum")

    @mock.patch("java.parse")
    def test_parser_returns_private_classes(self, java_parser):
        input_ast = javalang.parse.parse("""package dummy; 
            private class pClass1 {}
            private class pClass2 {}
            class Class {}
        """)
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "pClass1")
        self.assertEqual(result[1].name, "pClass2")
        self.assertEqual(result[2].name, "Class")

    @mock.patch("java.parse")
    def test_parser_parses_empty_methods(self, java_parser):
        input_ast = javalang.parse.parse("""package dummy; 
            class Class {
                private static void staticFoo(){}
                private void foo(){}
            }
        """)
        java_parser.return_value = input_ast
        result = sut.parse("")
        self.assertEqual(len(result), 1)
        methods = result[0].methods
        self.assertEqual(methods[0].name, "staticFoo")
        self.assertEqual(methods[1].name, "foo")