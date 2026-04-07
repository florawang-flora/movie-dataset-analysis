from ingestion.keywords_adapter import KeywordsAdapter 

def test_load_data():
    adapter = KeywordsAdapter('src/keywords.csv')
    keywords_files = adapter.load_data()
    print(keywords_files.shape)
    assert keywords_files is not None 
    assert len(keywords_files)> 0

def test_check_data_dulplicates():
    adapter = KeywordsAdapter('src/keywords.csv')
    adapter.load_data()
    print(adapter.check_data_dulplicates())
    assert adapter.check_data_dulplicates() is not None


def test_clean_data_dulplicates():
    adapter = KeywordsAdapter('src/keywords.csv')
    original_files = adapter.load_data()
    print(original_files.shape)
    clean_raw_files = adapter.clean_data_dulplicates()


def test_flatten_data():
    adapter = KeywordsAdapter('src/keywords.csv')
    original_files = adapter.load_data()
    clean_raw_files = adapter.clean_data_dulplicates()
    adapter.flatten_data(clean_raw_files)

def test_process():
    adapter = KeywordsAdapter('src/keywords.csv')
    adapter.process()


   
    
    
    
    
