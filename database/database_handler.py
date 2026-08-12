# database/database_adapter.py
from sqlalchemy import create_engine, text,inspect


class Database:
    """
    Database handler.
    Responsibilities:
      1. Manage the database connection (engine).
      2. Execute DDL statements to create the schema.
      3. Load DataFrames into existing tables.
    """

    def __init__(self, url):
        # Create the SQLAlchemy engine.
        # Note: this does NOT open a real connection yet.
        # The actual connection is opened when a query is executed.
        self.engine = create_engine(url)

    def execute_ddl(self, ddl_file_path):
        """
        Execute the DDL file to create tables, indexes, and constraints.
        Should be run once before loading any data.
        """
        # Read the SQL script from disk
        with open(ddl_file_path, 'r') as f:
            ddl_sql = f.read()

        # Open a transactional connection.
        # If any statement fails, all changes are rolled back automatically.
        with self.engine.begin() as conn:
            # Split the script into individual statements by ';'
            for stmt in ddl_sql.split(';'):
                # Skip empty lines / trailing whitespace
                if stmt.strip():
                    conn.execute(text(stmt))

        print("DDL executed successfully")

    def load_dataframe(self, df, table_name):
        """
        Append a DataFrame into an existing table.
        IMPORTANT: use 'append' instead of 'replace'.
        'replace' would drop the table and lose all PK / FK / CHECK constraints
        defined in the DDL.
        """
        df.to_sql(
            name=table_name,
            schema = 'public',
            con=self.engine,
            if_exists='append',   # keep the schema, only insert rows
            index=False,          # do not write the DataFrame index as a column
            method='multi',       # batch insert, much faster
            chunksize=1000       
        )
        print(f"Inserted {len(df)} rows into {table_name}")

    def table_exists(self, table_name, schema="public"):
        """
        Check whether a table exists in the specified database schema.

        Returns:
        True if the table exists.
        False if the table does not exist.
        """

        # Create a SQLAlchemy inspector to examine the database structure
        inspector = inspect(self.engine)
        # Check whether the specified table exists in the given schema
        has_table = inspector.has_table(table_name=table_name,schema=schema)
        return has_table
    
    def run_query(self, sql, params=None ):
        # open the conection 
        conn = self.engine.connect()
        # run the query 
        results = conn.execute(text(sql), params or {})
        rows = []
        # install as list of dict. 
        for row in results: 
            rows.append(dict(row._mapping))
        # close the conection 
        conn.close()
        return rows 
  
