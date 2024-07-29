import pandas as pd
import boto3

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
    # Test the DataLoader
    aws_session = boto3.Session()
    loader = DataLoader(aws_session)

    # Test loading from S3
    # df_s3 = loader.load_from_s3('your_bucket_name', 'your_file_key', 'csv')
    # print(df_s3.head())

    # Test loading from local
    df_local = loader.load_from_local('path_to_your_file.csv', 'csv')
    print(df_local.head())
