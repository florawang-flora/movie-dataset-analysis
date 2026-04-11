import pandas as pd
from ingestion.base_adapter import BaseAdapter
from ingestion.keywords_adapter import KeywordsAdapter
from ingestion.cast_adapter import CastApater
from ingestion.crew_adapter import CrewAdapter
from ingestion.genre_adapter import GenreAdapter
from ingestion.movie_adpater import MovieAdapter
# keywords 
#adapter_keywords = KeywordsAdapter('src/keywords.csv','keywords')
#adapter_keywords.process()

# cast 
#adapter_cast = CastApater('src/credits.csv','cast')
#adapter_cast.process()

# crew 
#adapter_crew = CrewAdapter('src/credits.csv','crew')
#adapter_crew.process()

# genres 
#adapter_crew = GenreAdapter('src/movies_metadata.csv','genres')
#adapter_crew.process()


# movie adapter 
#adapter_crew = MovieAdapter('src/movies_metadata.csv','movie')
#adapter_crew.process()


# links adapter 
#adapter_links = BaseAdapter('src/links_small.csv','links')
#adapter_links.generate_df()


#rating adapter
# links adapter 
adapter_rating = BaseAdapter('src/ratings_small.csv','ratings')
adapter_rating.generate_df()
