import pandas as pd
from curation.curation_base import BaseCuration
class CrewCuration(BaseCuration):
    def __init__(self,df):
        super().__init__(df)

    def generate_entity_df(self): 
        '''
        generate the crew entity table. 
        columns with crew_id, crew_name, gender
        '''
        crew_columns = ['crew_id', 'crew_name','gender']
        self.entity_df = self.df[crew_columns].copy()
        
        rows = self.entity_df.shape[0]
        columns = self.entity_df.shape[1]
        print(f"The crew entity dataframe has {rows} rows {columns} columns")
        
        print(self.entity_df.head(2))
        
        return self.entity_df
    
    def generate_mapping_df(self): 
        '''
        genreate the crew_movie  table, columns with the tmdb_id, 
        '''
        print(f'here is {self.df.head(2)}')
        crew_movie_columns = ['tmdb_id', 'crew_id', 'job', 'department']
        self.mapping_df = self.df[crew_movie_columns].copy()

        rows = self.mapping_df.shape[0]
        columns = self.mapping_df.shape[1]
        print(f"The movie_cast entity dataframe has {rows} rows {columns} columns")
        
        print(self.mapping_df.head(2))

        return self.mapping_df 
    
    def run(self):
        """
        Run the crew curation process.
        """

        # Display the original column data types.
        self.check_column_data_type()


        # Generate the crew entity dataframe.
        self.generate_entity_df()

        # Remove completely duplicated rows from the crew entity table.
        self.check_duplicates_entity_table()

        # Check crew_id because crew_id is the primary key of the cast table.
        self.primary_key_check_entity_table("crew_id")

        # Generate the movie_cast mapping dataframe.
        self.generate_mapping_df()

        # Check duplicated tmdb_id and actor_id relationships.
        self.check_duplicates_mapping_table(["tmdb_id", "crew_id"])

        print("Final cast table:\n")
        print(self.entity_df.head())

        print("Final movie_cast mapping table:\n")
        print(self.mapping_df.head())

        return self.entity_df, self.mapping_df