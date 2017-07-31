#!/usr/bin/python
import requests 
import json
import os

myElasticServerIp = os.environ.get('ES_SERVER_IP', 'localhost')
myIndexName = os.environ.get('ES_INDEX_NAME', 'bestbuy-products')

def main():
    deleteIndex()
    createIndex()

def createIndex():
    with open('mapping.json') as mappingFile:
        jsonData = json.load(mappingFile)
    type = 'product'
    postUrl = 'http://' + myElasticServerIp + ':9200/' + myIndexName + '/'
    print(postUrl)
    response = requests.post(postUrl, data=json.dumps(jsonData))
    print(response)
    print(response.content)

def deleteIndex():
    type = 'product'
    response = requests.delete('http://' + myElasticServerIp + ':9200/' + myIndexName + '/')
    print(response)
    print(response.content)

main()
