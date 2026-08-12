import pandas as pd
from tools.load_config import load_conf
from tools.utils import Utils
from raw.base_adapter import BaseAdapter
from raw.keywords_adapter import KeywordsAdapter
from raw.cast_adapter import CastApater
from raw.crew_adapter import CrewAdapter
from raw.genre_adapter import GenreAdapter
from raw.movie_adpater import MovieAdapter
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
from cli.chat_agent


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
   # database analysis 
    #postgresql
    prosgre_url = config['postgresql_url']
    db = Database(prosgre_url)
    schema = config["database"]['schema']
    table_to_load = config['table_to_load']
    tables = []
    missing_table_configs = []
    # add database table cmoviesonfig 
    for table_config in table_to_load: 
        table_name = table_config['table_name']
        tables.append(table_name)
        print(table_name)
        if db.table_exists(table_name,schema=schema): 
            print(f"Table '{table_name}' already exists.")
        else: 
            print(f"Table '{table_name}' does not exist.")
            missing_table_configs.append(table_config)
    available_dataframes = locals()
    
    if missing_table_configs:
        for table_config in missing_table_configs:
            table_name = table_config['table_name']
            dataframe_name = table_config['dataframe_name']
            dataframe = available_dataframes.get(dataframe_name)
            print(f"Loading Dataframe {dataframe_name} into table {schema}.{table_name}")
            db.load_dataframe(dataframe, table_name)
            print(f'Table {schema}.{table_name} loaded successfully')
    else:
        print('All required tables already exist. Nothing to load')

    Utils.export_tables_to_csv(
    database_url=prosgre_url,
    tables=tables,
    export_folder="export")
def 



## if __name__ == '__main__':
#    agent = ChatAgent()
#    print("Let's Chat! (type quite or exit to leave )\n")
#    while True: 
#        user_input = input("You: ")
#        if user_input.lower() in ('quit','exit', 'bye' ):
#            print('Goodbye!')
#            break
#        # skpit
#        if not user_input.strip():
#            continue
#        reply = agent.random_chat(user_input)
#        print(reply)

# task1 
#result = agent.search_movie("What movies did Tom Hanks appear in?")
#print(result)

if __name__ == '__main__':
    main_data_analytics()








