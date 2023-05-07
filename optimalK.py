from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from kneed import KneeLocator

def find_opt_k(x):
    rng = range(1, 15)
    sse = []
    for k in rng:
        km = KMeans(n_clusters=k, n_init=10)
        km.fit(x)
        sse.append(km.inertia_)

    choice = input('Plot Elbow Graph? (Y/N) --> ')
    if choice.upper() == 'Y':
        plt.xlabel('K')
        plt.ylabel('SSE')
        plt.title("Elbow Method For Optimal K")
        plt.plot(rng, sse)
        plt.show()

    kl = KneeLocator(range(1, 15), sse, curve="convex", direction="decreasing")

    return kl.elbow