#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, os

defaultIgnoredPathSegments = ["bin", "target", "examples", "test"]
version = '%(prog)s 1.0'
ignoredPathSegments = []

class Cli:
    
    parser = None
    
    def __init__(self):
        self.parser =  argparse.ArgumentParser()
        self.parser.add_argument('-w', dest='workingDir', default=os.getcwd(), help='Root folder for recursive analysis. Default is the script location')
        self.parser.add_argument('-i', dest='ignoredPathSegments', default=defaultIgnoredPathSegments, nargs='*' ,
            help="List of ignored sub path segements of the root location. Default is "+", ".join(defaultIgnoredPathSegments)+". Provide empty list to include all paths"
        )
        self.parser.add_argument('-v','--version', action='version', version=version)

    def parse(self):
        args = self.parser.parse_args() 
        return args.workingDir, args.ignoredPathSegments