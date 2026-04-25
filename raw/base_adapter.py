import pandas as pd
from abc import abstractmethod
class BaseAdapter:
    '''
    BaseAdaptor is an abstract class that defines the interface for all adaptors.
    # this is to define the rule for the keywords_adaptor, movie_adaptor
    This will define there are 3 things need to follow.
    Process:  
    1. load the data from the data source. 
    2. clean the dulplicate row for it. 
    3. flatten the data for the specific dat frame. 

    input: self.data_source: the data source for the adaptor.
    output: self.data_frame: the data frame for the adaptor.

    '''
    def __init__(self,path,filename):
        # input is a path for the data source.
        self.path = path 
        self.files = None
        self.filename = filename
        # output is a dataframe.
        self.df = None
        # This is for the movie cast table 
        # This is for the movie crew table
        self.movie_cast_df = None
        self.movie_crew_df = None
    def _load_data(self):
        '''
        This method is to load the data from the csv 
        '''
        # If we meet bad data, I'll skip the line first, then add it later. 
        self.files = pd.read_csv(self.path)
        rows,columns = self.files.shape
        print(f'There are {rows} rows and {columns} columns in the file.')
        print('Loading data...')
        return self.files 
                     
    def _check_data_dulplicates(self): 
        """
        This method is check whether we have the dulicate data in the data frame. 
        """
        print('Checking...')
        check_dulpliciated_rows = self.files.duplicated().sum()
        if check_dulpliciated_rows >= 0:
                print(f'There are {check_dulpliciated_rows} duplicate rows in the data frame.')
                print('Going to clean the data')
        else:
                print('Data is tidy')
                rows, columns = self.files.shape
                print(f'There are {rows} rows and {columns} columns in the data frame.')
        return check_dulpliciated_rows
                 
    def _clean_data_dulplicates(self):
            """
            This method is to clean the dulplicate data in the data frame. 
            """
            
            clean_raw_files = self.files.drop_duplicates()
            new_files_rows, new_files_columns = clean_raw_files.shape
            rows, columns = self.files.shape
            print(f'Before: thre are {rows} rows and {columns} columns in the data frame.')
            print(f'After: thre are {new_files_rows} rows and {new_files_columns} columns in the data frame.')
            print('Initial cleaning finished!')
            self.df = clean_raw_files 
            return self.df
        


    # this is the method for the csv file which doesn't have any nested arraay.    
    def generate_df(self):
        self._load_data()
        print(f'Here is {self.files} file datatype information :/n {self.files.info()}')
        print(f'Here is the example of the {self.files} dataset:/n {self.files.head(3)} ')
        return self.files
    
    @abstractmethod
    def flatten_data(self):
          pass 

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





