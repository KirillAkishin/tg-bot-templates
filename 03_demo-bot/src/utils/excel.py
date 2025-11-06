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

def get_excel_from_db(message):
    cond = 'NULL' if str(message.text) == '' else str(message.text)
    df = db.conn.request('database/request.sql', conditions=cond)
    filename = os.path.join(data_dir, f'table_{cond}.xlsx')
    utils.save_excel(df, filename)
    return open(filename, 'rb')

def get_excel_from_file(message):
    item = message.text.strip('/')
    filename = db.cache[item]
    return open(filename, 'rb')