from fetchCluster import fetch_cluster
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
    def clr(df, i):
        countries = []
        ratings = []
        # return data from cluster i as df
        tempdf = df[df['cluster'] == i].loc[:, ['users']]
        usa_countries = ['pender', 'washington,', 'florida,', 'missouri,', 'republic', 'california,', 'carolina,', 'massachusetts,', 'nebr,', 'tennessee,', 'states', 'pennsylvania,', 'texas,', 'ohio,', 'york,']
        # Extract country and rating information for each user in each book
        for index, row in tempdf.iterrows():
            # if not empty
            if row['users']:
                # for each user in each book
                for t in row['users']:
                    # country = ",".join(t[0].split(", ")[-2:])
                    country = t[0].split()[-1] # Extract the country from the user information
                    # # Check if the country is registered and the rating is not 0
                    if len(country) > 2 and int(t[2]):
                        if country in usa_countries:
                            country = 'usa'
                        countries.append(country)
                        ratings.append(int(t[2]))

        # Group the data based on country and rating
        groupit = pd.DataFrame({"country": [c for c in countries], "rating": [r for r in ratings]},
                                columns=['country', 'rating']) \
            .value_counts(['country', 'rating']).reset_index()
        groupit.rename({groupit.columns[-1]: 'times'}, axis=1, inplace=True)

        return groupit

    # fetch summaries
    df = fetch_cluster(int(input('Books to fetch: ')))

    # # Convert summaries to vectors using CountVectorizer
    vc = CountVectorizer()
    A = vc.fit_transform(df['summary']).toarray()

    # Perform dimensionality reduction with PCA
    aSvd = PCA(2).fit_transform(A)

    # Find the optimal K value using the find_opt_k function
    opt_k = find_opt_k(aSvd)

    if metric == 'cosine_similarity':
        # Normalize the data using L2 normalization
        aSvd = normalize(aSvd)
        # Calculate the magnitudes and divide by them
        length = np.sqrt((aSvd ** 2).sum(axis=1))[:, None]
        aSvd = aSvd / length

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=opt_k, n_init=10).fit(aSvd)

        # Calculate the normalized centroids
        len_ = np.sqrt(np.square(kmeans.cluster_centers_).sum(axis=1)[:, None])
        centroids = kmeans.cluster_centers_ / len_
    elif metric == 'euclidean_distance':
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=opt_k, n_init=10).fit(aSvd)
        centroids = kmeans.cluster_centers_
    else:
        raise SyntaxError('Choose one of the following: "euclidean_distance", "cosine_distance"')

    # Assign cluster labels to the DataFrame
    df['cluster'] = kmeans.predict(aSvd)

    # Get unique cluster labels
    u_clusters = np.unique(df['cluster'])

    # Plotting results:
    for i in u_clusters:
        plt.scatter(aSvd[df['cluster'] == i, 0], aSvd[df['cluster'] == i, 1], label=i)

    plt.scatter(centroids[:, 0], centroids[:, 1], color='black', marker='*', label='centroid')
    # Convert the metric input to the graph title
    words = metric.replace('_', ' ').split()
    title = words[0].capitalize() + " " + words[1].capitalize()
    plt.title(title)
    plt.legend()
    plt.show()

    # Generate heat maps for each cluster
    for i in range(0, opt_k):
        plot_df = clr(df, i)
        plot_df = plot_df.pivot(index="country", columns="rating", values="times")
        sns.heatmap(plot_df, linewidths=.3, yticklabels=True)
        plt.yticks()
        plt.title('Cluster ' + str(i))
        plt.show()