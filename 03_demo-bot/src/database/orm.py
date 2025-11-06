import pandas as pd
import pandas.io.sql as psql
from sqlalchemy import create_engine, MetaData, inspect, text, Table
from sqlalchemy import Column, Integer, String, Numeric, ARRAY
from sqlalchemy.engine.url import URL
from time import sleep

class SQLConnector(object):
    """ORM for connect to remote SQL servers"""

    def __init__(self, drivername, username, password, host, database, port, attempts=20):
        db_url = {
            'drivername': drivername,
            'username': username,
            'password': password,
            'host': host,
            'port': port,
            'database': database,}
        self._url = URL.create(**db_url)
        self._engine = create_engine(self._url)
        self._attempts = attempts

    def request(self, filename, conditions=None, attempts=None):
        with open(filename, "r") as f:
            query = f.read()
        if type(conditions) is dict:
            query.format(**conditions)
        if type(conditions) is str:
            query.format(conditions)
        return self.get_table(query, attempts=attempts)
    
    def get_table(self, query, attempts=None):
        for at in range((self._attempts if attempts is None else attempts)-1):
            try:
                return pd.read_sql_query(text(query), self._engine)
            except:
                print(f'bad_connection: {at}')
                sleep(3)
        return pd.read_sql_query(text(query), self._engine)
            
    def delete_table(self, schema, name, verbose=True):
        m = MetaData()
        table = Table(name, m, schema=schema)
        table.drop(self._engine)
        inspector = inspect(self._engine)
        if verbose:
            print(name not in inspector.get_table_names(schema=schema))
                
    def upload_dataframe(self, schema, table, df, if_exists='fail'):
        assert (if_exists=='fail') or (if_exists=='replace') or (if_exists=='append')
        df.to_sql(table, self._engine, schema=schema, if_exists=if_exists)
        
    def execute(self, query):
        with self._engine.connect() as conn:
            conn.execute(query)
            