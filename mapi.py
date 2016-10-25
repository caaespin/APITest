from flask import Flask, jsonify
#import the FlaskElasticsearch package
from flask.ext.elasticsearch import Elasticsearch
#import json

app = Flask(__name__)
es = Elasticsearch()

#Assumption: objectId is download_id
#Parses the elasticSearch response and makes it as similar as possible to the ICGC Data
#Portal. String "DUMMY" is used when no data for that field is available.
def parse_ES_response(es_dict):
	#print es_dict
	protoDict = {'hits':[]}
	for hit in es_dict['hits']['hits']:
		protoDict['hits'].append({
			'id' : 'DUMMY',
			'objectID' : 'DUMMY',
			'access' : 'DUMMY',
			'study' : ['DUMMY'],
			'dataCategorization' : {
				'dataType' : hit['_source']['analysis_type'],
				'experimentalStrategy' : 'DUMMY'
			},
			'fileCopies' : [{
				'repoDataBundleId' : 'DUMMY',
				'repoDataSetIds' :[],
				'repoCode' : 'DUMMY',
				'repoOrg' : 'DUMMY',
				'repoName' : 'DUMMY',
				'repoType' : 'DUMMY',
				'repoCountry' : 'DUMMY',
				'repoBaseUrl' : 'DUMMY',
				'repoDataPath' : 'DUMMY',
				'repoMetadatapath' : 'DUMMY',
				'indexFile' : {
					'id' : 'DUMMY',
					'objectId' : hit['_source']['download_id'],
					'fileName' : hit['_source']['title'],
					'fileFormat' : hit['_source']['file_type'],
					'fileMd5sum' : 'DUMMY',
					'fileSize' : 'DUMMY'
				},
				'fileName' : hit['_source']['title'],
				'fileFormat' : hit['_source']['file_type'],
				'fileMd5sum' : 'DUMMY',
				'lastModified' : 'DUMMY'
			}],
			'donors' : [{
				'donorId' : hit['_source']['donor'],
				'primarySite' : 'DUMMY',
				'projectCode' : hit['_source']['project'],
				'study' : 'DUMMY',
				'sampleId' : ['DUMMY'],
				'specimenType' : [hit['_source']['specimen_type']],
				'submittedDonorId' : "DUMMY",
				'submittedSampleId' : ['DUMMY'],
				'submittedSpecimenId' : ['DUMMY'],
				'otherIdentifiers' : {
					'tcgaSampleBarcode' : ['DUMMY'],
					'tcgaAliquotBarcode' : ['DUMMY']
				}

			}],

			'analysisMethod' : {
				'analysisType' : hit['_source']['analysis_type'],
				'software' : 'DUMMY'
			},
			'referenceGenome' : {
				'genomeBuild' : 'DUMMY',
				'referenceName' : 'DUMMY',
				'downloadUrl' : 'DUMMY'
			}
		})
		#print hit
	#print protoDict

	protoDict['pagination'] = {
		'count' : 25,
		'total' : es_dict['hits']['total'],
		'size' : 25,
		'from' : 1,
		'page' : 1,
		'pages' : -(-es_dict['hits']['total'] // 25),
		'sort' : 'DUMMY',
		'order' : 'desc'
	}

	protoDict['termFacets'] = es_dict['aggregations']

	#func_total = lambda x: x+x
	#Get the total for all the terms
	for section in protoDict['termFacets']:
		m_sum = 0
		print section
		for bucket in protoDict['termFacets'][section]['buckets']:
			m_sum += bucket['doc_count']
			#func_total(bucket['doc_count'])
		protoDict['termFacets'][section]['total'] = m_sum


	return protoDict

#This returns the agreggate terms and the list of hits from ElasticSearch
@app.route('/')
def get_data():
	mText = es.search(index='mfiles', body={"query": {"match_all": {}}, "aggs" : {
        "dataType" : {
            "terms" : { "field" : "analysis_type",
                        "size" : 9999}           
        },
        "projectCode":{
            "terms":{
                "field" : "project",
                "size" : 99999
            }
        },
        "specimenType":{
            "terms":{
                "field" : "specimen_type",
                "size" : 99999
            }
        },
        "fileFormat":{
            "terms":{
                "field" : "file_type",
                "size" : 99999
            }
        }
    }}, size=25)
	#print mText
	return jsonify(parse_ES_response(mText))

