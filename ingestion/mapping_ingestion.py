class MappingIngestion: 
    def __init__(self,  movie_mapping_df): 
        self.movie_mapping_df = movie_mapping_df
    def _clean_duplicates(self):
        # I'll do it later for each other column how do I solve
        self.movie_mapping_df = self.movie_mapping_df.drop_duplicates()

    def generate_mapping_table(self):
        """
        select the correcsponding column name + create the tname 
        """
        print('yyyyyyyy',self.movie_mapping_df.head(5))
        return self.movie_mapping_df


    def process(self):
        self._clean_duplicates()
        self.generate_mapping_table()
        return self.movie_mapping_df
