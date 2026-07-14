import pandas as pd
from curation.curation_base import BaseCuration
class GenreCuration(BaseCuration):
    def __init__(self,df):
        # run the __init__ method from BaseCuration
        super().__init__(df)
    
    def clean_genre_name(self): 
        '''
        clean the genre_name column 
        1. Fill the null value with an empty string 
        2. convert values to string
        3. removie spaces.
        4. save and remove empty genre names. 
        '''
        self.df['genre_name'] = self.df['genre_name'].fillna('').astype(str).str.strip()
        empty_genre_name_rows = self.df[self.df['genre_name'] == '']

        if not empty_genre_name_rows.empty:
            print(f'found {len(empty_genre_name_rows)} empty genre_name records')
        else: 
            print('The genre_name has no empty values')

    def generate_entity_df(self): 
        '''
        generate the genre entity table. 
        columns with genre_id, genre_name
        '''
        genre_columns = ['genre_id', 'genre_name']
        self.entity_df = self.df[genre_columns].copy()

        

        rows = self.entity_df.shape[0]
        columns = self.entity_df.shape[1]
        print(f"The genre entity dataframe has {rows} rows {columns} columns")
        
        print(self.entity_df.head(2))
        
        return self.entity_df
    
    def generate_mapping_df(self): 
        '''
        genreate the movie_genre_mapping table, columns with the tmdb_id, genre_id
        '''
        genre_movie_columns = ['tmdb_id', 'genre_id']
        self.mapping_df = self.df[genre_movie_columns].copy()

        rows = self.mapping_df.shape[0]
        columns = self.mapping_df.shape[1]
        print(f"The movie_genre entity dataframe has {rows} rows {columns} columns")
        
        print(self.mapping_df.head(2))

        return self.mapping_df 
    

    def run(self):
        """
        Run the genre curation process.
        """

        # Display the original column data types.
        self.check_column_data_type()

        self.clean_genre_name()

        # Generate the genre entity dataframe.
        self.generate_entity_df()

        # Remove completely duplicated rows from the genre entity table.
        self.check_duplicates_entity_table()

        # Check genre_id because genre_id is the primary key of the genre table.
        self.primary_key_check_entity_table("genre_id")

        # Generate the movie_genre mapping dataframe.
        self.generate_mapping_df()

        # Check duplicated movie and genre relationships.
        self.check_duplicates_mapping_table(["tmdb_id", "genre_id"])

        print("Final genre table:\n")
        print(self.entity_df.head())

        print("Final movie_genre mapping table:\n")
        print(self.mapping_df.head())

        return self.entity_df, self.mapping_df

  
    

        


    #def run(self): 
    #    '''
    #    run the genre curaton process 
    #    '''
    #   
    #    pass
    #
    #def check_duplicates_mapping_table(self,columns):
#
    #
#
    #    # step3: Generate the movie entity DataFrame.
    #    self.generate_entity_df()
#
    #    # step4: Check the tmdb_id primary key.
    #    self.primary_key_check_entity_table("tmdb_id")
#
    #    return self.entity_df