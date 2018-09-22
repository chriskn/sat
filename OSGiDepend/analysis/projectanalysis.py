#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
from project.projectgraph import ProjectGraph 
from analysis.analysis import Analysis
import numpy as np
import pandas as pd
import os, plot, logging

class ProjectAnalyser(Analysis):

    def getName(self):
        return "javaProjectDeps"
    
    def getDescription(self):
        return "Analysis plain java dependiencies for projects (based on classpath files)"

    def loadData(self, workingDir,ignoredPathSegments):
        self.logger.info("Loading project data...") 
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parseProjects()
        self._projects = projects

    def analyse(self, ignoredPathSegments): 
        self.logger.info("Creating project coupling graph")
        projectGraph = ProjectGraph(self._projects)
        self.logger.info("Analysing project cycles")
        cycles = projectGraph.getCycles()
        projectGraph.markCycles(cycles)
        self._projectGraph = projectGraph
        self._cycleProjectGraph =  projectGraph.getCycleGraph(cycles)
        self.logger.info("Creating project coupling map")
        self._projectCouplingMap = self._createProjectCouplingDataFrame(self._projects)
        self.logger.info("Analysed %d projects" %len(self._projects)) 

    def writeResults(self, outputDir):
        self.logger.info("Writing project analysis results")
        plot.plotHeatmap(self._projectCouplingMap, "Project Coupling", outputDir, "project_coupling_heatmap.pdf")
        self._writeGraphToGraphMl(os.path.join(outputDir,"project_dependencies.graphml"), self._projectGraph)
        self._writeGraphToGraphMl(os.path.join(outputDir,"cyclic_project_dependencies.graphml"), self._cycleProjectGraph)

    def _createProjectCouplingDataFrame(self, projects):
        pNames = []
        data = []
        for project in reversed(projects):
            pImports = project.getImports()
            pNames.append(project.name)
            projData = []
            for oProject in projects:
                projDeps = 0
                for oPackage in oProject.sourcePackages:
                    occurences = pImports.count(oPackage.name)
                    projDeps += occurences
                projData.append(projDeps)    
            data.append(projData)
        return pd.DataFrame(data=data, index=pNames, columns=list(reversed(pNames)))

    def _writeGraphToGraphMl(self, path, graph):
        with open(path, 'w') as outputFile:
            outputFile.write(graph.serialize())