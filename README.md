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
2.-The repo includes a sample jsonl file called elasticsearch.jsonl. It is a sample search index for testing purposes. Use `curl -XPOST "http://localhost:9200/mfiles/mfile/_bulk?pretty" --data-binary  @elasticsearch.jsonl` to index the data in elasticsearch.jsonl. <br>
3.-Use `virtualenv venv` to set up your virtualenv. Activate it using `. venv/bin/activate`<br>
4.-In case you don't have Flask and the Flask ElasticSearch client, use:
```
pip install Flask
pip install Flask-Elasticsearch
```
<br>
5.-Once you have that, start your Elasticsearch copy in another terminal window. Back where you have your virtual environment, do:
```
export FLASK_APP=mapi.py
flask run
```
<br>
This will start the app. <br>
6.-Open your browser and go to `http://127.0.0.1:5000/` to see the API response.  


