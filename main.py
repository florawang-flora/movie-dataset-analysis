import pandas as pd
from raw.base_adapter import BaseAdapter
from raw.keywords_adapter import KeywordsAdapter
from raw.cast_adapter import CastApater
from raw.crew_adapter import CrewAdapter
from raw.genre_adapter import GenreAdapter
from raw.movie_adpater import MovieAdapter
from tools.load_config import load_conf
from database.database_adapter import Database
from ingestion.movie_ingestion import MovieIngestion
from ingestion.cast_ingestion import CastIngestion
from ingestion.crew_ingestion import CrewIngestion
from ingestion.mapping_ingestion import MappingIngestion

#adapter_keywords = KeywordsAdapter('src/keywords.csv','keywords')
#adapter_keywords.process()

# cast 
#adapter_cast = CastApater('src/credits.csv','cast')
#adapter_cast.process()

# crew 
#adapter_crew = CrewAdapter('src/credits.csv','crew')
#adapter_crew.process()

# genres 
#adapter_genres = GenreAdapter('src/movies_metadata.csv','genres')
#adapter_genres.process()


# movie adapter 
#adapter_crew = MovieAdapter('src/movies_metadata.csv','movie')
#adapter_crew.process()




#rating adapter
# links adapter 
#adapter_rating = BaseAdapter('src/ratings_small.csv','ratings')
#adapter_rating.generate_df()


# links adapter 
#adapter_links = BaseAdapter('src/links_small.csv','links')
#link_df = adapter_links.generate_df()

# take the link information to the database. 
#oad_config = load_conf()
# take the sqlite_url 
#sqlite_url = load_config['sqlite_url']

##database = Database(sqlite_url, link_df , 'link')
#database.execute_sql()

def main():
    config = load_conf()
    data_source= config['data_source']
    movies = data_source['movies']
    # raw_movie
    raw_adapter_movie = MovieAdapter(movies['path'],movies['table_name'])
    raw_movie_df = raw_adapter_movie.process()

    # MOVIE TABLE 
    movie_object = MovieIngestion(raw_movie_df)
    movie_df = movie_object.run()



    ## CAST TABLE 
    # raw_cast
    casts = data_source['casts']
    raw_cast= CastApater(casts['path'], casts['table_name'])
    raw_cast_df, raw_movie_cast_df = raw_cast.process()
    # print(raw_cast_df)
    #print(raw_movie_cast_df)
    
    # movie_cast_table 
    movie_cast_object = MappingIngestion(raw_movie_cast_df)
    movie_cast_df  = movie_cast_object.process()
    #print('hhhhh ', movie_cast_df)
    # cast_df
    cast_object = CastIngestion(raw_cast_df)
    cast_df = cast_object.process()

    # CREW TABLE
    crew = data_source['crew']
    raw_crew = CrewAdapter(crew['path'], crew['table_name'])
    raw_crew_df,raw_movie_cast_df= raw_crew.process()
    # crew_df 
    crew_object = CrewIngestion(raw_crew_df)
    crew_df = crew_object.process()

    # put these movie, cast, crew and mapping tabel to the database. 


    prosgre_url = config['postgresql_url']

    movie_database=Database(prosgre_url, raw_crew_df , 'movie')
    movie_database.generate_sql_table()
    
    crew_database=Database(prosgre_url, raw_crew_df , 'crew')
    crew_database.generate_sql_table()

    cast_database=Database(prosgre_url, raw_cast_df , 'cast')
    cast_database.generate_sql_table()

    movie_cast_database=Database(prosgre_url, raw_movie_cast_df , 'movie_cast_mapping')
    movie_cast_database.generate_sql_table()

    movie_crew_database=Database(prosgre_url, raw_cast_df , 'movie_crew_mapping')
    movie_crew_database.generate_sql_table()





    






    #raw_movies_df = raw_adapter_movie.df

    #curated_movie = CurateMovies(raw_movies_df)
    #curated_movie.run()


    ## cast 
    #cast = data_source['cast']
    #raw_adapter_cast = MovieAdapter(cast['path'],cast['table_name'])
    #raw_adapter_cast.process()
    

if __name__ == '__main__':
    main()








