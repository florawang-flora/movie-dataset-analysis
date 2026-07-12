import pandas as pd
from curation.curation_base import BaseCuration


class MovieCuration(BaseCuration): 
    def __init__(self,df):
        # run the __init_ method from BaseCuration
        super().__init__(df)
    
    def transformed_date_column_data_type(self,col): 
        '''
        convert a column to date format. Invalid values will be converted to Nan. 
        '''
        converted_col = pd.to_datetime(self.df[col], errors = 'coerce')

        # find values that are not null originally
        # but become null after the conversion 

        boolen_bad_records = self.df[col].notna() & converted_col.isna()
        bad_format_rows = self.df[boolen_bad_records]

        if not bad_format_rows.empty:
            print(f'The column {col} has incorrect data values')
            self.bad_records[f'{col}_bad_format'] = bad_format_rows 

        # save the converted values back to the dataframe
        self.df[col] = converted_col

        print(f'{col} transformed successfully')

        return self.df

    def generate_entity_df(self): 
        movie_columns = ['tmdb_id', 'movie_title', 'budget', 'overview', 'popularity', 'production_companies','release_date','revenue']
        self.entity_df = self.df[movie_columns].copy()

        rows = self.entity_df.shape[0]
        columns = self.entity_df.shape[1]
        print(self.entity_df.head(2))
        
        return self.entity_df
    
    def run(self): 
        '''
        run the movie curaton process 
        '''
        # step1: display the original column data types. 
        self.check_column_data_type()

        # step2: transformed all release_date column data types
        self.transformed_date_column_data_type('release_date')

        # step3: Generate the movie entity DataFrame.
        self.generate_entity_df()

        # step4: Check the tmdb_id primary key.
        self.primary_key_check_entity_table("tmdb_id")

        return self.entity_df
        