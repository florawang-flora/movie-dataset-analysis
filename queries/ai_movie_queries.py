from database.database_handler import Database
from tools.load_config import load_conf

class MovieQueries:
    def __init__(self): 
        config = load_conf()
        prosgre_url = config['postgresql_url']
        self.db = Database(prosgre_url)

    def movie_by_cast(self, actor_name): 
        sql = """
            SELECT m.movie_title, m.release_date
            FROM movie m
            JOIN cast_movie cm ON m.tmdb_id = cm.tmdb_id
            JOIN cast_table c  ON cm.actor_id = c.actor_id
            WHERE c.cast_name ILIKE :name
            ORDER BY m.release_date;
        """
        rows = self.db.run_query(sql, {"name": f"%{actor_name}%"})
        #for row in rows:
        #   print(row)
        return rows

    # function2 
    def get_all_overviews(self, limit = None): 
        # if limit = 100, the number of people will think about 
        """
        Get movie overviews for the text analsyis.
        """
        sql = '''
        SELECT movie_title, overview 
        FROM movie
        WHERE overview IS NOT NULL and overview != ''
        '''
        params = {}
        if limit is not None: 
            sql += '\n LIMIT :limit'
            params = {'limit' : limit }

        rows = self.db.run_query(sql, params)  
        return rows
        

