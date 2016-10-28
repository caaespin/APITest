from flask import Flask, jsonify, request
#import the FlaskElasticsearch package
from flask.ext.elasticsearch import Elasticsearch
#import json
import ast

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
		'count' : len(es_dict['hits']['hits']),#25,
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
		#print section
		for bucket in protoDict['termFacets'][section]['buckets']:
			m_sum += bucket['doc_count']
			#func_total(bucket['doc_count'])
		protoDict['termFacets'][section]['total'] = m_sum


	return protoDict

#This returns the agreggate terms and the list of hits from ElasticSearch
@app.route('/files/')
def get_data():
	#Get all the parameters from the URL
	m_field = request.args.get('field')
	m_filters = request.args.get('filters')
	m_From = request.args.get('from', 1, type=int)
	m_Size = request.args.get('size', 25, type=int)
	m_Sort = request.args.get('sort', 'center_name')
	m_Order = request.args.get('order', 'desc')

	#Will hold the query that will be used when calling ES
	mQuery = {}
	print m_filters
	#print dict(m_filters)
	#print m_filters['file']
	#get a list of all the fields requested
	try:
		m_fields_List = [x.strip() for x in m_field.split(',')]
	except:
		m_fields_List = None
	print m_fields_List
	#Get a list of all the Filters requested
	try:
		m_filters = ast.literal_eval(m_filters)
		filt_list = [{"match":{x:y['is'][0]}} for x,y in m_filters['file'].items()]
		mQuery = {"bool":{"must":filt_list}}
		print filt_list	
		print mQuery	
		#print m_filters['file']
		#pass
	except:
		m_fields_List = None
		mQuery = {"match_all":{}}
		pass
	mText = es.search(index='mfiles', body={"query": mQuery, "aggs" : {
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
    }, "fields":m_fields_List}, from_=m_From, size=m_Size, sort=m_Sort+":"+m_Order)
	#return jsonify(mText)
	return jsonify(parse_ES_response(mText))

