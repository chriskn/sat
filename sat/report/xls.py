#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pandas as pd


def write_data_frame(data, filename, outputdir, sheetname):
    filepath = os.path.join(outputdir, filename)
    writer = pd.ExcelWriter(filepath)
    data.to_excel(writer, sheetname, index=False)
    writer.save()
