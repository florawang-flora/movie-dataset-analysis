# export_csv.py
import os
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("postgresql://postgres:123@localhost:5432/postgres")

# make sure the export folder exists 
os.makedirs('export', exist_ok=True)

# export the database data to csv file.
tables = ['movie', 'cast_table', 'crew', 'movie_cast', 'movie_crew']

for table in tables:
    try:
        df = pd.read_sql(f"SELECT * FROM {table}", engine)
        path = f'export/{table}.csv'
        df.to_csv(path, index=False)
        print(f"{table}: {len(df)} rows → {path}")
    except Exception as e:
        print(f"{table}: {e}")