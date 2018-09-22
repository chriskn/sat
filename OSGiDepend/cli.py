#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, os
from argparse import RawTextHelpFormatter

defaultIgnoredPathSegments = ["bin", "target", "examples", "test"]
version = '%(prog)s 0.1.0'
ignoredPathSegments = []

class Cli:
    
    parser = None
    
    def __init__(self, analysers):
        self.parser =  argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
        analysersNames = [analyser.getName() for analyser in analysers]
        requiredNamed = self.parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('-a', dest='analysers', choices=analysersNames,  nargs='+', required=True, help='List of analysis to run')
        self.parser.add_argument('-w', dest='workingDir', default=os.getcwd(), help='Root folder for recursive analysis. Default is script location')
        self.parser.add_argument('-i', dest='ignoredPathSegments', default=defaultIgnoredPathSegments, nargs='*' ,
            help="List of ignored path segements. Default is "+", ".join(defaultIgnoredPathSegments)+". Provide empty list to include all paths"
        )
        self.parser.add_argument('-v','--version', action='version', version=version)

    def parse(self):
        args = self.parser.parse_args() 
        return args.workingDir, args.ignoredPathSegments, args.analysers