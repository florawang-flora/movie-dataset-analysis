import pandas as pd
from abc import abstractmethod
class BaseCuration:
    def __init__(self,df):
        self.df = df 
        # save bad records for the later investigation
        self.bad_records = {}

        self.entity_df = None 
        self.mapping_df = None

    def check_column_data_type(self): 
        '''
        display the current data type of each column
        '''
        print('Current column data types: ')
        print(self.df.dtypes)
        return self.df.dtypes
    
    def transformed_date_column_data_type(self,col): 
        '''
        convert a column to date format. Invalid values will be converted to Nan. 
        '''
        pass
    
    @abstractmethod
    def generate_entity_df(self): 
        '''
        select the required columns and generate the final entity data frame
        Eg. movie, genre, cast, crew
        '''
        pass 

    def generate_mapping_df(self): 
        '''
        generate the maaping dataframe
        eg. movie_genre, movie_cast,movie_crew
        '''
        pass


    def check_duplicates_entity_table(self): 
        ''''''
        pass
    
    def check_duplicates_mapping_table(self,columns):
        '''
        check whether the mapping table contains duplicated . 
        key_columns = ['tmdb_id', 'genre_id']
        ''' 
        duplicate_boolean = self.mapping_df.duplicated(subset=columns,keep=False)
        duplicate_rows = self.mapping_df[duplicate_boolean]

        if not duplicate_rows.empty:
            print('The mapping table has duplicated records')
            self.bad_records['mapping_table_duplicates'] = duplicate_rows
            self.mapping_df = self.mapping_df.drop_duplicates(subset = columns, keep = 'first')
        else:
            print('The mapping tables has no duplicated records')
        
        return self.mapping_df
    

    @abstractmethod
    def primary_key_check_entity_table(self, primary_key):
        '''
        check whether the entity table primary key: 
        1. contains null values 
        2. contains duplicated values
        '''
        if self.entity_df is None: 
            print('The entity dataframe has not been generated')
            return None 
        
        # check null primary key
        boolean_is_primary_key = self.entity_df[primary_key].isna()
        null_rows = self.entity_df[boolean_is_primary_key]
        
        if not null_rows.empty: 
            print(f'The primary key {primary_key} has null values')
            self.bad_records[f'{primary_key}_null'] = null_rows

        # we have save the bad records. Delete rows where the primary key is null. 
        self.entity_df = self.entity_df.dropna(subset = [primary_key])

        # check duplicated_rows.empty: 
        boolean_duplicate_primary_key = self.entity_df.duplicated(subset=[primary_key], keep=False)
        duplicate_rows = self.entity_df[boolean_duplicate_primary_key]

        self.entity_df = (
            self.entity_df
            .drop_duplicates(
                subset=[primary_key],
                keep='first'
            )
            .reset_index(drop=True)
        )

        if not duplicate_rows.empty: 
            print(f'The primary key {primary_key} has duplicated values')
            self.bad_records[f"{primary_key}_duplicates"] = duplicate_rows

            #self.entity_df = (
            #    self.entity_df
            #    .sort_values('release_date')
            #    .drop_duplicates(subset = [primary_key], keep = 'last')
            #)
        else:
            print(f'The primary key {primary_key}is unique')

        return self.entity_df 


        #if not duplicate_rows.empty: 
            #print(f'The primary key {primary_key} has duplicated balues')

    #def primary_key_check_mapping_table(self): 

    

    def run(self): 
        '''
        run the common data curation process. 
        1. check column data type
        2. transformed date column 
        3. check the primary key null 
        4. check primary key duplicates
        5. check mapping key null 
        6. check mapping table duplicates
        7. save bad records 
        8. run the common process 
        '''
        # step1: display the origianl column data types
        pass

  

  


