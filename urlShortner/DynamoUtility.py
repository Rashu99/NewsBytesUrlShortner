from boto3.dynamodb.conditions import Key, Attr
import datetime
import pandas as pd
import simplejson
from decimal import Decimal
import json

from urlShortner.DynamoBase import DynamoDB

"""
    This is Generic Utility class for performing Dynamo Operations.
    One can Perform :-
        1. Get the meta info about table
        2. Single read/write operation
        3. Perform batch write operation
        4. perform batch delete operation
        5. serializer/de-serializer

    You can also Specify region, access_key_id and secret_access_key

                :) :) :) :) :)
"""


class DynamoUtility:

    def __init__(self, region_name='ap-south-1', aws_access_key_id=None, aws_secret_access_key=None):
        dynamoDB = DynamoDB(region_name=region_name, aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        self.conn = dynamoDB.getConnection()

    def get_table_meta_data(self, table_name: str):
        """
            This function will returns the meta data for the table
        """
        table = self.conn.Table(table_name)

        return {
            'num_items': table.item_count,
            'primary_key_name': table.key_schema[0],
            'status': table.table_status,
            'bytes_size': table.table_size_bytes,
            'global_secondary_indices': table.global_secondary_indexes
        }

    def perform_write_operation(self, table_name: str, data: dict):
        """
            This Function Writes single row
            Input is dictionary with Primary Key mandatory
            PrimaryKey - (Partition Key + Sort Key(Optional))
        """
        table = self.conn.Table(table_name)
        resp = table.put_item(Item=data)
        return resp

    def perform_delete_operation(self, table_name: str, key_dict: dict):
        """
            This Function performs single delete Operation
            Input is dictionary which should contain Primary Key
            PrimaryKey - (Partition Key + Sort Key(Optional))
        """
        table = self.conn.Table(table_name)
        resp = table.delete_item(key=key_dict)
        return resp

    def perform_query_with_user_defined(self, table_name: str, query_dict: dict):
        table = self.conn.Table(table_name)
        response = table.query(**query_dict)
        return response

    def perform_query_on_table(self, table_name: str, key: str, val, consistentRead: bool = False,
                               scanIndexForward: bool = True):
        """
            This Function performs the simple query based on Partition Key / Primary Key only
            Input is Key and value
            Optional Inputs :-
            consistentRead - Takes Two values
                             True - StronglyConsistentRead
                             False - EventuallyConsistentRead

                StronglyConsistentRead - When you request a strongly consistent read, DynamoDB returns a response with
                                         the most up-to-date data, reflecting the updates from all prior write
                                         operations that were successful.
                EventuallyConsistentRead - When you read data from a DynamoDB table, the response might not reflect the
                                           results of a recently completed write operation.

            scanIndexForward - Takes Two values
                                True - Give results in ascending order of sort key
                                False - Give results in descending order of sort key
        """
        table = self.conn.Table(table_name)
        response = table.query(
            ConsistentRead=consistentRead,
            KeyConditionExpression=Key(key).eq(val),
            ScanIndexForward=scanIndexForward,

        )
        return response

    @staticmethod
    def serialize_datetime(data: dict) -> dict:
        for i, v in data.items():
            if isinstance(v, datetime.datetime) or isinstance(v, datetime.time):
                if not pd.isnull(v):
                    data[i] = v.strftime('%Y-%m-%d:%H:%M:%S')
                else:
                    data[i] = None
        each_item_dump = simplejson.dumps(data, ignore_nan=True)
        dict_serialized = json.loads(each_item_dump, parse_float=Decimal)
        return dict_serialized

    @staticmethod
    def deserialize_datetime(data: dict, date_col_name: list = None) -> dict:
        each_item_dump = simplejson.dumps(data)
        dict_deserialized = json.loads(each_item_dump)
        if date_col_name is None:
            return dict_deserialized
        for i, v in dict_deserialized.items():
            if i in date_col_name:
                if not pd.isnull(v):
                    dict_deserialized[i] = datetime.datetime.strptime(v, '%Y-%m-%d:%H:%M:%S')
        return dict_deserialized
