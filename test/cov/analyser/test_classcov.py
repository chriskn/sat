import os

import unittest
from sat.cov.analyser.classcov import ClassCov


class ClassCovTest(unittest.TestCase):
    def test_class_cov(self):
        # work in progress
        # pylint: disable=R0201
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_testdata = os.path.join(cur_dir, "testdata", "coverage.csv")
        sut = ClassCov(path_to_testdata)
        sut.load_data("exampleProjects", [])
        sut.analyse([])
        sut.write_results(os.path.join(path_to_testdata[:-1], "classcov_out.pdf"))
