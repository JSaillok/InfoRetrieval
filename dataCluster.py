from uploadCluster import upload_cluster
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from optimalK import find_opt_k
from sklearn.preprocessing import normalize, MaxAbsScaler
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import seaborn as sns

def clusterData(metric, userId=None):
    def clear_them(df, i):
        countries = []
        ratings = []
        # return data from cluster i as df
        tempdf = df[df['cluster'] == i].loc[:, ['users']]
        usa_countries = ['pender', 'washington,', 'florida,', 'missouri,', 'republic', 'california,', 'carolina,', 'massachusetts,', 'nebr,', 'tennessee,', 'states', 'pennsylvania,', 'texas,', 'ohio,', 'york,']
        for index, row in tempdf.iterrows():
            # if not empty
            if row['users']:
                # for each user in each book
                for t in row['users']:
                    # country = ",".join(t[0].split(", ")[-2:])
                    country = t[0].split()[-1]
                    # if country registered and rate not 0
                    if len(country) > 2 and int(t[2]):
                        if country in usa_countries:
                            country = 'usa'
                        countries.append(country)
                        ratings.append(int(t[2]))

        # group data
        group_it = pd.DataFrame({"country": [c for c in countries], "rating": [r for r in ratings]},
                                columns=['country', 'rating']) \
            .value_counts(['country', 'rating']).reset_index()
        group_it.rename({group_it.columns[-1]: 'times'}, axis=1, inplace=True)

        return group_it

    # fetch summaries
    df = upload_cluster(int(input('Books to fetch: ')))

    # convert summaries to vectors and normalize them
    vec = CountVectorizer()
    X = vec.fit_transform(df['summary']).toarray()

    # dim reduction with SVD
    xSvd = PCA(2).fit_transform(X)

    # fit them to kmeans
    opt_k = find_opt_k(xSvd)

    if metric == 'cosine_similarity':
        # data normalization
        xSvd = normalize(xSvd)
        # calculate magnitudes and divide by it
        length = np.sqrt((xSvd ** 2).sum(axis=1))[:, None]
        xSvd = xSvd / length

        # produce k-means
        kmeans = KMeans(n_clusters=opt_k, n_init=10).fit(xSvd)

        # calculate centroids
        len_ = np.sqrt(np.square(kmeans.cluster_centers_).sum(axis=1)[:, None])
        centroids = kmeans.cluster_centers_ / len_
    elif metric == 'euclidean_distance':
        # produce k-means
        kmeans = KMeans(n_clusters=opt_k, n_init=10).fit(xSvd)
        centroids = kmeans.cluster_centers_
    else:
        raise SyntaxError('Choose one of the following: "euclidean_distance", "cosine_distance"')

    df['cluster'] = kmeans.predict(xSvd)

    # Getting unique clusters
    u_clusters = np.unique(df['cluster'])

    # plotting the results:
    for i in u_clusters:
        plt.scatter(xSvd[df['cluster'] == i, 0], xSvd[df['cluster'] == i, 1], label=i)

    plt.scatter(centroids[:, 0], centroids[:, 1], color='black', marker='*', label='centroid')
    # convert metric input to graph title
    words = metric.replace('_', ' ').split()
    title = words[0].capitalize() + " " + words[1].capitalize()
    plt.title(title)
    plt.legend()
    plt.show()

    # form data for heat map for each cluster
    for i in range(0, opt_k):
        plot_df = clear_them(df, i)
        plot_df = plot_df.pivot(index="country", columns="rating", values="times")
        sns.heatmap(plot_df, linewidths=.3, yticklabels=True)
        plt.yticks()
        plt.title('Cluster ' + str(i))
        plt.show()