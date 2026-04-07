import pandas as pd
import ast 
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
    def __init__(self,path):
        # input is a path for the data source.
        self.path = path 
        self.files = None
        # output is a dataframe.
        self.df = None
    def load_data(self):
        '''
        This method is to load data from the data source. 
        ''' 
        raise NotImplementedError("The load data method you hasn't been implemented yet. Please go to subclass to implement your adaptor.") 
    def clean_data(self): 
        """
        This method is to flatten the data for the specific data frame. 
        """
        raise NotImplementedError("The clean data method you hasn't been implemented yet. Please go to subclass to implement your adaptor.")
    def process(self):
        '''
        1.load the data from the data source
        2, check the dulplicate rows for it 
        3. clean the data dulplicate row . 
        4, flatten the data for the specific data frame.
    
        '''
        self.load_data()
        self.clean_data()
        return self.df 





