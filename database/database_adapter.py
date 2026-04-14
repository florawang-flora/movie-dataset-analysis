from sqlalchemy import create_engine
import pandas as pd

class Database:

    def __init__(self,url,df,table_name):
        self.url = url
        self.df = df 
        self.table_name = table_name
    def _create_engine(self): 
        return create_engine(self.url)
    def execute_sql(self):
        self.df.to_sql(
            name = self.table_name, 
            con = self._create_engine(), 
            if_exists = 'replace',
            index = False 
        )
        print(f"Successful! {len(self.df)} has been writtein into {self.table_name} table.")
   
    

    

