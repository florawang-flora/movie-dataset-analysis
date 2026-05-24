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
        self.bad_records = {}

    
    def check_primary_null_in_column(self, col):
        is_null_column = self.df[col].isna().any()
        if is_null_column: 
            print(f'The column {col} has null value')
            bad_rows = self.df[self.df.isna()]
            self.bad_records[f'{col}_null'] = bad_rows
            return self.bad_records
        else:
            print(f'The column {col} has no null value')
    




    def check_key_incorrect_format_string(self, col):
          """
          Check whether a supposed ID column has incorrect format.
          Example: tmdb_id should be numeric, then stored as string.
          """

          # 先尝试转成数字；坏值会变成 NaN
          converted_col = pd.to_numeric(self.df[col], errors="coerce")

          # 找出格式不对的行：
          # 原值不是空，但转换后变成空，说明原值有问题
          # check the origianal_id is not NA data. 
          # after after we do the transformation, we get the Nan data, 
          # from the example, we can see the data 1998-01-01 under the tmdb_id column, so 
          # self.df[col].notna() is NaN.
        
          bad_format_rows = self.df[self.df[col].notna() & converted_col.isna()]
          if not bad_format_rows.empty:
              print(f"The column {col} has incorrect format rows")
              self.bad_records[f"{col}_bad_format"] = bad_format_rows
          else:
              print(f"The column {col} format looks fine")

          # 把转换结果放回 dataframe
          self.df[col] = converted_col

          # 再找 null（包括原来的 null + 转换失败变成的 null）
          null_rows = self.df[self.df[col].isna()]
          if not null_rows.empty:
              self.bad_records[f"{col}_null_after_convert"] = null_rows

          ## 删除主键为空的行
          self.df = self.df.dropna(subset=[col])

          # change the int_to_the_str column.
          self.df[col] = self.df[col].astype(int).astype(str)

          print(f"{col} cleaned successfully")
    
    def check_null_in_columns(self,col): 
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

    
    def clean_string_column(self, series):
        col = series.name
        self.df[col] = series.astype(str).str.strip()
        print('Successfully finish cleaning the string column')
        return self.df
    
    def clean_integer_column(self, series):
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
    

    def clean_date_column(self, col): 
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
    def generate_movie_dataframe(self):
        movie_df = self.df[['tmdb_id', 'movie_title', 'production_companies', 'budget', 'revenue', 'release_date']]
        rows, columns = movie_df.shape[0], movie_df.shape[1]
        
        print(f'Here is the movie dataframe with {rows} rows and {columns} columns')
        print(f'Here is the sample of the dataframe {movie_df.head()}')

        return movie_df

    def run(self):
        # movies tmdb_id
        self.check_primary_null_in_column('tmdb_id')
        self.check_key_incorrect_format_string("tmdb_id")

        # movies title
        movies_title = self.check_null_in_columns('movie_title')
        self.clean_string_column(movies_title)

        # production company
        production_companies = self.check_null_in_columns('production_companies')
        self.clean_string_column(production_companies)

        # budget
        # it contans the bad data ValueError: invalid literal for int() with base 10: '/ff9qCepilowshEtG2GYWwzt2bs4.jpg'
        budget = self.check_null_in_columns('budget')
        self.clean_integer_column(budget)

        # revenue 
        revenue  = self.check_null_in_columns('revenue')
        self.clean_integer_column(revenue)
      
        # release_date 

        self.clean_date_column('release_date')
        return self.generate_movie_dataframe()
   
   


 
