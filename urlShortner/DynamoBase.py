import boto3
from decimal import Decimal
import json
import datetime
import pandas as pd
import simplejson
from botocore.config import Config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DynamoDB(metaclass=Singleton):

    def __init__(self, region_name='ap-south-1', aws_access_key_id=None, aws_secret_access_key=None):
        config = Config(
            retries=dict(
                max_attempts=5
            )
        )
        self.dynamodb = boto3.resource(
            'dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key, config=config
        )

    def getConnection(self):
        return self.dynamodb

    def _serialize_(self, dict):
        for i, v in dict.items():
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.time):
                if not pd.isnull(v):
                    dict[i] = v.strftime('%Y-%m-%d')
                else:
                    dict[i] = None
        each_item_dump = simplejson.dumps(dict, ignore_nan=True)
        dict_serialized = json.loads(each_item_dump, parse_float=Decimal)
        return dict_serialized
