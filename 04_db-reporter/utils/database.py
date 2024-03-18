import pandas as pd
import yaml
import pandas.io.sql as psql
from sqlalchemy import create_engine, MetaData, inspect, text, Table
from sqlalchemy import Column, Integer, String, Numeric, ARRAY
from sqlalchemy.engine.url import URL
from time import sleep
    

class DBConn(object):
    """Database adapter"""

    def __init__(self, username, password, host, database, port, n_tries=20):
        db_url = {
            'drivername': 'postgresql',
            'username': username,
            'password': password,
            'host': host,
            'port': port,
            'database': database,}
        self.url = URL(**db_url)
        self.engine = create_engine(self.url)
        self.n_tries = n_tries

    def get_data(self, sql_query, n_tries=None):
        for n_try in range((self.n_tries if n_tries is None else n_tries)-1):
            try:
                return pd.read_sql_query(text(sql_query), self.engine)
            except:
                print(f'bad_connect: {n_try}')
                sleep(3)
        return pd.read_sql_query(text(sql_query), self.engine)
            
    def delete_table(self, schema, name, verbose=True):
        m = MetaData()
        table = Table(name, m, schema=schema)
        table.drop(self.engine)
        inspector = inspect(self.engine)
        if verbose:
            print(name not in inspector.get_table_names(schema=schema))
                
    def upload_dataframe(self, schema, table, df, if_exists='fail'):
        assert (if_exists=='fail') or (if_exists=='replace') or (if_exists=='append')
        df.to_sql(table, self.engine, schema=schema, if_exists=if_exists)
        
    def execute(self, sql_query):
        with self.engine.connect() as connection:
            connection.execute(sql_query)
            
class Conn(DBConn):
    def __init__(self, db_params, n_tries=1):
        DBConn.__init__(self, **db_params)
        self.n_tries = n_tries
     

# conn = {
#     'one': Conn('one', n_tries=1),
#     'two': Conn('two', n_tries=1),
# }            
     
# configs = {
#     'one': {
#         'host' : 'host.one.ru',
#         'password' : 'pass',
#         'port' : '8888',
#         'database' : 'main',
#         'username' : 'reader',},
#     'two': {
#         'host' : 'host.two.ru',
#         'password' : 'pass',
#         'port' : '8888',
#         'database' : 'main',
#         'username' : 'reader',},
# }