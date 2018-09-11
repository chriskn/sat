#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project.projectparser import ProjectParser
import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns 
sns.set()


class ProjectAnalyser:

    _projects = None

    def analyse(self, workingDir, ignoredPathSegments): 
        print("Analysing projects...") 
        parser = ProjectParser(workingDir, ignoredPathSegments)
        projects = parser.parseProjects()
        self._projects = projects
        print("Analysed %d projects" %len(projects)) 
    
    def writeResults(self, outputFolder):
        self._writePackageCouplingHeatmap(outputFolder)
        self._writeProjectCouplingHeatmap(outputFolder)

    def _writePackageCouplingHeatmap(self,outputFolder):
        print("Creating package coupling heatmap...")
        packages = []
        for p in self._projects:
            packages.extend(p.sourcePackages)
        heatmapFig = self._buildCouplingHeatmap(packages, "Package Coupling")
        heatmapPath = os.path.join(outputFolder,"package_coupling_heatmap.pdf")
        print("Writing coupling heatmap...")
        heatmapFig.savefig(heatmapPath, bbox_inches = 'tight')
        plt.close(heatmapFig)
        print("Wrote coupling heatmap to %s" %heatmapPath)

    def _writeProjectCouplingHeatmap(self, outputFolder):
        print("Creating project coupling heatmap...")
        heatmapFig = self._buildPCouplingHeatmap(self._projects, "Project Coupling")
        heatmapPath = os.path.join(outputFolder,"project_coupling_heatmap.pdf")
        print("Writing coupling heatmap...")
        heatmapFig.savefig(heatmapPath, bbox_inches = 'tight')
        plt.close(heatmapFig)
        print("Wrote coupling heatmap to %s" %heatmapPath)
 
    def _buildCouplingHeatmap(self, packages, title):
        names = [p.name for p in packages]
        data = []
        for package in reversed(packages):
            data.append([package.getImports().count(pName) for pName in names])
        df = pd.DataFrame(data=data, index=list(reversed(names)), columns=names)
        return self._buildHeatMap(df, title)

    def _buildPCouplingHeatmap(self, projects, title):
        names = []
        data = []
        for project in reversed(projects):
            pImports = project.getImports()
            names.append(project.name)
            projData = []
            for oProject in projects:
                projDeps = 0
                for oPackage in oProject.sourcePackages:
                    occurences = pImports.count(oPackage.name)
                    projDeps += occurences
                projData.append(projDeps)    
            data.append(projData)
        df = pd.DataFrame(data=data, index=names, columns=list(reversed(names)))
        return self._buildHeatMap(df, title)
       
    def _buildHeatMap(self, dataFrame, title):
        dpi = 72.27
        fontsize_pt = plt.rcParams['ytick.labelsize']
        numberOfEntries = dataFrame.shape[0]
        twentyPercent = int(round(numberOfEntries * 0.1))
        maxTwentyPercent = sorted(dataFrame.values.flatten())[-twentyPercent:]
        vmax = min(maxTwentyPercent)
        matrix_height_pt = fontsize_pt * numberOfEntries
        matrix_height_in = matrix_height_pt / dpi

        # compute the required figure height 
        entryOffset = +numberOfEntries * 0.2
        figure_height = matrix_height_in + entryOffset

        cmap = plt.get_cmap('autumn_r',10)
        cmap.set_under('white')
        cmap.set_over('black')

        # build the figure instance with the desired height
        fig, ax = plt.subplots(
            figsize=(figure_height,figure_height), 
        )
        ax.set_title(title)
        sns.heatmap(dataFrame, square=True, fmt="d", ax=ax, 
            xticklabels=True, yticklabels=True,
            annot_kws={"size": 8}, annot=True,
            cmap=cmap, vmin=1, vmax=vmax,
            cbar_kws={"shrink": 0.5}, linewidths=0.5, linecolor="grey"
        )#, linewidth=.5, cmap=colorPalette)
        return fig 