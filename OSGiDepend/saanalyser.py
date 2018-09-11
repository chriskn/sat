#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import Cli
from bundle.bundleanalyser import BundleAnalyser
from project.projectanalyser import ProjectAnalyser

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns 
sns.set()

'''
def buildHCouplingHeatmap(packages, title):
    names = [p.name for p in packages]
    data = []
    for package in reversed(packages):
        data.append([package.dependencies.count(pName) for pName in names])
    df = pd.DataFrame(data=data, index=list(reversed(names)), columns=names)
    #colorPalette = sns.color_palette("Blues")
    sns.clustermap(df, annot=True, fmt="d")#, cmap=colorPalette)
    plt.show()
'''
ANALYSERS = [ProjectAnalyser()]

if __name__ == '__main__':
    cli = Cli()
    workingDir, ignoredPathSegments = cli.parse()
    print("Ignoring directory paths containing one of the following strings %s" % ignoredPathSegments)
    print("Using directory %s as working directory" % workingDir)
    for analyser in ANALYSERS: 
        analyser.analyse(workingDir, ignoredPathSegments)    
    for analyser in ANALYSERS: analyser.writeResults(workingDir)    
