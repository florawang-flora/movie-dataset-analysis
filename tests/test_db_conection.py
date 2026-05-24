# test_db_connection.py
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:123@localhost:5432/postgres")

with engine.begin() as conn:
    result = conn.execute(text("SELECT 1 + 1 AS answer"))
    print(result.fetchone())