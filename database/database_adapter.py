from sqlalchemy import create_engine
import pandas as pd

class Database:

    def __init__(self,url,df,table_name):
        self.url = url
        self.df = df 
        self.table_name = table_name
    def _postgresql_connection(self): 
        return create_engine(self.url)
    def _execute_sql(self):
        self.df.to_sql(
            name = self.table_name, 
            con = self._postgresql_connection(), 
            if_exists = 'replace',
            index = False 
        )
        print(f"Successful! {len(self.df)} has been writtein into {self.table_name} table.")
    def drop_table_databse(self):
        pass
    def generate_sql_table(self): 
        self._postgresql_connection()
        self._execute_sql()
    
    

    

