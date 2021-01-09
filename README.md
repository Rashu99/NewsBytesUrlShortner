# NewsBytesUrlShortner

This Projects Provide two get API ---->
  1. Get Short Url from Long Url
  2, Get Long Url from Short Url

This Project only handles the url with BASE URL = https://www.newsbytesapp.com/

Two APIs ---->
   {{host}}/api/v1/urlShortner/tiny-url?long_url=https://www.newsbytesapp.com/......
   {{host}}/api/v1/urlShortner/long-url?short_url=https://www.newsbytesapp.com/......
   
# Method and Technology

I have used md5 hash to generate unique identifoer for each url, chances of collision of md5 hash is approximately: 1.47*10-29

Used DynamoDB to store tiny_url and long_url
DynamoDB ---- primary_key -- tiny_url

Used NoSQL DB for scalability and as no SQL operations are required

Project is in Django

Sample:--

Long URL --- http://127.0.0.1:8000/api/v1/urlShortner/tiny-url?long_url=https://www.newsbytesapp.com/communication/advisoryCards/103566021?referrer=utm_source%3Dadvisory%26utm_medium%3Demail%26utm_campaign%3DVGQMStockRecommendation&utm_source=advisory&utm_medium=email&utm_campaign=VGQMStockRecommendation&dynamo_id=2021-01-06%3A19%3A09%3A25%231063%23%23%23258385

Short URL---- https://www.newsbytesapp.com/7add93bc704563c3e246393c9b22351e

