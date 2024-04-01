import pandas as pd
from prettytable import PrettyTable
from .orm import SQLConnector

class DataFrame:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename, index_col=0)
        
    def write(self):
        return self.df.to_csv(self.filename)
    
    def __str__(self):
        tab = PrettyTable()
        tab.field_names = [self.df.index.name] + list(self.df.columns)
        for row in self.df.iterrows():
            tab.add_row([row[0]] + list(row[1]))
        return '```\n{}```'.format(tab.get_string())

class LocalStorage:
    """Local storage"""
    
    def __init__(self, kwargs):
        for name, filename in kwargs.items():
            setattr(self, name, DataFrame(filename))

class DataBase:
    """DataBase adapter"""
    
    def __init__(self, db_params):
        if 'local' in db_params:
            self.loc = LocalStorage(db_params['local'])
        if 'remotes' in db_params:
            for srv in (db_params['remotes']):
                setattr(self, srv, SQLConnector(**db_params['remotes'][srv]))
                

     
