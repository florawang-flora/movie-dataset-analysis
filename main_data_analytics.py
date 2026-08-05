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
from curation.curation_base import BaseCuration
from curation.curation_movie import MovieCuration
from curation.curation_genre import GenreCuration
from curation.curation_cast import CastCuration
from curation.curation_crew import CrewCuration
from database.database_handler import Database


def main_data_analytics():
    config = load_conf()
    data_source= config['data_source']

    # ===============
    # movie df 
    movies = data_source['movies']
    raw_movie = MovieAdapter(movies['path'],movies['table_name'])
    raw_movie_df = raw_movie.process()

    ## movie ingestion
    movie_df_ingest = MovieIngestion(raw_movie_df)
    raw_movie_df = movie_df_ingest.run()
    print(raw_movie_df.dtypes)

    ## movie entity - curation process
    movie_entity = MovieCuration(raw_movie_df)
    movie_entity_df = movie_entity.run()
    print(f'The movie entity df data type {movie_entity_df.dtypes}')


    # we only investigate invalid 
    valid_tmdb_ids = set(movie_entity_df['tmdb_id'].astype(str).str.strip())
    print(f'There are {len(valid_tmdb_ids)} valid movie IDs')

    #==================
    # genre table 
    genres = data_source['genres']
    raw_genres = GenreAdapter(genres['path'], genres['table_name'])
    raw_genre_df = raw_genres.process()

    ##genre ingestion
    genre_df_ingestion = GenreIngestion(raw_genre_df, valid_tmdb_ids)
    raw_genre_df = genre_df_ingestion.process()
    print(f'The shape of raw genre  table   \n {raw_genre_df.shape}')

    #genre curation process

    genre_entity = GenreCuration(raw_genre_df)
    genre_entity_df, genre_movie_mapping = genre_entity.run()
    print(f'The genre entity  data type\n {genre_entity_df.dtypes}')
    print(f'The genre movie mapping table  data type \n {genre_entity_df.dtypes}')

    #==================

    # cast table 
    casts = data_source['casts']
    raw_cast= CastApater(casts['path'], casts['table_name'])
    raw_cast_df = raw_cast.process()
    print(raw_cast_df.dtypes)
    print(raw_cast_df.head())

    #cast ingestion
    cast_df_ingestion = CastIngestion(raw_cast_df,valid_tmdb_ids)
    raw_cast_df = cast_df_ingestion.process()
    print(f'The shape of raw cast  table   \n {raw_cast_df.shape}')

    cast_entity = CastCuration(raw_cast_df)
    cast_entity_df, cast_movie_mapping = cast_entity.run()
    print(f'The cast entity data type\n {cast_entity_df.dtypes}')
    print(f'The cast movie mapping table data type \n {cast_movie_mapping.dtypes}')
   
    #==================

    # crew table 
    crew = data_source['crew']
    raw_crew = CrewAdapter(crew['path'], crew['table_name'])
    raw_crew_df= raw_crew.process()

    # crew ingestion 
    crew_df_ingestion = CrewIngestion(raw_crew_df,valid_tmdb_ids)
    raw_crew_df = crew_df_ingestion.process()
    print(f'The shape of raw crew  table   \n {raw_crew_df.shape}')

    crew_entity = CrewCuration(raw_crew_df)
    crew_entity_df , crew_movie_mapping = crew_entity.run()
    print(f'The cast entity data type\n {crew_entity_df.dtypes}')
    print(f'The cast movie mapping table data type \n {crew_movie_mapping.dtypes}')

 

    # put these movie, cast, crew and mapping tabel to the database. 

    #=========================
    #postgresql
    prosgre_url = config['postgresql_url']
    db = Database(prosgre_url)


    # 2. Load dimension tables first
    # this is to check whether in the database, otherwise, not in the 
    #db.load_dataframe(movie_entity_df,  'movie')
    #db.load_dataframe(genre_entity_df,   'genre')
    #db.load_dataframe(genre_movie_mapping, 'genre_movie') 
    #db.load_dataframe(cast_entity_df,   'cast_table')
    #db.load_dataframe(cast_movie_mapping, 'cast_movie') 
    db.load_dataframe(crew_entity_df,   'crew')
    db.load_dataframe(crew_movie_mapping,   'crew_movie')

   

    tables = ['crew', 'crew_movie', 'cast_table' , 'cast_movie', 'genre', 'genre_movie']


    Utils.export_tables_to_csv(
    database_url=prosgre_url,
    tables=tables,
    export_folder="export")

 






    






    #raw_movies_df = raw_adapter_movie.df

    #curated_movie = CurateMovies(raw_movies_df)
    #curated_movie.run()


    ## cast 
    #cast = data_source['cast']
    #raw_adapter_cast = MovieAdapter(cast['path'],cast['table_name'])
    #raw_adapter_cast.process()
    

if __name__ == '__main__':
    main_data_analytics()








