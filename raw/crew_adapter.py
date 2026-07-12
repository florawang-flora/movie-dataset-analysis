import pandas as pd
from raw.base_adapter import BaseAdapter
from tools.utils import Utils
from tools.load_config import load_conf
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

        self.df = flatten_normailized_crew[[ 'tmdb_id', 'department', 'gender', 'job', 'name', 'id']].rename(
            columns = {
            'tmdb_id':'tmdb_id',
            'department': 'department',
            'gender' : 'gender', 
            'name': 'crew_name', 
            'job': 'job',
            'id': 'crew_id'
             })
        print(f'Here is {self.filename} file datatype information :/n {self.df.info}')
        print(f'Here is the example of the {self.filename} dataset:/n {self.df.head(5)} ')

        #self.movie_crew_df = flatten_normailized_crew[[ 'tmdb_id','id', 'job', 'department']].rename(
        #    columns = {
        #    'tmdb_id':'tmdb_id', 
        #    'id': 'crew_id',
        #    'job': 'job', 
        #    'department': 'department'
        #    })
        #print(f'Here is movie_crew mapping file datatype information :/n {self.movie_crew_df.info}')
        #print(f'Here is the example of the movie_crew dataset:/n {self.movie_crew_df.head(5)} ')
        #return self.df, self.movie_crew_df 

    
        
    def process(self):
        '''
        1.load the data from the data source
        2, check the dulplicate rows for it 
        3. clean the data dulplicate row . 
        4, flatten the data for the specific data frame.
    
        '''
        self._load_data()
        self._check_data_dulplicates()
        self._clean_data_dulplicates()
        self.flatten_data()

        return self.df
        #, self.movie_crew_df 
    
if __name__ == '__main__':
     config = load_conf()
     data_source = config['data_source']
     cast = data_source['casts']
     raw_cast = CrewAdapter(cast['path'], cast['table_name'])
     casts_df = raw_cast.process() 
