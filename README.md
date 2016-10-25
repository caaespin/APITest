# APITest
Simple Flask web service to communicate with ElasticSearch and output the list of results in JSON format. <br>

<h2>Instructions</h2>
***Assumptions***<br>
-You have ElasticSearch 2.4.1 installed<br>
-You have virtualenv installed<br>
<br>In case you don't have virtualenv installed, you can do so by:<br>
```
sudo easy_install virtualenv
```
Download this repo by using `git clone https://github.com/caaespin/APITest.git`<br>
Run `make getFlask` to get your virtualenv running and install Flask and Flak-Elasticsearch (ElasticSearch Python clinet). <br>
The repo includes a sample jsonl file called elasticsearch.jsonl. It is a sample search index for testing purposes. Use `make index` to index the data in elasticsearch.jsonl. <br>
Once you have that, start Elasticsearch. In another terminal window, run `make runapp`. Open your browser and go to `http://127.0.0.1:5000/` to see the API response.  

`sudo pip`

