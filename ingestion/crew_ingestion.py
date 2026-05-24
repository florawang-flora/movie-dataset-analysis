import pandas as pd
class CrewIngestion: 
    def __init__(self,ingestion_df):
        self.df = ingestion_df.copy()
        # cast table only contains cast
        self.crew_df = None 
        self.bad_records = {}
    def _retrieve_df(self):
        self.crew_df = self.df[['crew_id', 'gender', 'crew_name']]
        return self.crew_df

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
        return self.crew_df

        transformed includes clean the null value ,if  we have the null value, we'll drop na. transfer the data type, 
        '''
        # crew_id 
        # finding NA value then cleaning, fianlly transfer the type 
        # convert actor_id to numeric fist, invalid values become NaN
        self.crew_df['crew_id'] = pd.to_numeric(
            self.crew_df['crew_id'],
            errors = 'coerce'
        )
        # records bad records if we have, then will print the logging information
        bad_records_crew_id = self.crew_df[self.crew_df['crew_id'].isna()]
        if not bad_records_crew_id.empty:
            self.bad_records['bad_actor_id'] = bad_records_crew_id
            print(f'Found {len(bad_records_crew_id)} bad crew_id records. They will be removed')

        # remove records which has Nan values 
        self.crew_df = self.crew_df.dropna(subset =['crew_id'])

        #convert crew_id to string and strip spaces

        self.crew_df['crew_id']= self.crew_df['crew_id'].astype('int').astype('str')


        # cast_name 
        # if we found the NA data, fill na with empty string
        # transfer the type to become the stirng.
        # strip spaces
        self.crew_df['crew_name'] = (
            self.crew_df['crew_name']
            .fillna('')
            .astype(str)
            .str.strip()
        )


        # gender 
        # only keep valid gender values
        valid_gender = [0, 1, 2]
        bad_gender = self.crew_df[~self.crew_df['gender'].isin(valid_gender)]
        if not bad_gender.empty: 
            self.bad_recrods['bad_gender'] = bad_gender
            print(f'Found {len(bad_gender) } bad gender reocords, They will be removed')
        self.crew_df = self.crew_df[self.crew_df['gender'].isin(valid_gender)]

        gender_map = {
            2: 'male',
            1: 'female',
            0: 'non-binary' 

        }
        self.crew_df['gender'] = self.crew_df['gender'].map(gender_map)
        #print(self.crew_df.dtypes)
        print(self.crew_df.shape)
        return self.crew_df 

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
        crew_df_clean = self.crew_df.drop_duplicates()
        # make sure the crew_id is unqiue 
        crew_df_clean = crew_df_clean.drop_duplicates(subset=['crew_id'], keep='first')
        

        duplicates = crew_df_clean[crew_df_clean.duplicated(subset=['crew_id'], keep=False)]
        if not duplicates.empty:
            print(f'The duplicates actor ids are {duplicates},please have a check ')
        else:
            print('No duplicates!')
        
        self.crew_id = crew_df_clean
        return self.crew_df

    def generate_main_table(self):
        '''
        return the head of table looks like. 
        look at the column type. 
        '''
        print("\nFinal cast table preview:")
        print(self.crew_df.head())

        print("\nColumn types:")
        print(self.crew_df.dtypes)
        return self.crew_df
    
    def process(self): 
        self._retrieve_df()
        self._transformed_table_type()
        self._clean_duplicates()
        self.generate_main_table()
        return self.crew_df 

    


        
        