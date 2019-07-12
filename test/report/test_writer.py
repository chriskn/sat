#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import mock
from mock import Mock
from mock import mock_open
import sat.app.report.writer as sut

# no self use
# pylint: disable=R0201


class TestWriter(unittest.TestCase):
    @mock.patch("pandas.ExcelWriter")
    def test_write_dataframe_to_xls_writes_to_given_path(self, mock_writer_factory):
        mock_data = Mock()
        exp_filename = "dummyFileName"
        exp_out_dir = os.path.join("dummy", "path")
        exp_path = os.path.join(exp_out_dir, exp_filename)

        sut.write_dataframe_to_xls(mock_data, exp_filename, exp_out_dir, "")

        mock_writer_factory.assert_called_with(exp_path)

    @mock.patch("pandas.ExcelWriter")
    def test_write_dataframe_to_xls_writes_expected_data(self, mock_writer_factory):
        mock_data = Mock()
        mock_writer = Mock()
        exp_sheetname = "My Dummy Sheet"
        mock_writer_factory.return_value = mock_writer

        sut.write_dataframe_to_xls(mock_data, "", "", exp_sheetname)

        mock_data.to_excel.assert_called_with(mock_writer, exp_sheetname, index=False)

    @mock.patch("pandas.ExcelWriter")
    def test_write_dataframe_to_xls_saves_xls(self, mock_writer_factory):
        mock_data = Mock()
        mock_writer = Mock()
        mock_writer_factory.return_value = mock_writer

        sut.write_dataframe_to_xls(mock_data, "", "", "")

        self.assertTrue(mock_writer.save.called)

    @mock.patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_write_graphml_writes_graphml(self, open_mock):
        graph_mock = Mock()
        exp_path = "dummypath"
        exp_graph_content = "foobar"
        graph_mock.serialize.return_value = exp_graph_content
        sut.write_graphml(exp_path, graph_mock)

        open_mock.assert_called_once_with(exp_path, "w")
        handle = open_mock()
        handle.write.assert_called_once_with(exp_graph_content)

    @mock.patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_write_cycles_to_txt_writes_cycles(self, open_mock):
        exp_path = "dummypath"
        input_cycles = [["4", "5"], ["a", "b", "3"], ["1", "2"]]
        sut.write_cycles_to_txt(exp_path, input_cycles)

        open_mock.assert_called_once_with(exp_path, "w")
        handle = open_mock()
        self.assertEqual(
            [mock.call("4, 5\n"), mock.call("3, a, b\n"), mock.call("1, 2\n")],
            handle.write.mock_calls,
        )
