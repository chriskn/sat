#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

import sat.app.report.plot as plot
import sat.app.report.writer as writer

from sat.app.execution.analyser import Analyser
from sat.comp.domain import TopLevelType

_COLUMNS = [
    "Package",
    "Complexity",
    "Number of statements",
    "Number of classes",
    "Number of abstract classes",
    "Number of interfaces",
    "Number of enums",
    "Number of types",
    "Number of methods",
    "Average complexity by class",
    "Average complexity by method",
    "Project",
    "Path",
]


class PackageComp(Analyser):
    @staticmethod
    def name():
        return "packages"

    def __init__(self, workspace):
        Analyser.__init__(self, workspace)
        self._packages = None
        self._analysis_result = None

    def load_data(self):
        self._packages = self._workspace.packages()

    def analyse(self):
        self._logger.info("Analysing Package Complexity.")
        data = []
        for package in self._packages:
            num_types = len(package.types)
            num_classes = len(
                list(filter(lambda p: p.type == TopLevelType.CLASS, package.types))
            )
            num_abstract_classes = len(
                list(
                    filter(
                        lambda p: p.type == TopLevelType.ABSTRACT_CLASS, package.types
                    )
                )
            )
            num_enums = len(
                list(filter(lambda p: p.type == TopLevelType.ENUM, package.types))
            )
            num_interfaces = len(
                list(filter(lambda p: p.type == TopLevelType.INTERFACE, package.types))
            )
            num_methods = sum([len(type_.methods) for type_ in package.types])
            num_statements = sum(type_.num_statements for type_ in package.types)
            av_method_comp = av_method_comp = (
                package.complexity / num_methods if num_methods else 0
            )
            av_type_comp = av_type_comp = (
                package.complexity / num_types if num_types > 0 else 0
            )
            data.append(
                (
                    package.name,
                    package.complexity,
                    num_statements,
                    num_classes,
                    num_abstract_classes,
                    num_interfaces,
                    num_enums,
                    num_types,
                    num_methods,
                    av_type_comp,
                    av_method_comp,
                    package.proj_name,
                    package.abs_path,
                )
            )
        package_dataframe = pd.DataFrame(data, columns=_COLUMNS).round(2)
        self._analysis_result = package_dataframe.sort_values(
            _COLUMNS[1], ascending=False
        )
        return self._analysis_result

    def write_results(self, output_dir):
        writer.write_dataframe_to_xls(
            self._analysis_result,
            "cognitive_complexity_per_package.xls",
            output_dir,
            "Package Complexity",
        )
        writer.write_dataframe_to_csv(
            self._analysis_result, "cognitive_complexity_per_package.csv", output_dir
        )
        self._plot_treemaps(output_dir)

    def _plot_treemaps(self, output_dir):
        total_comp = self._create_treemap_data(_COLUMNS[1])
        avm_comp = self._create_treemap_data(_COLUMNS[5])
        avt_comp = self._create_treemap_data(_COLUMNS[6])
        plot.plot_treemap(
            total_comp,
            "Cognitive complexity per package",
            output_dir,
            "cognitive_complexity_per_package.pdf",
            "complexity:",
        )
        plot.plot_treemap(
            avm_comp,
            "av method complexity per package",
            output_dir,
            "av_method_complexity_per_package.pdf",
            "avm complexity:",
        )
        plot.plot_treemap(
            avt_comp,
            "av class complexity per package",
            output_dir,
            "av_class_complexity_per_package.pdf",
            "avc complexity:",
        )

    def _create_treemap_data(self, data_column):
        columns_to_drop = list(_COLUMNS)
        columns_to_drop.remove(data_column)
        columns_to_drop.remove(_COLUMNS[0])
        tm_data = self._analysis_result.drop(columns=columns_to_drop)
        return tm_data[tm_data[data_column] > 0]
