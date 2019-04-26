import requests
import json
from elasticsearch import Elasticsearch
from pprint import pprint
import yaml
import ast

#This function connects to ElasticSearch on the localhost on port 9200
def establish_ES_connection():

	es = Elasticsearch([{'host': 'localhost',
						 'port': 9200
						}])

	return es

#Quickly tests whether the ElasticSearch connection is successful
def test_ES_connection():

	req = requests.get('http://localhost:9200')

	content = req.content

	parsed = json.loads(content)

	print_response(parsed)

#function to print the response in a easily-readible format
def print_response(response):
	print(json.dumps(response, indent=4, sort_keys=True))

#Check whether a document on a particular Index exists already
def document_exists(es, index, doc_id, doc_type):
	pass

#If the document exists already, update the document where the doc_id's are the same
def update_authors_document(es, index, doc_id, doc_type, data):
	
	new_data = {}

	#Need to add this argument to solve update/upsert issues if document does not exist
	#new_data['scripted_upsert'] = True

	#We also need to add a script to the JSON to check and add the associated data appropriately
	new_data['script'] = {
					"source": "ctx._source.papers.add(params.new_papers); ctx._source.papers.add(params.new_clusters)",
					"lang": "painless",
					"params": {
						"new_papers": data['papers'][0],
						"new_clusters": data['clusters'][0]
					}
	 }

	new_data['upsert'] = {
					"papers": data['papers'],
					"author_id": data['author_id'],
                                        "cluster": data['clusters'],
                                        "name": data['name'],
					"affiliation": data['affiliation'],
					"address": data['address'],
					"email": data['email']

	}

	#Update the specific document located by the ID
	
	#new_data = ast.literal_eval(json.dumps(new_data))	

	update1 = es.update(index=index, doc_type=doc_type, id=doc_id,
						body=new_data)

def update_clusters_document(es, index, doc_id, doc_type, data):

	new_data = {}

	new_data['script'] = {
					"source": "ctx._source.included_papers.add(params.new_papers); ctx._source.included_authors.add(params.new_authors)",
					"lang": "painless",
					"params": {
						"new_papers": data['included_papers'][0],
						"new_authors": data['included_authors']
					}
	}


	new_data['upsert'] = {
					"cluster_id": data['cluster_id'],
					"included_papers": data['included_papers'],
					"included_authors": data['included_authors']
	}


	update1 = es.updated(index=index, doc_type=doc_type, doc_id=doc_id, body=new_data)
	

#If the document does not exist, create it in the proper index
def create_document(es, index, doc_id, doc_type, data):

	#Begin indexing the data in the correct index
	
	index1 = es.index(index=index, id=doc_id, doc_type=doc_type, body=data)





