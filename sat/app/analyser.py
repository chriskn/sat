#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging


class Analyser(ABC):
    @staticmethod
    @abstractmethod
    def name():
        pass

    @property
    def _logger(self):
        return logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_data(self, working_dir, ignored_path_segments):
        pass

    @abstractmethod
    def analyse(self, ignored_path_segments):
        pass

    @abstractmethod
    def write_results(self, output_dir):
        pass
