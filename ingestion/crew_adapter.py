import pandas as pd
from ingestion.base_adapter import BaseAdapter
from tools.utils import Utils
class CrewAdapter(BaseAdapter): 
    def flatten_data(self): 
        """
        This method is to flatten crew data from credits.csv data source
        step1: change the nested string format to the list format.
        step2: explode the data. 
        step3: take the cast out to form the keywords.df
        """
        #step1: change the nested string format to the list format.
        self.df['crew_list'] = self.df['crew'].apply(Utils.parse)

        #step2: explode the data
        crew_df = self.df[['id', 'crew_list']].explode('crew_list')
        # crew_list now with the dict format

        # drop dulplicate rows 
        crew_df.dropna(subset= ['crew_list'])

        # flatten the character, gender, names  from the cast_list(dict) column.

        flatten_normailized_crew =  pd.json_normalize(crew_df['crew_list'])
        
        #add tmdb_id to the df.
        # the reason why we do it first is because cast also has the column called id as well.
        flatten_normailized_crew['tmdb_id'] = crew_df['id']

        #column: department, gender, job， name
        # take the id, character, gender, name to the df and rename it. 

        self.df = flatten_normailized_crew[[ 'tmdb_id', 'department', 'gender', 'job', 'name']].rename(
            columns = {
            'tmdb_id':'tmdb_id', 
            'department': 'crew_department', 
            'gender' : 'gender', 
            'name': 'crew_name', 
            'job': 'crew_job'
            })
        print(f'Here is {self.filename} file datatype information :/n {self.df.info()}')
        print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')
        return self.df
    

    

