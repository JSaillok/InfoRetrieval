from conn import connElasticSearch
from elasticsearch.helpers import scan
import pandas as pd
from teachdata import teach_data

def getData2(indexname,keyword, userId, activate_nn=False):
    cn = connElasticSearch()
    cn.indices.refresh(index=indexname) #refresh elastic search every (condition)
    def getBooks():
        # Elasticsearch Query.
        query = {
            "query": {
                "match": {
                    "book_title": {
                        "query": keyword,
                        "operator": "and"
                    }
                }
            },
            "aggs": {
            	"avg_rating": {
            		"avg": {
            			"field": "rating",
            		}
            	}
            }
        }

        # Collecting all the data using Scan function.
        rel = scan(
            client=cn,
            query=query,
            scroll='1m',
            index='merged',
            raise_on_error=True,
            preserve_order=False,
            clear_scroll=True
        )
        # This list keeps the response.
        result = list(rel)
        temp = []

        # Clear the response data from metadata like _id, _type, _index.
        for hit in result:
            # So, we're getting only '_source'
            temp.append(hit['_source'])

        # Create a dataframe
        books_df = pd.DataFrame(temp)

        return books_df
    
    def getRating():
	    # Elasticsearch Query.
        query = {
            "query": {
                "match": {
	                "uid": {
				    	"query": userId
				    }
			    }
		    }
	    }

        # Collecting all the data using Scan function.
        rel1 = scan(
            client=cn,
            query=query,
            scroll='1m',
            index='bx-book-ratings',
            raise_on_error=True,
            preserve_order=False,
            clear_scroll=True
            )

        # This list keeps the response.
        result = list(rel1)
        temp1 = []

        # Clear the response data from metadata like _id, _type, _index.
        for hit in result:
            # So, we're getting only '_source'
            temp1.append(hit['_source'])

        # Create a dataframe
        user_df = pd.DataFrame(temp1)

        return user_df

    df = getBooks()
    df1 = getRating()

    if activate_nn:
        # books with no rating by user
        fill = (df['rating'] == 0)
        # check if there are unrated books
        if fill.value_counts()[0]:
            df.loc[fill, 'rating'] = teach_data(userId, df[fill])