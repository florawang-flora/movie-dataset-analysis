import pandas as pd
import ast  
from ingestion.base_adapter import BaseAdapter
class GenreAdapter(BaseAdapter):
        # flatten data column have problem rn.       
        def flatten_data(self):
                """
                This method is to flatten genre data for the specific data frame. 
                step1: change the nested string format to the list format.
                step2: explode the data. 
                step3: take the genre out to form the genre.df
                """
                # step1: change the nested string format to the list format.
      
                self.df["genres_list"] = self.df['genres'].apply(self.parse)
                
                # retrun a dataframe
                genres_df = self.df[['id', 'imdb_id','genres_list']].explode('genres_list')
             
                # check whether we have NaN data for the name data. otherwise, we can't extract the name column.
                genres_df.dropna(subset = ['genres_list'])
                # check genre_list has how many types
                
                genres_df['genres_list'] = genres_df['genres_list'].apply(lambda x : x['name'] if isinstance(x,dict) and 'name' in x else None)
                self.df = genres_df[['id', 'imdb_id', 'genres_list']].rename(
                        columns ={
                                'id': 'tmdb_id',
                                'imdb_id' : 'imdb_id',
                                'genres_list': 'genres_name'
                        }
                )
                print(f'Here is {self.filename} file datatype information :/n {self.df.info()}')
                print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')

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

