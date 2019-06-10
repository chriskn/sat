import os
import unittest

import mock

import sat.deps.parser.packageparser as sut
from sat.deps.domain import SourceFile


class PackageParserTest(unittest.TestCase):
    def test_parse_packages_returns_empty_list_if_sourcefolders_are_empty(self):
        self.assertEqual(sut.parse_packages([]), [])

    @mock.patch("os.walk")
    def test_parse_packages_returns_empty_list_if_no_sourcefiles_are_found(
        self, walker_mock
    ):
        walker_mock.return_value = [("", [], [])]

        self.assertEqual(sut.parse_packages([""]), [])

    @mock.patch("os.walk")
    def test_parse_packages_analyses_given_sourcefolders(self, walker_mock):
        source_folders = ["a", "b", "c"]

        walker_mock.return_value = [("", [], [])]

        self.assertEqual(sut.parse_packages(source_folders), [])
        walker_mock.assert_any_call(source_folders[0])
        walker_mock.assert_any_call(source_folders[1])
        walker_mock.assert_any_call(source_folders[2])
        assert len(source_folders) == walker_mock.call_count

    @mock.patch("sat.deps.repo.sourcerepo.sourcefiles")
    @mock.patch("os.walk")
    def test_parse_packages_parses_expected_path(self, walker_mock, source_repo_mock):
        # disable no self use
        # pylint: disable = R0201
        java_filenames = ["AbstractDummy.java", "IDummy.java"]
        package_path = os.sep.join(["exampleprojects", "dummy.project1", "src"])
        walker_mock.return_value = [(package_path, [], java_filenames)]
        source_repo_mock.return_value = []

        sut.parse_packages(["exampleprojects"])

        source_repo_mock.assert_called_once_with(
            java_filenames, package_path, "dummy.project1.src"
        )

    @mock.patch("sat.deps.repo.sourcerepo.sourcefiles")
    @mock.patch("os.walk")
    def test_parse_packages_returns_expected_packages(
        self, walker_mock, source_repo_mock
    ):
        java_filenames = ["AbstractDummy.java", "IDummy.java"]
        package_path = os.sep.join(["exampleprojects", "dummy.project1", "src"])
        source_file = SourceFile("DummyFile", "java", [], [], [], [], [])
        walker_mock.return_value = [(package_path, [], java_filenames)]
        source_repo_mock.return_value = [source_file]

        result_packages = sut.parse_packages(["exampleprojects"])

        assert len(result_packages) == 1
        self.assertEqual(result_packages[0].name, "dummy.project1.src")
        self.assertEqual(result_packages[0].path, package_path)
        self.assertEqual(result_packages[0].sourcefiles, [source_file])
