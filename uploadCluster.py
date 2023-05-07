from conn import connElasticSearch
import pandas as pd

def upload_cluster(size):
    cn = connElasticSearch()

    match_query = {"match_all": {}}

    # execute query and return matches
    res = cn.search(index='books', query=match_query, size=size)

    summary = []
    isbns = []
    for hit in res['hits']['hits']:
        summary.append(hit['_source']['summary'])
        isbns.append(hit['_source']['isbn'])

    # aggregation for each isbn up to 100 users
    aggr = {
        "aggs": {
            "top_hits": {
                "size": 100,
                "_source": ['uid', 'rating']
            }
        }
    }

    users = []
    # for each book
    for isbn in isbns:
        match_isbn = {"match": {"isbn": isbn}}
        res = cn.search(index='bratings', query=match_isbn, aggregations=aggr, size=0)
        temp_list = []
        # get users and ratings
        for hit in res['aggregations']['aggs']['hits']['hits']:
            match_user = {"match": {"uid": hit['_source']['uid']}}
            userRes = cn.search(index='users', query=match_user, size=1)
            # if user exists
            if userRes['hits']['hits']:
                temp = userRes['hits']['hits'][0]['_source']
                temp_list.append((temp['location'], temp['age'], hit['_source']['rating']))
        users.append(temp_list)

    return pd.DataFrame({"summary": [s for s in summary], "users": [user for user in users]},
                        columns=['summary', 'users'])