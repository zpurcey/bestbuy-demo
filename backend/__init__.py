#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
import json
import os
import uuid
import getpass


app = Flask(__name__, static_url_path = "")
CORS(app) # required for Cross-origin Request Sharing
api = Api(app)

api_base_url = '/api/v1'
es_base_url = {
    'products': 'http://10.128.0.4:9200/bestbuy-products-3/product',
}

parser = reqparse.RequestParser()

@app.route('/', methods = ['GET'])
def default():
        return '{<br>&nbsp;&nbsp;"paths": [<br>&nbsp;&nbsp;&nbsp;&nbsp;"/wordcloud/api",<br>&nbsp;&nbsp;&nbsp;&nbsp;"/wordcloud/api/v1",<br>&nbsp;&nbsp;&nbsp;&nbsp;"/healthz",<br>&nbsp;&nbsp;]<br>}'

class Healthz(Resource):
    def get(self):
        return 'OK'

api.add_resource(Healthz, api_base_url+'/healthz')

class Search(Resource):
 
    def get(self):
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
        print("url:"+url)
        print("query:"+json.dumps(query))
        data = resp.json()
        #print (data)
        # Build an array of results
        products = []
        for hit in data['hits']['hits']:
            product = hit['_source']
            product['id'] = hit['_id']
            products.append(product['name'])
        print "\n" + '\n'.join(products)
        return products 
api.add_resource(Search, api_base_url+'/search')
