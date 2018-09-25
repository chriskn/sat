#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analysis.analysis import Analysis
import subprocess, re, plot
import pandas as pd
import os.path

class Change():

    def __init__(self, linesAdded, linesRemoved, fileName):
        self.linesAdded = linesAdded
        self.linesRemoved = linesRemoved
        self.fileName = fileName

class GitChanges(Analysis):

    LINES_CHANGED_PATTERN = re.compile(r"\d+\t\d+\t*")
    changes = []
    changesPerFile = []

    def getName(self):
        return "gitChanges"
    
    def getDescription(self):
        pass

    def loadData(self, workingDir, ignoredPathSegments):
        self._workingDir = workingDir
        result = subprocess.run('git log --numstat --oneline --shortstat --after="2017-26-09" -- '+workingDir, stdout=subprocess.PIPE, cwd=workingDir, shell=True) 
        lines = result.stdout.splitlines()
        i = 0
        for line in lines:
            decoded = line.decode('utf-8')
            if self.LINES_CHANGED_PATTERN.match(decoded):
                split = decoded.split("\t")
                self.changes.append(Change(int(split[0]), int(split[1]), split[2]))
                i+=1
            if i > 20:
                return

    def analyse(self, ignoredPathSegments):     
        fileNames = set([change.fileName for change in self.changes])
        for fileName in fileNames:
            linesAdded = 0
            linesRemoved = 0
            for change in self.changes:
                if change.fileName == fileName:
                    linesAdded += change.linesAdded
                    linesRemoved += change.linesRemoved
            self.changesPerFile.append(Change(linesAdded, linesRemoved, fileName))
        self.changesPerFile[:] = [change for change in self.changesPerFile if os.path.isfile(os.path.join(self._workingDir,change.fileName))]
        self.changesPerFile.sort(key=lambda c: c.linesAdded+c.linesRemoved, reverse=True)

    def writeResults(self, outputDir):
        fileNames = [change.fileName for change in self.changesPerFile]
        data = []
        for change in self.changesPerFile[0:20]:
            data.append([change.linesAdded, change.linesRemoved])
        df = pd.DataFrame(data=data, index=fileNames[0:20], columns=["Added","Removed"])
        plot.plotStackedBarChart(df, "Number of changed lines", outputDir, "changes.pdf")

