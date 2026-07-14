import pandas as pd
import ast  
from raw.base_adapter import BaseAdapter
from tools.utils import Utils
from tools.load_config import load_conf
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
      
                self.df["genre_dict"] = self.df['genres'].apply(Utils.parse)
                
                # select the required columns and create one row for each genre.
                genres_df = self.df[['id','genre_dict']].explode('genre_dict')

                # remove rows that do not contain genre information.
                genres_df.dropna(subset = ['genre_dict'])

                # extract the genre name from each genre dictionary.
                genres_df['genre_name'] = genres_df['genre_dict'].apply(lambda x : x['name'] if isinstance(x,dict) and 'name' in x else None)

                # extract the genre name from each genre dictionary.
                genres_df['genre_id'] = genres_df['genre_dict'].apply(lambda x : x['id'] if isinstance(x, dict) and 'id' in x else None  )

                self.df = genres_df[['id',  'genre_id','genre_name']].rename(
                        columns ={
                                'id': 'tmdb_id',
                                'genre_name': 'genre_name',
                                'genre_id': 'genre_id'
                        }
                )
                print(f'Here is {self.filename} file datatype information :/n {self.df.info()}')
                print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')

                return self.df 

#if __name__ == '__main__':
#        config = load_conf()
#        data_source = config['data_source']
#        genre = data_source['genres']
#       raw_genre = GenreAdapter(genre['path'], genre['table_name'])
#       genres_df = raw_genre.process()
        