import os
import openpyxl as xl
import pandas as pd

def save_excel(df, filename, index=False):
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(filename):
        os.remove(filename)
    wb = xl.Workbook()
    wb.save(file_name)
    with pd.ExcelWriter(filename, datetime_format='DD-MM-YYYY') as wr:
        df.to_excel(wr, sheet_name='main_sheet', index=index)
