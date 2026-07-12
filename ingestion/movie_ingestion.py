import pandas as pd
class MovieIngestion:
    '''
    STEP1: CHECK EACH COLUMN WHETHER THEY HAVE THE INCORRECT FORMAT
    FOR EACH COLUMN WE PICKED, check whether the column has incorect format, 
    for the bad data, we try to save it, and tell user we have the bad data, we need to do the manual validate. 
    STEP2: check for each column whether we have the Nan VALUE . 
    if the id. has the null value, print it, and save it later. 
    if the result of it, set it as NULL or empty string. 
    STEP3: Once it correct, create it as dataframe. 
    step3: 
     
    '''
    '''
    Curate movie dataset
    1. check null value in key columns
    2. check incorrect format 
    3. save bad records 
    4. return cleaned df
    '''
    def __init__(self,df):
        self.df = df 
        self.transformed_df = None
        self.bad_records = {}

    
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
    
    def _clean_integer_column(self, series):
        col = series.name 
        # tranform to the numeric data
        coverated_col = pd.to_numeric(self.df[col], errors = 'coerce')
        # find the bad data
        bad_format_rows = self.df[self.df[col].notna() & coverated_col.isna()]
        if not bad_format_rows.empty: 
            print(f'The column {col} has incorrect format rows')
            self.bad_records[f'{col}_bad_format'] = bad_format_rows
        else:
            print(f"The column {col} format looks fine")
        # cover the original column 
        self.df[col] = coverated_col 

        # clean the NaN column 
        self.df = self.df.dropna(subset = [col])

        # change it to the int type
        self.df[col] = self.df[col].astype('int')
        print(f'{col} cleaned successfully')
        print(self.df.info())
        return self.df
    

    def _clean_date_column(self, col): 
        """
        release date : 1999-12-19
        null value
        wrong format 1998/01/01 01-01-1998
        dirty data: 'unknown'
        wrong data format: "/ff9qCepilowshEtG2GYWwzt2bs4.jpg"
        """
        # change the data type to the datetime format
        converted_col = pd.to_datetime(self.df[col],errors = 'coerce')
        # find the bad data
        bad_format_rows = self.df[self.df[col].notna() & converted_col.isna()]

        # overite the original column 
        self.df[col]  = converted_col

        # stanrdardlize the column to 
        self.df[col] = self.df[col].dt.strftime("%Y-%m-%d")
        print(f"{col} formated successfully")

    def _transformed_table_type(self):
        # Display all current column data types.
        print("Data types before transformation:")
        print(self.df.dtypes)

        # movies tmdb_id
        self._check_primary_null_in_column('tmdb_id')
        self._check_key_incorrect_format_string("tmdb_id")
        
        # movie_title
        # budget
        # overview
        # production_companies 
        string_columns = ['movie_title', 'budget', 'overview','production_companies']

        # clean and transform multiple string columns

        for col in string_columns: 
            column = self._check_null_in_columns(col)
            self._clean_string_column(column)

        # release_date
        # clean release_date and keep the final format as string: YYYY-MM-DD
        self._clean_date_column('release_date')
        

        #popularity_date
        #transformed populartiy to float 
        converted_popularity = pd.to_numeric(self.df['popularity'], errors = 'coerce')
        # find incorrect_popuarlity_values
        # check whether popularity has a value but cannot be converted to a number.
        boolean_popularity = self.df['popularity'].notna() & converted_popularity.isna()
        popularity_bad_rows = self.df[boolean_popularity]

        if not popularity_bad_rows.empty: 
            print('The column popularity has incorrect format rows')
            self.bad_records['populartiy_bad_format'] = popularity_bad_rows
        else:
            print('The column popularity format looks fine')

        # save the converted popularity columns. 
        self.df['popularity'] = converted_popularity.astype('float64')
        
        # revenue
        # transformed revenus to integer 
        revenue = self._check_null_in_columns('revenue')
        self._clean_integer_column(revenue)

        #budget 
        budget = self._check_null_in_columns('budget')
        self._clean_integer_column(budget)


        self.transformed_df = self.df.copy()

        # display all column data types after transformation 
        print('Data types after transformation: ')
        print(self.transformed_df.dtypes)
        return self.transformed_df



    def _generate_movie_dataframe(self):
        rows, columns = self.transformed_df.shape[0], self.transformed_df.shape[1]
        print(f'Here is the movie dataframe with {rows} rows and {columns} columns')
        print(f'Here is the sample of the dataframe {self.transformed_df.head()}')

        return self.transformed_df

    def run(self):
        self._transformed_table_type()
        self._generate_movie_dataframe()
        return self._generate_movie_dataframe()
       
   
   


 
