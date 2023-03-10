from elasticsearch import helpers
import csv
from conn import connElasticSearch

# Upload the data to elasticsearch

def uploadData(filename, indexname):
	cn = connElasticSearch()
	try:
		with open(filename, encoding='utf8') as csvFile:
			reader = csv.DictReader(csvFile)
			helpers.bulk(cn, reader, index=indexname)
	except FileNotFoundError:
		print("The file with that name does not exists")