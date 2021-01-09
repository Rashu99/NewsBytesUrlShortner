
# Create your models here.
import datetime
from dataclasses import dataclass

@dataclass()
class Melodic:
    tiny_url: str
    long_url: str
    created: datetime

    def getData(self):
        data = dict(
            tiny_url=self.tiny_url, long_url=self.long_url, created=self.created
        )
        return data
