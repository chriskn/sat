#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import mock
from mock import Mock

import sat.report.xls as sut

# no self use
# pylint: disable=R0201


class TestXls(unittest.TestCase):
    @mock.patch("pandas.ExcelWriter")
    def test_write_data_frame_writes_to_given_path(self, mock_writer_factory):
        mock_data = Mock()
        exp_filename = "dummyFileName"
        exp_out_dir = os.path.join("dummy", "path")
        exp_path = os.path.join(exp_out_dir, exp_filename)

        sut.write_data_frame(mock_data, exp_filename, exp_out_dir, "")

        mock_writer_factory.assert_called_with(exp_path)

    @mock.patch("pandas.ExcelWriter")
    def test_write_data_frame_writes_expected_data(self, mock_writer_factory):
        mock_data = Mock()
        mock_writer = Mock()
        exp_sheetname = "My Dummy Sheet"
        mock_writer_factory.return_value = mock_writer

        sut.write_data_frame(mock_data, "", "", exp_sheetname)

        mock_data.to_excel.assert_called_with(mock_writer, exp_sheetname, index=False)

    @mock.patch("pandas.ExcelWriter")
    def test_write_data_frame_saves_xls(self, mock_writer_factory):
        mock_data = Mock()
        mock_writer = Mock()
        mock_writer_factory.return_value = mock_writer

        sut.write_data_frame(mock_data, "", "", "")

        self.assertTrue(mock_writer.save.called)
