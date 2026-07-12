import pandas as pd
from tools.load_config import load_conf
from tools.utils import Utils
from raw.base_adapter import BaseAdapter
from raw.keywords_adapter import KeywordsAdapter
from raw.cast_adapter import CastApater
from raw.crew_adapter import CrewAdapter
from raw.genre_adapter import GenreAdapter
from raw.movie_adpater import MovieAdapter
from database.database_adapter import Database
from ingestion.movie_ingestion import MovieIngestion
from ingestion.cast_ingestion import CastIngestion
from ingestion.crew_ingestion import CrewIngestion
from ingestion.genre_ingestion import GenreIngestion
from ingestion.mapping_ingestion import MappingIngestion
from curation.curation_base import BaseCuration
from curation.curation_movie import MovieCuration
from curation.curation_genre import GenreCuration
from database.database_handler import Database
from export_csv import export_csv

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

    # movie df 
    movies = data_source['movies']
    raw_movie = MovieAdapter(movies['path'],movies['table_name'])
    raw_movie_df = raw_movie.process()

    # movie ingestion
    movie_df_ingest = MovieIngestion(raw_movie_df)
    raw_movie_df = movie_df_ingest.run()
    print(raw_movie_df.dtypes)

    # movie entity - curation process
    movie_entity = MovieCuration(raw_movie_df)
    movie_entity_df = movie_entity.run()
    print(f'The movie entity df data type {movie_entity_df.dtypes}')


    # genre table 
    genres = data_source['genres']
    raw_genres = GenreAdapter(genres['path'], genres['table_name'])
    raw_genre_df = raw_genres.process()

    #genre ingestion
    genre_df_ingestion = GenreIngestion(raw_genre_df)
    raw_genre_df = genre_df_ingestion.process()
    print(f'The shape of  raw genre  table   \n {raw_genre_df.shape}')

    #genre curation process

    genre_entity = GenreCuration(raw_genre_df)
    genre_entity_df, genre_movie_mapping = genre_entity.run()
    print(f'The genre entity  data type\n {genre_entity_df.dtypes}')
    print(f'The genre movie mapping table  data type \n {genre_entity_df.dtypes}')




    ## CAST TABLE 
    # raw_cast
    #casts = data_source['casts']
    #raw_cast= CastApater(casts['path'], casts['table_name'])
    #raw_cast_df, raw_movie_cast_df = raw_cast.process()
    
    # movie_cast_table 
    #movie_cast_object = MappingIngestion(raw_movie_cast_df)
    #movie_cast_df  = movie_cast_object.process()
    #print(f'Here is movie cast df data source {movie_cast_df.head()}')
    # cast_df
    #cast_object = CastIngestion(raw_cast_df)
    #cast_df = cast_object.process()
    #print(f'Here is cast df data source {cast_df.head()}')


    # CREW TABLE
    #crew = data_source['crew']
    #raw_crew = CrewAdapter(crew['path'], crew['table_name'])
    #raw_crew_df,raw_movie_cast_df= raw_crew.process()
    # crew_df 
    #crew_object = CrewIngestion(raw_crew_df)
    #crew_df = crew_object.process()
    #print(f'HEre is crew_df data source{crew_df.head()}')

    # put these movie, cast, crew and mapping tabel to the database. 


    prosgre_url = config['postgresql_url']
    db = Database(prosgre_url)

    # 1. Create the schema first (run DDL)
    #db.execute_ddl('database/schema.sql')

    # 2. Load dimension tables first
    #db.load_dataframe(movie_entity_df,  'movie')
    #db.load_dataframe(genre_entity_df,   'genre')
    db.load_dataframe(genre_movie_mapping, 'genre_movie') 
    #db.load_dataframe(crew_df,   'crew')

   

    tables = ["genre", 'movie', 'genre_movie']

    Utils.export_tables_to_csv(
    database_url=prosgre_url,
    tables=tables,
    export_folder="export")

    # 3. Load mapping tables last (they depend on the dimension tables via FK)
    #db.load_dataframe(movie_cast_df, 'movie_cast')
    #db.load_dataframe(movie_crew_df, 'movie_crew')

    #movie_database=Database(prosgre_url, raw_crew_df , 'movie')
    #movie_database.generate_sql_table()
    
    #crew_database=Database(prosgre_url, raw_crew_df , 'crew')
    #crew_database.generate_sql_table()

    #cast_database=Database(prosgre_url, raw_cast_df , 'crew_df')
    #cast_database.generate_sql_table()

    #movie_cast_database=Database(prosgre_url, raw_movie_cast_df , 'movie_cast_mapping')
    #movie_cast_database.generate_sql_table()

    #movie_cast_database=Database(prosgre_url, raw_cast_df , 'movie_crew_mapping')
    #movie_cast_database.generate_sql_table()






    






    #raw_movies_df = raw_adapter_movie.df

    #curated_movie = CurateMovies(raw_movies_df)
    #curated_movie.run()


    ## cast 
    #cast = data_source['cast']
    #raw_adapter_cast = MovieAdapter(cast['path'],cast['table_name'])
    #raw_adapter_cast.process()
    

if __name__ == '__main__':
    main()








