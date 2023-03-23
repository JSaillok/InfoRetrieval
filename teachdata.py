from teachuser import teach_user
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

def teach_data(userId, zero_books):
    # candidates for ML: 131837, 135458, 124078, 254, random: 1 -> 145451

    user_nz_data = teach_user(userId)

    # return zeros if there are not enough data
    if len(user_nz_data) <= 1:
        raise Exception("User's train data are not enough")
    # Information Retrieval
    user_nz_data['title_summary'] = user_nz_data['book_title'] + ' ' + user_nz_data['summary']
    # split 80-20 the (known) data for training and testing
    train, test = train_test_split(user_nz_data.loc[:, ['title_summary', 'rating']], test_size=0.3, random_state=42)
    print(len(train), len(test))
    # these are the data for training the model
    train_x = [t_s for t_s in train['title_summary']]
    train_y = [int(rate) for rate in train['rating']]

    # these are the data for testing/predicting the model
    test_x = [t_s for t_s in test['title_summary']]
    test_y = [int(rate) for rate in test['rating']]

    # finding the dictionary
    # and converting words to matrices
    vectorizer = CountVectorizer()
    # Dimensions of document-term-matrix are n x m
    # where n the total summaries
    # and m the total words from corpus
    train_x_vectors = vectorizer.fit_transform(train_x)

    test_x_vectors = vectorizer.transform(test_x)

    # scale data
    scaler = MaxAbsScaler()
    train_x_vectors = scaler.fit_transform(train_x_vectors)
    test_x_vectors = scaler.transform(test_x_vectors)

    # RandomForestClassifier
    # Default Classifier
    clf_rfc = RandomForestClassifier()
    clf_rfc.fit(train_x_vectors, train_y)

    # LogisticRegression classifier
    clf_log = LogisticRegression()
    clf_log.fit(train_x_vectors, train_y)

    # DecisionTreeClassifier
    clf_dec = DecisionTreeClassifier()
    clf_dec.fit(train_x_vectors, train_y)

    # linear SVC
    clf_svm = svm.SVC(kernel='linear', C=4)
    clf_svm.fit(train_x_vectors, train_y)

    print("Mean Accuracies: ")
    print("1. RandomForest: ", clf_rfc.score(test_x_vectors, test_y))
    print("2. LogisticRegression: ", clf_log.score(test_x_vectors, test_y))
    print("3. DecisionTree: ", clf_dec.score(test_x_vectors, test_y))
    print("4. SVM: ", clf_svm.score(test_x_vectors, test_y))
    pick = int(input("Classifier: "))

    zero_books_x = [t_s for t_s in (zero_books.loc[:, 'book_title'] + ' ' + zero_books.loc[:, 'summary'])]
    zero_books_x_vectors = vectorizer.transform(zero_books_x)

    # Pick the most suitable model (out of 4)
    if pick == 1:
        return clf_rfc.predict(zero_books_x_vectors)
    elif pick == 2:
        return clf_log.predict(zero_books_x_vectors)
    elif pick == 3:
        return clf_dec.predict(zero_books_x_vectors)
    elif pick == 4:
        return clf_svm.predict(zero_books_x_vectors)
