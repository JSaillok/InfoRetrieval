from conn import connElasticSearch
import pandas as pd

def teach_user(userId):
    cn = connElasticSearch()
    res = cn.search(index='bratings', query={"match": {"uid": userId}}, size=10000)

    array = []
    # get all the books(isbn) for a user into a list
    for hit in res['hits']['hits']:
        # keep rated by user books
        userRating = int(hit['_source']['rating'])
        if userRating:
            isbn_rating = (hit['_source']['isbn'], userRating)
            array.append(isbn_rating)

    book_titles = []
    summaries = []
    ratings = []
    book_isbn = []
    # checking if all books exists in index 'books'
    for t in array:
        res = cn.search(index='books', query={"match": {"isbn": t[0]}})
        # if specific book exists in index 'books'
        if res['hits']['total']['value']:
            # get the rating
            ratings.append(int(t[1]))

            for hit in res['hits']['hits']:
                book_titles += [hit['_source']['book_title']]
                summaries += [hit['_source']['summary']]
                book_isbn += [hit['_source']['isbn']]

    # convert data to pandas df
    d = {'isbn': book_isbn, 'book_title': book_titles, 'summary': summaries, 'rating': ratings}
    return pd.DataFrame(d)