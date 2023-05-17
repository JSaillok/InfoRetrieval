import pandas as pd
from conn import connElasticSearch

# Get the data according to the keyword

def getdata(indexname, keyword):
	cn = connElasticSearch()
	cn.indices.refresh(index=indexname) #refresh elastic search every (condition)
	match_query = {
		"match": {
			"book_title": keyword
		}
	}
	result = cn.search(index=indexname, query=match_query, size=10000)

	books = []
	score = []
	for hit in result['hits']['hits']:
		books.append(hit['_source'])
		score.append(hit['_score'])

	df = pd.DataFrame(books)
	df['score'] = score

	return df