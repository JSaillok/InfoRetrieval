from conn import connElasticSearch

# Check the data if they 're uploaded

def checkdata(index):
	cn = connElasticSearch()
	result = cn.search(index=index, size=1000)
	num_docs = result['hits']['total']['value']
	return num_docs