#!/usr/bin/python
import requests 
import json
import datetime
import time
import os

myApiKey = os.environ.get('BESTBUY_API_KEY')
myElasticServerIp = os.environ.get('ES_SERVER_IP', 'localhost')
myIndexName = os.environ.get('ES_INDEX_NAME', 'bestbuy-products')


def checkPageCount():
    url = 'https://api.bestbuy.com/v1/products?page=1&pageSize=100&format=json&show=sku,name,salePrice,salesRankLongTerm,bestSellingRank,onSale,active&sort=bestSellingRank.asc&apiKey=' + myApiKey
    r = requests.get(url)
    j = r.json()
    print j['totalPages']
    return (j['totalPages'])

def loadPage(pageNum):
    url = 'https://api.bestbuy.com/v1/products?page=' + str(pageNum) + '&pageSize=100&format=json&show=sku,name,salePrice,salesRankLongTerm,bestSellingRank,onSale,active&sort=bestSellingRank.asc&apiKey=' + myApiKey
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        j = r.json()
        if 'products' in j:
            for product in j['products']:
                loadJson(json.dumps(product))
    else:
        f = open('page-missed.log', 'a')
        f.write('Page download failed for Page ' + str(pageNum) + '\n') 
        f.close()

def main():
    deleteIndex()
    pageNum = 1
    todaysDate = datetime.datetime.today().strftime('%Y.%m.%d')
    startTime = datetime.datetime.today()
    totalPageCount = checkPageCount()
    while pageNum <= totalPageCount:
        pageStartTime = datetime.datetime.today()
        loadPage(pageNum)
        pageNum += 1
        print 'Page ' + str(pageNum) + ' of ' + str(totalPageCount) + ' completed...'
        print 'Total runtime: ' + str((datetime.datetime.today() - startTime).total_seconds())
        print 'Page Processed in: ' + str((datetime.datetime.today() - pageStartTime).total_seconds())
        print 'Minutes to complete product load: ' + str((totalPageCount - pageNum)*(datetime.datetime.today() - pageStartTime).total_seconds()/60)

def loadJson(jsonData):
    index = myIndexName 
    type = 'product'
    response = requests.post('http://' + myElasticServerIp + ':9200/'+index+'/'+type+'/', data=jsonData)
    print(response)

def deleteIndex():
    index = myIndexName
    type = 'product'
    response = requests.delete('http://' + myElasticServerIp + ':9200/'+index+'/')
    print(response)

main()
