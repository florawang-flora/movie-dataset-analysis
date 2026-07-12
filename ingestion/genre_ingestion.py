import pandas as pd
class GenreIngestion:
    def __init__(self,genre_df):
        self.df = genre_df.copy()
        # store invalid records for later investigation
        self.bad_records ={}

    #def genre_id, tmdb_id, genre_id, whether has the null value., 
    # if it has, save it to the bad_record. 

    # then to check whether we have the dulplicates, if we don't have it, then delete it. 

    def _transformed_table_type(self):
        """
        1.check tmdb_id and genre_id 
        2.save the invalid records 
        3.remove null records 
        4.convert ids to string
        """
        # convert the tmdb_id to numeric
        self.df['tmdb_id'] = pd.to_numeric(
            self.df['tmdb_id'], 
            errors = 'coerce'
        )
        # check the data whether is belong to na.
        is_na_tmdb_id = self.df['tmdb_id'].isna()
        bad_tmdb_id = self.df[is_na_tmdb_id]

        # save the nan records to the bad records
        if not bad_tmdb_id.empty:
            self.bad_records['bad_tmdb_id'] = bad_tmdb_id
            print( f"Found {len(bad_tmdb_id)} number of bad tmdb_id records ")
        

        # conver the genre_id to numeric so can find nan value. 
        self.df['genre_id'] = pd.to_numeric(
            self.df['genre_id'],
            errors = 'coerce'
        )

        is_na_genre_id = self.df['genre_id'].isna()
        bad_genre_id = self.df[is_na_genre_id]

        if not bad_genre_id.empty: 
            self.bad_records['bad_genre_id'] = bad_genre_id
            print( f"Found {len(bad_tmdb_id)} number of bad genre records ")
        
        # remove records with null IDs
        self.df = self.df.dropna(
            subset = ['tmdb_id', 'genre_id']
        )

        # convert ids from float to string 

        self.df['tmdb_id'] = self.df['tmdb_id'].astype('int').astype('str')

        self.df['genre_id'] = self.df['genre_id'].astype('int').astype('str')

        self.df['genre_name'] = self.df['genre_name'].fillna('').astype('str').str.strip()

        return self.df

        # genrate the genre_raw_base table 
    
    def _clean_duplicates(self):
        boolean_dulplicates = self.df.duplicated(
            subset = ['tmdb_id', 'genre_id', 'genre_name'],
            keep = False
        )

        duplicates = self.df[boolean_dulplicates]
        print(f'Found {duplicates} duplicate records')

        self.df = self.df.drop_duplicates(
            subset = ['tmdb_id', 'genre_id', 'genre_name'],
            keep = 'first'
        )
        return self.df
    

    def _generate_genre_table(self): 
        print('\nFinal genre table:')
        print(self.df.head())

        print('\nColumn types: ')
        print(self.df.dtypes)

        return self.df

    def process(self):
        self._transformed_table_type()
        self._clean_duplicates()
        self._generate_genre_table()

        return self.df






        
        

        



        


    

