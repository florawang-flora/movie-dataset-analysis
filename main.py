import pandas as pd
from ingestion.base_adapter import BaseAdapter
from ingestion.keywords_adapter import KeywordsAdapter
from ingestion.cast_adapter import CastApater
from ingestion.crew_adapter import CrewAdapter
from ingestion.genre_adapter import GenreAdapter
from ingestion.movie_adpater import MovieAdapter
from tools.load_config import load_conf
from database.database_adapter import Database
from curation.curation_movies import CurateMovies
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
adapter_links = BaseAdapter('src/links_small.csv','links')
link_df = adapter_links.generate_df()

# take the link information to the database. 
load_config = load_conf()
# take the sqlite_url 
sqlite_url = load_config['sqlite_url']

database = Database(sqlite_url, link_df , 'link')
database.execute_sql()

def main():
    config = load_conf()
    data_source= config['data_source']
    #movies = data_source['movies']
    #raw_adapter_movie = MovieAdapter(movies['path'],movies['table_name'])
    #raw_adapter_movie.process()

    #raw_movies_df = raw_adapter_movie.df

    #curated_movie = CurateMovies(raw_movies_df)
    #curated_movie.run()


    ## cast 
    cast = data_source['cast']
    raw_adapter_cast = MovieAdapter(cast['path'],cast['table_name'])
    raw_adapter_cast.process()
    

if __name__ == '__main__':
    main()








