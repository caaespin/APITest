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
<br>
1.-Download this repo by using `git clone https://github.com/caaespin/APITest.git`<br>
2.-In case you don't have Flask and the Flask ElasticSearch client, you can use `make getFlask` to do so. This will also set up your virtual environment, so you can skip to step 4.<br>
3.-Use `virtualenv venv` to set up your virtualenv. <br>
4.-The repo includes a sample jsonl file called elasticsearch.jsonl. It is a sample search index for testing purposes. Use `make index` to index the data in elasticsearch.jsonl. <br>
5.-Once you have that, start your Elasticsearch copy. In another terminal window, run `make runapp`. This will start the virtual environment and start the app for you. <br>
6.-Open your browser and go to `http://127.0.0.1:5000/` to see the API response.  


