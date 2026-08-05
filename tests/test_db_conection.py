from database.database_handler import Database
from tools.load_config import load_conf
config = load_conf()
prosgre_url = config['postgresql_url']
db = Database(prosgre_url)

def test_get_db():
    rows = db.run_query("SELECT * FROM movie LIMIT 3")
    for row in rows:
        print(row)

    # python3 -m tests.test_db_connection()
    # it works

def movies_by_actor(actor_name): 
    sql = """
        SELECT m.movie_title, m.release_date
        FROM movie m
        JOIN cast_movie cm ON m.tmdb_id = cm.tmdb_id
        JOIN cast_table c  ON cm.actor_id = c.actor_id
        WHERE c.cast_name ILIKE :name
        ORDER BY m.release_date;
    """
    rows =  db.run_query(sql, {"name": f"%{actor_name}%"})
    for row in rows:
        print(row)

if __name__ == '__main__':
    movies_by_actor('Sophia Loren')