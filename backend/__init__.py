from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
import json
import os
import uuid
import getpass
import datetime

app = Flask(__name__, static_url_path = "")
CORS(app) # required for Cross-origin Request Sharing
api = Api(app)

myElasticServerIp = os.environ.get('ES_SERVER_IP', 'localhost')
myIndexName = os.environ.get('ES_INDEX_NAME', 'bestbuy-products')

api_base_url = '/api/v1'
es_base_url = {
    'products': 'http://' + myElasticServerIp + ':9200/' + myIndexName + '/product',
}

parser = reqparse.RequestParser()

class Healthz(Resource):
    def get(self):
        return 'OK'

api.add_resource(Healthz, api_base_url+'/healthz')

class Search(Resource):
 
    def get(self):
        startTime = datetime.datetime.today()
        # parse the query: ?q=[something]
        parser.add_argument('q')
        query_string = parser.parse_args()
        # base search URL
        url = es_base_url['products']+'/_search'
        # Query Elasticsearch
        query_alnum = ''.join(e for e in query_string['q'] if (e.isalnum() or e.isspace()) )
        query = {
            "query": {
                "match": {
                    "_all": {
                        "query": query_alnum, 
                        "operator": "and"
                    }
                }
            },
            "size": 20,
            "sort" : [
            "onSale",
            "bestSellingRank",
            "_score"
            ]
        } 
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()

        # Build an array of results
        products = []
        for hit in data['hits']['hits']:
            product = hit['_source']
            product['id'] = hit['_id']
            products.append(product['name'])

        #Request Logging
        f = open('/tmp/__init__.log', 'a')
        f.write("\n")
        f.write("\nrequest.url: " + request.url)
        f.write("\nurl: "+url)
        f.write("\nquery: "+json.dumps(query))
        f.write('\n' + '\n'.join(products).encode('utf-8') )
        f.write('\nQuery Processed in: ' + str((datetime.datetime.today() - startTime).microseconds / 1000) + ' milliseconds')
        f.close()
        return products 
api.add_resource(Search, api_base_url+'/search')
