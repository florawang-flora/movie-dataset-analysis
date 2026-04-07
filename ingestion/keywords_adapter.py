import pandas as pd
import ast  
from ingestion.base_adapter import BaseAdapter
class KeywordsAdapter(BaseAdapter):
        def load_data(self):
                '''
                This method is to load the data from the csv 
                '''
                self.files = pd.read_csv(self.path)
                return self.files 
        def clean_data(self): 
                """
                This method is check whether we have the dulicate data in the data frame. 
                """
                self.check_data_dulplicates()
                self.clean_data_dulplicates()
                self.flatten_data()
                     
        def check_data_dulplicates(self): 
                """
                This method is check whether we have the dulicate data in the data frame. 
                """
                check_dulpliciated_rows = self.files.duplicated().sum()
                if check_dulpliciated_rows >= 0:
                        print(f'There are {check_dulpliciated_rows} duplicate rows in the data frame.')
                        print('Going to clean the data')
                else:
                        print('data is tidy')
                        row, column = self.files.shape
                        print(f'There are {row} rows and {column} columns in the data frame.')
                return check_dulpliciated_rows
                 
        def clean_data_dulplicates(self):
                """
                This method is to clean the dulplicate data in the data frame. 
                """
                
                clean_raw_files = self.files.drop_duplicates()
                print(f'Before: thre are {self.files.shape[0]} rows and {self.files.shape[1]} columns in the data frame.')
                print(f'After: thre are {clean_raw_files.shape[0]} rows and {clean_raw_files.shape[1]} columns in the data frame.')
                self.df = clean_raw_files 
                return self.df
                
        # flatten data column have problem rn.       
        def flatten_data(self):
                # columns = clean_raw_files' column
                """
                This method is to flatten the data for the specific data frame. 
                """
                # clean the keywords column
                keywords = self.df['keywords']
                if isinstance(keywords, str):
                        keywords_list = ast.literal_eval(keywords)
                else:
                        keywords_list = []
        
                keywords_explode = self.df[['id', 'keywords_list']].explode('keywords_list')
                keywords_explode = keywords_explode.dropna(subset = ['keywords_list'])
                keywords_explode['keywords_list'] = keywords_explode['keywords_list'].apply(
                        lambda x: x[['name']]
                )
                self.df = keywords_explode[['id', 'keywords_list']].rename(
                        columns = {
                                'id' : 'tmdb_id',
                                'keywords_list': 'keywords'
                        }
                )
                print(self.df.head())
                return self.df                
        

        def process(self):
                '''
                This process to define the the process for the keywords adaptor.
                '''
                self.load_data()
                self.check_data_dulplicates()
                self.clean_data_dulplicates()
                self.flatten_data()
                return self.df
        

