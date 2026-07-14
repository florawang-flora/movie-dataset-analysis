import pandas as pd
class CastIngestion: 
    def __init__(self,ingestion_df,valid_tmdb_ids):
        self.df = ingestion_df.copy()
        # cast table only contains cast
        self.cast_df = None 
        self.bad_records = {}
        self.valid_tmdb_ids = valid_tmdb_ids
    def _check_primary_null_in_column(self, col):
        is_null_column = self.df[col].isna().any()
        if is_null_column: 
            print(f'The column {col} has null value')
            bad_rows = self.df[self.df.isna()]
            self.bad_records[f'{col}_null'] = bad_rows
            return self.bad_records
        else:
            print(f'The column {col} has no null value')


    def _check_key_incorrect_format_string(self, col):
        """
        Check whether a supposed ID column has incorrect format.
        Example: tmdb_id should be numeric, then stored as string.
        """
        # First, try to convert the column to numeric values.
        # Invalid values will be converted to NaN.
        converted_col = pd.to_numeric(self.df[col], errors="coerce")
        # Find rows with an invalid format:
        # The original value is not empty, but it becomes NaN after conversion.
        # This means the original value has an incorrect format.

        # For example, if "1998-01-01" appears in the tmdb_id column:
        # self.df[col].notna() returns True because the original value is not empty.
        # converted_col.isna() also returns True because "1998-01-01"
        # cannot be converted to a numeric value.
    
        bad_format_rows = self.df[self.df[col].notna() & converted_col.isna()]
        if not bad_format_rows.empty:
            print(f"The column {col} has incorrect format rows")
            self.bad_records[f"{col}_bad_format"] = bad_format_rows
        else:
            print(f"The column {col} format looks fine")
        # Save the converted values back to the DataFrame.
        self.df[col] = converted_col
        # Find null rows, including:
        # 1. Original null values.
        # 2. Invalid values that became NaN after conversion.
        null_rows = self.df[self.df[col].isna()]
        # save the null rows into bad_records for later investigation.
        if not null_rows.empty:
            self.bad_records[f"{col}_null_after_convert"] = null_rows
        # Delete rows where the primary key is null.
        self.df = self.df.dropna(subset=[col])
        # Convert the column from float to integer, and then to string.
        self.df[col] = self.df[col].astype(int).astype(str)
        # Print a message after the column is cleaned successfully.
        print(f"{col} cleaned successfully")
    
    def _check_null_in_columns(self,col): 
        is_null_column = self.df[col].isna().any()
        if is_null_column:
            print(f'{col} has null values')
            # to chekc the type whether is string or object
            if self.df[col].dtype == 'object' or self.df[col].dtype == 'string':
                # if it's a null value the column type is string, we'll fill the NA value 
                self.df[col] = self.df[col].fillna('')
                print(f'{col} null values replaces with empty string')
        else:
            print(f'The column {col} has no null value')
        return self.df[col]
    
    def _clean_string_column(self, series):
        col = series.name
        self.df[col] = series.astype(str).str.strip()
        print('Successfully finish cleaning the string column')
        return self.df

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
        #===========
        # actor_id  primary-key 
        #===========
        self._check_primary_null_in_column('actor_id')
        self._check_key_incorrect_format_string("actor_id")

        ## records bad records if we have, then will print the logging information
        #bad_records_actor_id = self.cast_df[self.cast_df['actor_id'].isna()]
        #if not bad_records_actor_id.empty:
        #    self.bad_records['bad_actor_id'] = bad_records_actor_id
        #    print(f'Found {len(bad_records_actor_id)} bad actor_id records. They will be removed')
#
        ## remove records which has Nan values ,because it will use the primary key in the future. 
        #self.cast_df = self.cast_df.dropna(subset =['actor_id'])
#
        ##convert actor_id to string and strip spaces
#
        #self.cast_df['actor_id']= self.cast_df['actor_id'].astype('int').astype('str')

        #============
        #tmdb_id
        #============
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
         
        #convert ids from float to string 
        self.df['tmdb_id'] = self.df['tmdb_id'].astype('int').astype('str')
     
        #===========
        # cast_name 
        #===========
        # if we found the NA data, fill na with empty string
        # transfer the type to become the stirng.
        # strip spaces
        self.df['cast_name'] = (
            self.df['cast_name']
            .fillna('')
            .astype(str)
            .str.strip()
        )
        #=========
        # gender 
        #=========
        # only keep valid gender values
        valid_gender = [0, 1, 2]
        bad_gender = self.df[~self.df['gender'].isin(valid_gender)]
        if not bad_gender.empty: 
            self.bad_recrods['bad_gender'] = bad_gender
            print(f'Found {len(bad_gender) } bad gender reocords, They will be removed')
        self.df = self.df[self.df['gender'].isin(valid_gender)]

        gender_map = {
            3: 'unknown',
            2: 'male',
            1: 'female',
            0: 'non-binary' 

        }
        self.df['gender'] = self.df['gender'].map(gender_map)

        string_columns = ['character_name', 'gender', 'cast_name','actor_id','tmdb_id']

        # clean and transform multiple string columns

        for col in string_columns: 
            column = self._check_null_in_columns(col)
            self._clean_string_column(column)

        print(self.df.dtypes)
        print(self.df.shape)
        return self.df 
    def _filter_valid_tmdb_ids(self):
        '''
        Only keep cast records whose tmdb_id is not in the movie table 
        '''
        #make tmdb_id string type
        self.df['tmdb_id'] = self.df['tmdb_id'].astype(str)
        #find cast records whose tmdb_id is not in the movie table
        invalid_rows = self.df[~self.df['tmdb_id'].isin(self.valid_tmdb_ids)]
        # save invalid records 
        if not invalid_rows.empty:
            self.bad_records['valid_tmdb_ids'] = invalid_rows
            print(f'Found {len(invalid_rows)} invalid tmdb_id records')
        # only keep valid tmdb_records
        boolean_valid_records = self.df['tmdb_id'].isin(self.valid_tmdb_ids)
        self.df = self.df[boolean_valid_records]
        print(f'{len(self.df)} valid cast records remain')
        return self.df 
        


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
        cast_df_clean = self.df.drop_duplicates()
        # make sure the actor_id is unqiue 
        cast_df_clean = cast_df_clean.drop_duplicates(subset=['actor_id'], keep='first')
        

        duplicates = cast_df_clean[cast_df_clean.duplicated(subset=['actor_id'], keep=False)]
        if not duplicates.empty:
            print(f'The duplicates actor ids are {duplicates},please have a check ')
        else:
            print('No duplicates!')
        
        self.df = cast_df_clean
        return self.df 

    def generate_main_table(self):
        '''
        return the head of table looks like. 
        look at the column type. 
        '''
        print("\nFinal cast table preview:")
        print(self.df.head())

        print("\nColumn types:")
        print(self.df.dtypes)
        return self.df
    
    def process(self): 
        self._transformed_table_type()
        self._filter_valid_tmdb_ids()
        self._clean_duplicates()
        self.generate_main_table()
        return self.df 

    


        
        