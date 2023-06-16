from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from kneed import KneeLocator

def find_opt_k(x):
    # Define the range of K values to evaluate
    rng = range(1, 15)
    sum_squared_errors = []
    for k in rng:
        # Create a KMeans model with the current K value
        km = KMeans(n_clusters=k, n_init=10)
        # Fit the model to the data
        km.fit(x)
        # Calculate the Sum of Squared Errors and append it to the list
        sum_squared_errors.append(km.inertia_)

    choice = input('Plot Elbow Graph? (Y/N) --> ')
    if choice.upper() == 'Y':
        # Plot
        plt.xlabel('K')
        plt.ylabel('SSE')
        plt.title("Elbow Method For Optimal K")
        plt.plot(rng, sum_squared_errors)
        plt.show()

    # Use the KneeLocator to find the optimal K value (elbow point)
    kneel = KneeLocator(range(1, 15), sum_squared_errors, curve="convex", direction="decreasing")

    return kneel.elbow