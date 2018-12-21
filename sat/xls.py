#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlwt

def write_xls(sheet_name, rows, filepath):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)
    for row_idx, row in enumerate(rows):
        _write_row(ws, row_idx, row)
    wb.save(filepath)


def _write_row(sheet, row_idx, row):
    for cell_idx, cell in enumerate(row):
        sheet.write(row_idx, cell_idx, str(cell))
