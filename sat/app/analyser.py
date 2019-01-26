
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
    def load_data(self, workingdir, ignoredpathsegments):
        pass

    @abstractmethod
    def analyse(self, ignoredpathsegments):
        pass

    @abstractmethod
    def write_results(self, outputfolder):
        pass
