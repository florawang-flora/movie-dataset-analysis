import ast
import os
import pandas as pd 
from sqlalchemy import create_engine
class Utils: 
      @staticmethod
      def parse(x: str):
            if isinstance(x,str):
                  return ast.literal_eval(x)
            else: 
                  return []
      
      @staticmethod
      def export_tables_to_csv(database_url,tables,export_folder="export"):
        """
        Export PostgreSQL tables to CSV files.

        Parameters:
            database_url: PostgreSQL connection URL
            tables: a list of table names
            export_folder: folder used to store CSV files
        """

        # Create the PostgreSQL connection engine
        engine = create_engine(database_url)

        # Make sure the export folder exists
        os.makedirs(export_folder, exist_ok=True)

        # Export each PostgreSQL table to a CSV file
        for table in tables:
            try:
                # Read the PostgreSQL table into a DataFrame
                query = f'SELECT * FROM "{table}"'
                df = pd.read_sql(query, engine)

                # Create the CSV file path
                file_path = os.path.join(
                    export_folder,
                    f"{table}.csv"
                )

                # Export the DataFrame to CSV
                df.to_csv(
                    file_path,
                    index=False,
                    encoding="utf-8"
                )

                print(
                    f"{table}: {len(df)} rows exported to {file_path}"
                )

            except Exception as error:
                print(f"{table}: export failed")
                print(error)

        # Close the database connections
        engine.dispose()

        print("CSV export process finished.")               