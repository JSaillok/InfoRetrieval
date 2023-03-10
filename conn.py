from elasticsearch import Elasticsearch

# Method for connection to elasticsearch

def connElasticSearch():
	ES_NODES = "http://localhost:9200"

	conn = Elasticsearch(hosts = [ES_NODES])
	if conn.ping():
		return conn
	else:
		raise("Connection to ElasticSearch was failed")
# Returns True if host (conn) responds to a ping request.