import pandas as pd
import os
from datetime import datetime
import psycopg2
import mysql.connector
import boto3
from GTI.auth_handler import RedshiftAuth

class Redshift:
    def __init__(self, use_connection_pooling=True):
        self.auth = RedshiftAuth()
        self.conn = self.auth.get_connection()
        self.use_connection_pooling = use_connection_pooling

    def run_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        if not self.use_connection_pooling:
            self.conn.close()
        return pd.DataFrame(rows, columns=columns)

    def read_query(self, query):
        return self.run_query(query)

    def write_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
        if not self.use_connection_pooling:
            self.conn.close()

class DataSaver:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir

    def save_data(self, dataframes, file_format="parquet"):
        today = datetime.now()
        year, month, day = today.year, today.month, today.day
        dir_path = os.path.join(self.base_dir, f"{year}", f"{month:02d}", f"{day:02d}")
        os.makedirs(dir_path, exist_ok=True)
        
        for df_name, df in dataframes.items():
            file_path = os.path.join(dir_path, f"{df_name}.{file_format}")
            if file_format == "parquet":
                df.to_parquet(file_path)
            elif file_format == "csv":
                df.to_csv(file_path, index=False)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            print(f"Saved {df_name} to {file_path}")

class DataLoader:
    def __init__(self, aws_session=None):
        self.s3_client = aws_session.client('s3') if aws_session else None

    def load_from_s3(self, bucket_name, file_key, file_format):
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        if file_format == 'csv':
            return pd.read_csv(obj['Body'])
        elif file_format == 'parquet':
            return pd.read_parquet(obj['Body'])

    def load_from_local(self, file_path, file_format):
        if file_format == 'csv':
            return pd.read_csv(file_path)
        elif file_format == 'parquet':
            return pd.read_parquet(file_path)

if __name__ == "__main__":
    handler = Redshift()
    query = "SELECT * FROM your_table_name LIMIT 10"
    df = handler.run_query(query)
    print(df)
