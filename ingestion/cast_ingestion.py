import pandas as pd
class CastIngestion: 
    def __init__(self,ingestion_df):
        self.df = ingestion_df.copy()
        # cast table only contains cast
        self.cast_df = None 
        self.bad_records = {}
    def _retrieve_df(self):
        self.cast_df = self.df[['actor_id', 'gender', 'cast_name']]
        return self.cast_df
  
    
    def _transformed_table_type(self): 
        '''
        For each column, we're going to see whether they have the bad format data type. 

        For each column, check the column name:
            If it's actor_id. (check the current type:) -> transfer to string [this part can check whether the pirmary key has null value]
            If it's cast_name -> transfer to string 
            If it's gender -> transform the number to the string 
                gender = 2 male
                gender = 1 female 
                gender = 0 non-binary
                Note: gender = 2 and gender = 0 can be described as same people

        For these changes, if they have the incorrect format, delete the records
        such as gender is '1233.png'
        return self.cast_df

        transformed includes clean the null value ,if  we have the null value, we'll drop na. transfer the data type, 
        '''
        # actor_id 
        # finding NA value then cleaning, fianlly transfer the type 
        # convert actor_id to numeric fist, invalid values become NaN
        self.cast_df['actor_id'] = pd.to_numeric(
            self.cast_df['actor_id'],
            errors = 'coerce'
        )
        # records bad records if we have, then will print the logging information
        bad_records_actor_id = self.cast_df[self.cast_df['actor_id'].isna()]
        if not bad_records_actor_id.empty:
            self.bad_records['bad_actor_id'] = bad_records_actor_id
            print(f'Found {len(bad_records_actor_id)} bad actor_id records. They will be removed')

        # remove records which has Nan values 
        self.cast_df = self.cast_df.dropna(subset =['actor_id'])

        #convert actor_id to string and strip spaces

        self.cast_df['actor_id']= self.cast_df['actor_id'].astype('int').astype('str')


        # cast_name 
        # if we found the NA data, fill na with empty string
        # transfer the type to become the stirng.
        # strip spaces
        self.cast_df['cast_name'] = (
            self.cast_df['cast_name']
            .fillna('')
            .astype(str)
            .str.strip()
        )


        # gender 
        # only keep valid gender values
        valid_gender = [0, 1, 2]
        bad_gender = self.cast_df[~self.cast_df['gender'].isin(valid_gender)]
        if not bad_gender.empty: 
            self.bad_recrods['bad_gender'] = bad_gender
            print(f'Found {len(bad_gender) } bad gender reocords, They will be removed')
        self.cast_df = self.cast_df[self.cast_df['gender'].isin(valid_gender)]

        gender_map = {
            3: 'unknown',
            2: 'male',
            1: 'female',
            0: 'non-binary' 

        }
        self.cast_df['gender'] = self.cast_df['gender'].map(gender_map)
        #print(self.cast_df.dtypes)
        print(self.cast_df.shape)
        return self.cast_df 

# make sure the primary key don't have the null value 
    def _clean_duplicates(self):
        '''
        return 
        check the table whether it has duplicatation. 
        clean the duplication, if there are two records that only keep 1 

        actor_id character_name gender  
        23764.0	Эрика Элениак	1.0
        23764.0	Erika Eleniak	1.0
        check table whether have duplicates: 
        If it has: 
            print(logging information- id with this name has the duplicates, please go to raw data source to clean the data.)
        else: 
           logging message cleaning successfully. 
        '''
        # delete the row duplicates
        cast_df_clean = self.cast_df.drop_duplicates()
        # make sure the actor_id is unqiue 
        cast_df_clean = cast_df_clean.drop_duplicates(subset=['actor_id'], keep='first')
        

        duplicates = cast_df_clean[cast_df_clean.duplicated(subset=['actor_id'], keep=False)]
        if not duplicates.empty:
            print(f'The duplicates actor ids are {duplicates},please have a check ')
        else:
            print('No duplicates!')
        
        self.cast_df = cast_df_clean
        return self.cast_df 

    def generate_main_table(self):
        '''
        return the head of table looks like. 
        look at the column type. 
        '''
        print("\nFinal cast table preview:")
        print(self.cast_df.head())

        print("\nColumn types:")
        print(self.cast_df.dtypes)
        return self.cast_df
    
    def process(self): 
        self._retrieve_df()
        self._transformed_table_type()
        self._clean_duplicates()
        self.generate_main_table()
        return self.cast_df 

    


        
        