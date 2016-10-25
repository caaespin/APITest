#--------------------------------------------------------------------
#	Makefile for testing purposes only
#	Assumes you already have elasticSearch installed. 
#	
#	getFlask: sets up virtualenv, and installs Flask and Flask-Elasticsearch
#
#	runapp: sets up the virtualenv and runs the app. 
#--------------------------------------------------------------------

getFlask:
	virtualenv venv
	. venv/bin/activate
	pip install Flask
	pip install Flask-Elasticsearch

runapp:
	. venv/bin/activate
	export FLASK_APP=mapi.py
	flask run

index:
	curl -XPOST "http://localhost:9200/mfiles/mfile/_bulk?pretty" --data-binary  @elasticsearch.jsonl

