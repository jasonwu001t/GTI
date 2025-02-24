import os
import configparser
import psycopg2
import mysql.connector
import boto3
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from ib_insync import IB

class ConfigLoader:
    def __init__(self, config_file='auth.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.get_config_path())

    def get_config_path(self):
        package_dir = os.path.dirname(__file__)
        return os.path.join(package_dir, self.config_file)

    def get_config(self, section, key):
        return os.getenv(f"{section.upper()}_{key.upper()}") or self.config.get(section, key, fallback=None)

class RedshiftAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.conn = psycopg2.connect(
            host=config_loader.get_config('Redshift', 'host'),
            user=config_loader.get_config('Redshift', 'user'),
            port=config_loader.get_config('Redshift', 'port'),
            password=config_loader.get_config('Redshift', 'password'),
            database=config_loader.get_config('Redshift', 'database')
        )

    def get_connection(self):
        return self.conn

class MySQLAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.conn = mysql.connector.connect(
            host=config_loader.get_config('MySQL', 'host'),
            user=config_loader.get_config('MySQL', 'user'),
            password=config_loader.get_config('MySQL', 'password'),
            database=config_loader.get_config('MySQL', 'database')
        )

    def get_connection(self):
        return self.conn

class DynamoDBAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.client = boto3.client(
            'dynamodb',
            aws_access_key_id=config_loader.get_config('DynamoDB', 'aws_access_key_id'),
            aws_secret_access_key=config_loader.get_config('DynamoDB', 'aws_secret_access_key'),
            region_name=config_loader.get_config('DynamoDB', 'region_name')
        )

    def get_client(self):
        return self.client

class AWSAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.session = boto3.Session(
            aws_access_key_id=config_loader.get_config('AWS', 'aws_access_key_id'),
            aws_secret_access_key=config_loader.get_config('AWS', 'aws_secret_access_key'),
            region_name=config_loader.get_config('AWS', 'region_name')
        )

    def get_session(self):
        return self.session

class BrokerAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.api_key = config_loader.get_config('Broker', 'api_key')
        self.secret_key = config_loader.get_config('Broker', 'secret_key')

    def get_headers(self):
        return {
            'API-KEY': self.api_key,
            'SECRET-KEY': self.secret_key
        }

class OpenAIAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.api_key = config_loader.get_config('OpenAI', 'api_key')

    def get_api_key(self):
        return self.api_key

class IBAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.host = config_loader.get_config('IB', 'host')
        self.port = config_loader.get_config('IB', 'port')
        self.client_id = config_loader.get_config('IB', 'client_id')

    def connect(self):
        ib = IB()
        ib.connect(self.host, int(self.port), clientId=int(self.client_id))
        return ib

class AlpacaAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.api_key = config_loader.get_config('Alpaca', 'api_key')
        self.api_secret = config_loader.get_config('Alpaca', 'api_secret')
        self.base_url = config_loader.get_config('Alpaca', 'base_url')

    def get_trading_client(self):
        return TradingClient(self.api_key, self.api_secret, paper=True)

    def get_market_data_client(self):
        return StockHistoricalDataClient(self.api_key, self.api_secret)

class BLSAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.api_key = config_loader.get_config('BLS', 'api_key')

    def get_api_key(self):
        return self.api_key

class FredAuth:
    def __init__(self):
        config_loader = ConfigLoader()
        self.api_key = config_loader.get_config('Fred', 'api_key')

    def get_api_key(self):
        return self.api_key