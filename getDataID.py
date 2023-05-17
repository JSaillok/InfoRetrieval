from conn import connElasticSearch
from getDataS import getdata
from teachdata import teach_data


def getdataisbnUid(keyword, userId, activate_nn=False):
    # inner function to return book avg
    def isbnRatingAvg(book_code):
        # match isbn and boost if user has read it
        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "isbn": book_code
                        }
                    }
                ],
                "should": [
                    {
                        "match": {
                            "uid": userId
                        }
                    }
                ]
            }
        }

        # execute query
        rst = cn.search(index='bratings', query=query, size=10000)

        if not rst['hits']['hits']:
            return 0, 0

        s = 0
        cnt = 0
        # get user's grade
        userRating = int(rst['hits']['hits'][0]['_source']['rating'])
        for h in rst['hits']['hits']:
            # grade > 0
            some_user_rate = int(h['_source']['rating'])
            if some_user_rate:
                s += some_user_rate
                cnt += 1

        # checking for division by zero
        if cnt != 0:
            return (s / cnt), userRating
        else:
            return s, userRating

    cn = connElasticSearch()

    # get all the books matching keyword
    books = getdata('books', keyword)

    avgs = []
    ratings = []
    # separate lists for user's book ratings and avg's
    for isbn in books['isbn']:
        mean, rate = isbnRatingAvg(isbn)
        avgs += [mean]
        ratings += [rate]

    books['rating'] = ratings

    if activate_nn:
        # books with no rating by user
        fill = (books['rating'] == 0)
        # check if there are unrated books
        if fill.value_counts()[0]:
            books.loc[fill, 'rating'] = teach_data(userId, books[fill])


    score = []
    # formulating and calculating the scores
    for i in range(len(books)):
        score += [(0.65 * books.loc[i, 'score']) + (0.25 * books.loc[i, 'rating']) + (0.1 * avgs[i])]

    # replace with the new custom scores
    books['score'] = score

    # sort by 'score'
    return books.sort_values(by=['score'], ascending=False)