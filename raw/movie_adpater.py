import pandas as pd
import ast  
from raw.base_adapter import BaseAdapter
from tools.utils import Utils
class MovieAdapter(BaseAdapter):
        # flatten data column have problem rn.       
        def flatten_data(self):
            """
            This method is to flatten movie metadata for the specific data frame. 
            step1: change the nested string format to the list format.
            step2: explode the data. 
            step3: take the keynames out to form the keywords.df
            columns: 
            budget, tmdb_id, imdb_id, overview, poplularity, production_companies_name, produnction_countries,
            release_date,revenue,tagline, title, vote_average, vote_count
            # I don't want to take the vote_average, vote_count at the moment. 
            # but I take it first, let's see how it goes.
            produnction companies : list of dict
            produnction_countries : list of dict
            """
            # step1: production_companies
    
            self.df["production_companies"] = self.df['production_companies'].apply(Utils.parse)
            movie_df = self.df[['id', 'imdb_id', 'title', 'budget', 'overview', 'popularity', 'production_companies', 'production_countries',
            'release_date','revenue','tagline', 'vote_average', 'vote_count']].explode('production_companies')
            movie_df.dropna(subset = ['production_companies'])
            movie_df['production_companies'] = movie_df['production_companies'].apply(lambda x : x['name'] if isinstance(x,dict) and 'name' in x else None)
            # step2: production_countries
            movie_df =  self.df[['id', 'imdb_id', 'title', 'budget', 'overview', 'popularity', 'production_companies', 'production_countries',
            'release_date','revenue','tagline', 'vote_average', 'vote_count',]].explode('production_countries')
            movie_df.dropna(subset = ['production_countries'])
            movie_df['production_countries'] = movie_df['production_countries'].apply(lambda x : x['name'] if isinstance(x,dict) and 'name' in x else None)
            self.df = movie_df.rename(
                    columns = {
                            'id':'tmdb_id', 
                            'title':'movie_title'
                    }
            )
            print(f'Here is {self.filename} file datatype information :/n {self.df.info()}')
            print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')
            return self.df




