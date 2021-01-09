from datetime import datetime
import hashlib
from NewsBytesUrlShortner import settings
from pytz import timezone
from urlShortner.DynamoUtility import DynamoUtility
from urlShortner.constants import BASE_URL, DYNAMODB_URL_TABLE_NAME
from urlShortner.models import Melodic


class UrlService:

    def __init__(self, url=None, input_tiny_url=None):
        self.url = url
        self.input_tiny_url = input_tiny_url

    def _generate_md5_for_url(self, url_part):
        hash_data = hashlib.md5(str(url_part).encode(encoding='UTF-8', errors='ignore')).hexdigest()
        return hash_data

    def shorten_url(self):
        url_part = str(self.url).split(BASE_URL, 1)[1]
        hash_url = self._generate_md5_for_url(url_part)
        tiny_url = hash_url
        return tiny_url

    def get_tiny_url(self):
        tiny_url = self.shorten_url()
        DynamoObj = DynamoUtility(region_name=settings.AWS_REGION,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_KEY_ID)
        response_data = DynamoObj.perform_query_on_table(DYNAMODB_URL_TABLE_NAME, "tiny_url", tiny_url, True)
        if response_data['ResponseMetadata']['HTTPStatusCode'] == 200:
            items = response_data['Items']
            if len(items) == 0:
                created = datetime.now(tz=timezone("Asia/Kolkata"))
                url_data_dict = Melodic(
                    tiny_url=tiny_url,
                    long_url=self.url,
                    created=created
                ).getData()
                serialized_data = DynamoUtility.serialize_datetime(url_data_dict)
                DynamoObj.perform_write_operation(DYNAMODB_URL_TABLE_NAME, serialized_data)
        full_tiny_url = BASE_URL + str(tiny_url)
        return full_tiny_url

    def get_long_url(self):
        exact_tiny_url = str(self.input_tiny_url).split(BASE_URL, 1)[1]
        DynamoObj = DynamoUtility(region_name=settings.ADVISORY_AWS_REGION,
                                  aws_access_key_id=settings.ADVISORY_AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.ADVISORY_AWS_SECRET_KEY_ID)
        response_data = DynamoObj.perform_query_on_table(DYNAMODB_URL_TABLE_NAME, "tiny_url", exact_tiny_url, True)
        if response_data['ResponseMetadata']['HTTPStatusCode'] == 200:
            items = response_data['Items']
            if len(items) > 0:
                long_url = items[0]['long_url']
                return long_url
        return None

    @staticmethod
    def request_data_validator(url_data):
        if str(url_data).__contains__(BASE_URL):
            return 1
        return 0
