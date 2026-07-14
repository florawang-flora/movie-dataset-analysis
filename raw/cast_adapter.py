import pandas as pd
from raw.base_adapter import BaseAdapter
from tools.utils import Utils
from tools.load_config import load_conf

class CastApater(BaseAdapter): 
    def flatten_data(self): 
        """
        This method is to flatten cast data from credits.csv data source
        step1: change the nested string format to the list format.
        step2: explode the data. 
        step3: take the cast out to form the keywords.df
        """
        #step1: change the nested string format to the list format.
        self.df['cast_list'] = self.df['cast'].apply(Utils.parse)
        
        #step2: explode the data
        cast_df = self.df[['id', 'cast_list']].explode('cast_list')
        # cast_list now with the dict format

        # drop nah rows 
        cast_df.dropna(subset= ['cast_list'])

        # flatten the character, gender, names  from the cast_list(dict) column.

        flatten_normailized_cast =  pd.json_normalize(cast_df['cast_list'])
        #print(flatten_normailized_cast.head(1))
        #print('here is the flatten_normalized_cast', flatten_normailized_cast)
        #add tmdb_id to the df.
        # the reason why we do it first is because cast also has the column called id as well.
        # save id named as tmdb_id in case of ambiguity
        flatten_normailized_cast['tmdb_id'] = cast_df['id']

        #column: character, gender, name
        # take the id, character, gender, name to the df and rename it. 

        # before the change 
        self.df = flatten_normailized_cast[[ 'tmdb_id', 'character','gender', 'name', 'id']].rename(
            columns = {
            'tmdb_id':'tmdb_id', 
            'id': 'actor_id',
            'character': 'character_name', 
            'gender' : 'gender', 
            'name': 'cast_name'
            })
      
        return self.df
       
    
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
    


#if __name__ == '__main__':
#    config = load_conf()
#    data_source = config['data_source']
#    casts = data_source['casts']
#
#    raw_cast= CastApater(casts['path'], casts['table_name'])
#
#    cast_df = raw_cast.process()
#    print(f'here is cast df {cast_df.dtypes}')
#    print(f'here is cast df {cast_df.shape}')
