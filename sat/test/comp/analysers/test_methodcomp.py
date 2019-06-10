#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from comp.domain import Method, Type
from comp.analyser.methodcomp import MethodComp
from unittest.mock import ANY

_TYPES = [
    Type(
        "dummy1/path",
        "dummy1",
        [Method("dummy1Method1", 10), Method("dummy1Method2", 15)],
    ),
    Type(
        "dummy2/path",
        "dummy2",
        [Method("dummy2Method1", 5), Method("dummy2Method2", 9)],
    ),
    Type(
        "dummy3/path",
        "dummy3",
        [Method("dummy3Method1", 0), Method("dummy3Method2", 500)],
    ),
    Type("dummy4/path", "dummy4", []),
]


class TestMethodComp(unittest.TestCase):
    def setUp(self):
        self.sut = MethodComp()

    @mock.patch("comp.repo.typerepo.types")
    def test_load_data_calls_typerepo(self, types_mock_repo):
        wdir = "dummy/dir"
        ignored = "foo.bar"
        self.sut.load_data(wdir, ignored)
        types_mock_repo.assert_called_with(wdir, ignored)

    def test_name_is_methods(self):
        self.assertEqual(MethodComp.name(), "methods")

    @mock.patch("comp.repo.typerepo.types")
    def test_analyse_creates_expected_dataframe(self, mock_type_repo):
        mock_type_repo.return_value = _TYPES
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        complexity = list(result["Complexity"])
        methods = list(result["Method"])
        path = list(result["Path"])
        self.assertEqual(complexity, [500, 15, 10, 9, 5, 0])
        self.assertEqual(
            methods,
            [
                "dummy3Method2",
                "dummy1Method2",
                "dummy1Method1",
                "dummy2Method2",
                "dummy2Method1",
                "dummy3Method1",
            ],
        )
        self.assertEqual(
            path,
            [
                "dummy3/path",
                "dummy1/path",
                "dummy1/path",
                "dummy2/path",
                "dummy2/path",
                "dummy3/path",
            ],
        )
        self.assertEqual(len(result.columns), 3, "Columns with unexpected lengths.")

    @mock.patch("report.plot.plot_barchart")
    @mock.patch("report.xls.write_data_frame")
    @mock.patch("comp.repo.typerepo.types")
    def test_write_results_calls_write_data_frame(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_type_repo.return_value = []
        self.sut.load_data("", "")
        self.sut.analyse("")
        odir = "result\\dir"
        self.sut.write_results(odir)
        write_xls.assert_called_with(
            ANY, "cognitive_complexity_per_method.xls", odir, "Method Complexity"
        )

    @mock.patch("report.plot.plot_barchart")
    @mock.patch("report.xls.write_data_frame")
    @mock.patch("comp.repo.typerepo.types")
    def test_write_results_calls_plot_barchart(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_type_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        plot_barchart.assert_called_with(
            ANY,
            "Cognitive complexity",
            "Methods with highest cognitive complexity",
            odir,
            "most_complex_methods.pdf",
        )

    @mock.patch("report.plot.plot_barchart")
    @mock.patch("report.xls.write_data_frame")
    @mock.patch("comp.repo.typerepo.types")
    def test_write_results_plots_expected_data(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param. only mocked to avoid error
        # pylint: disable=W0613
        mock_type_repo.return_value = _TYPES
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        args, _ = plot_barchart.call_args
        used_data = args[0]
        complexity = list(used_data["Complexity"])
        methods = list(used_data["Method"])
        # Ignores methods without complexity
        self.assertEqual(complexity, [500, 15, 10, 9, 5])
        self.assertEqual(
            methods,
            [
                "dummy3Method2",
                "dummy1Method2",
                "dummy1Method1",
                "dummy2Method2",
                "dummy2Method1",
            ],
        )
        self.assertEqual(len(used_data.columns), 2, "Columns with unexpected lengths.")


if __name__ == "__main__":
    unittest.main()
