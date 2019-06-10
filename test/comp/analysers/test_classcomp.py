#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import ANY
import mock

from sat.comp.analyser.classcomp import ClassComp
from sat.comp.domain import Method, Type

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


class TestClassComp(unittest.TestCase):
    def setUp(self):
        self.sut = ClassComp()

    @mock.patch("sat.comp.repo.typerepo.types")
    def test_load_data_calls_typerepo(self, types_mock_repo):
        wdir = "dummy/dir"
        ignored = "foo.bar"
        self.sut.load_data(wdir, ignored)
        types_mock_repo.assert_called_with(wdir, ignored)

    def test_name_is_methods(self):
        self.assertEqual(ClassComp.name(), "classes")

    @mock.patch("sat.comp.repo.typerepo.types")
    def test_analyse_creates_expected_dataframe(self, mock_type_repo):
        mock_type_repo.return_value = _TYPES
        self.sut.load_data("", "")
        result = self.sut.analyse("")
        complexity = list(result["Complexity"])
        classes = list(result["Class"])
        paths = list(result["Path"])
        methods = list(result["Methods with complexity > 0"])
        self.assertEqual(complexity, [500, 25, 14, 0])
        self.assertEqual(classes, ["dummy3", "dummy1", "dummy2", "dummy4"])
        self.assertEqual(
            paths, ["dummy3/path", "dummy1/path", "dummy2/path", "dummy4/path"]
        )
        self.assertEqual(
            methods,
            [
                "dummy3Method2:500",
                "dummy1Method2:15, dummy1Method1:10",
                "dummy2Method2:9, dummy2Method1:5",
                "",
            ],
        )
        self.assertEqual(len(result.columns), 4, "Columns with unexpected lengths.")

    @mock.patch("sat.report.plot.plot_barchart")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.typerepo.types")
    def test_write_results_calls_write_data_frame(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param because mock avoids error
        # pylint: disable=W0613
        mock_type_repo.return_value = []
        self.sut.load_data("", "")
        self.sut.analyse("")
        odir = "result\\dir"
        self.sut.write_results(odir)
        write_xls.assert_called_with(
            ANY, "cognitive_complexity_per_class.xls", odir, "Class Complexity"
        )

    @mock.patch("sat.report.plot.plot_barchart")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.typerepo.types")
    def test_write_results_calls_plot_barchart(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param because mock avoids error
        # pylint: disable=W0613
        mock_type_repo.return_value = []
        self.sut.load_data("", "")
        odir = "result\\dir"
        self.sut.analyse("")
        self.sut.write_results(odir)
        plot_barchart.assert_called_with(
            ANY,
            "Cognitive complexity",
            "Classes with highest cognitive complexity",
            odir,
            "most_complex_classes.pdf",
        )

    @mock.patch("sat.report.plot.plot_barchart")
    @mock.patch("sat.report.xls.write_data_frame")
    @mock.patch("sat.comp.repo.typerepo.types")
    def test_write_results_plots_expected_data(
        self, mock_type_repo, write_xls, plot_barchart
    ):
        # disable unused param because mock avoids error
        # pylint: disable=W0613
        mock_type_repo.return_value = _TYPES
        self.sut.load_data("", "")
        self.sut.analyse("")
        self.sut.write_results("")
        args, _ = plot_barchart.call_args
        used_data = args[0]
        complexity = list(used_data["Complexity"])
        classes = list(used_data["Class"])
        # Ignores classes without complexity
        self.assertEqual(complexity, [500, 25, 14])
        self.assertEqual(classes, ["dummy3", "dummy1", "dummy2"])
        self.assertEqual(len(used_data.columns), 2, "Columns with unexpected lengths.")


if __name__ == "__main__":
    unittest.main()
