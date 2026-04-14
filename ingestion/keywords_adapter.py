import pandas as pd
import ast  
from ingestion.base_adapter import BaseAdapter
from tools.utils import Utils
class KeywordsAdapter(BaseAdapter):
        
                
        # flatten data column have problem rn.       
        def flatten_data(self):

                """
                This method is to flatten keywords data for the specific data frame. 
                step1: change the nested str ][ing format to the list format.
                step2: explode the data. 
                step3: take the keynames out to form the keywords.df
                """
                # step1: change the nested string format to the list format.
      
                self.df["keywords_list"] = self.df['keywords'].apply(Utils.parse)
                # retrun a dataframe
                keywords_df = self.df[['id', 'keywords_list']].explode('keywords_list')
                #print(keywords_df['keywords_list'].apply(type).value_counts())
                #print(keywords_df['keywords_list'].head(10))
                # check whether we have NaN data for the name data. otherwise, we can't extract the name column.
                keywords_df.dropna(subset = ['keywords_list'])
                # check keywords_list has how many types
                #print('yoyoyyo',keywords_df['keywords_list'].apply(type).value_counts())
                #print(keywords_df.loc[keywords_df['keywords_list'].apply(lambda x:  isinstance(x,float)), 'keywords_list'].head(30))

                keywords_df['keywords_list'] = keywords_df['keywords_list'].apply(lambda x : x['name'] if isinstance(x,dict) and 'name' in x else None)
                self.df = keywords_df[['id', 'keywords_list']].rename(
                        columns ={
                                'id': 'tmdb_id',
                                'keywords_list': 'keywords'
                        }
                )
                print(f'Here is {self.filename} file datatype information :/n {self.df.info()}')
                print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')

                return self.df 
                


