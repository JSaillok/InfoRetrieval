from conn import connElasticSearch
import pandas as pd

def fetch_cluster(size):
    cn = connElasticSearch()

    # Define the match query to retrieve all documents
    matchq = {"match_all": {}}

    # Execute the query and retrieve the matching documents
    result = cn.search(index='books', query=matchq, size=size)

    summary = []
    isbns = []
    # Extract the summary and ISBN of each book
    for hit in result['hits']['hits']:
        summary.append(hit['_source']['summary'])
        isbns.append(hit['_source']['isbn'])

    # Aggregation for each ISBN with a maximum of 100 users
    aggr = {
        "aggs": {
            "top_hits": {
                "size": 100,
                "_source": ['uid', 'rating']
            }
        }
    }

    users = []
    for isbn in isbns:
        # Match query to retrieve users who rated the book
        match_isbn = {"match": {"isbn": isbn}}
        res = cn.search(index='bratings', query=match_isbn, aggregations=aggr, size=0)
        temp_list = []
        # Retrieve users and their ratings
        for hit in res['aggregations']['aggs']['hits']['hits']:
            match_user = {"match": {"uid": hit['_source']['uid']}}
            userRes = cn.search(index='users', query=match_user, size=1)
            # Check if the user exists
            if userRes['hits']['hits']:
                temp = userRes['hits']['hits'][0]['_source']
                temp_list.append((temp['location'], temp['age'], hit['_source']['rating']))
        users.append(temp_list)
    
    # Create a DataFrame to store the retrieved data
    return pd.DataFrame({"summary": [s for s in summary], "users": [user for user in users]},
                        columns=['summary', 'users'])