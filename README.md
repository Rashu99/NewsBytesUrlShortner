# NewsBytes Backend Assignment | UrlShortner

<h3># Problem Statement </h3>
<p>Write a URL Shortener Service which provides below functionalities <br>
1. Get Short Url from Long Url <br>
2. Get Long Url from Short Url
</p>

<p><b>This Project also contains the utility functions for DynamoDB CRUD operation in Python</b></p>

<p> Note:- <i>This Project only handles the url having BASE URL = https://www.newsbytesapp.com/ </i></p>

<h3># Tech / Framework Used </h3>
  <ul>
  <li>Python (Django)</li>
  <li>DynamoDB</li>
  </ul>
  
<h3># APIs Details</h3>
<h4>1. Get Shorl Url</h4>
<p>

```
{{host}}/api/v1/urlShortner/tiny-url?long_url=https://www.newsbytesapp.com/......
```

</p>

<h4>2. Get Original Url</h4>
<p>

```
{{host}}/api/v1/urlShortner/long-url?short_url=https://www.newsbytesapp.com/......
```

</p>

<h3># Approach used in the Project</h3>

<p> 
<ul> 
<li>I have used md5 hash to generate unique identifoer for each url, chances of collision of md5 hash is approximately: 1.47*10-29 </li>
<li>Used DynamoDB to store tiny_url and long_url </li> 
<li>DynamoDB ---- primary_key -- tiny_url </li>
<li>Used NoSQL DB for scalability and as no SQL operations are required </li>
</ul>
</p>

<h3># Example :- </h3>

<p> Long URL --- 

```
http://127.0.0.1:8000/api/v1/urlShortner/tiny-url?long_url=https://www.newsbytesapp.com/communication/advisoryCards/103566021?referrer=utm_source%3Dadvisory%26utm_medium%3Demail%26utm_campaign%3DVGQMStockRecommendation&utm_source=advisory&utm_medium=email&utm_campaign=VGQMStockRecommendation&dynamo_id=2021-01-06%3A19%3A09%3A25%231063%23%23%23258385
```
</p>

<p>
Short URL --- 

```
https://www.newsbytesapp.com/7add93bc704563c3e246393c9b22351e
```

</p>

