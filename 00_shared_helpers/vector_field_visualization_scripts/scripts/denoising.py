from scipy.linalg import svd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA



# Function to compute subspace-denoised vectors using SVD
def subspace_denoised(X, Y, r, alpha=0.5, method="sum"):
    if method == "sum":
        mat = alpha * X + (1 - alpha) * Y
        u, s, vh = svd(mat, full_matrices=False)
        V_hat = vh[:r, :]
        X_hat = X @ V_hat.T
        Y_hat = Y @ V_hat.T
        
#     if method == "combined":
#         mat = np.hstack((X, Y))
#         u, s, vh = svd(mat, full_matrices=False)
#         V_hat = vh[:r, :]
#         mat_hat = mat @ V_hat.T @ V_hat
#         X_hat = mat_hat[:,:X.shape[1]]
#         Y_hat = mat_hat[:,X.shape[1]:]
    return X_hat, Y_hat, V_hat
    


def pca_elbow_plot(data, top_k=None, dot_size=10):
    """
    Select the number of principal components based on the explained variance.

    Parameters
    ----------
    data : ndarray of shape (n_samples, n_features)
        The input data to perform PCA on.

    variance_threshold : float, optional
        The cumulative variance threshold (e.g., 0.9 for 90%).

    plot : bool, optional
        Whether to plot the explained variance and cumulative variance.

    Returns
    -------
    n_pcs : int
        The number of PCs to retain.
    """
    # Fit PCA to the data
    pca = PCA()
    pca.fit(data)

    # Explained variance ratio
    explained_variance = pca.explained_variance_ratio_

    # Limit to the top K components if specified
    if top_k is not None:
        explained_variance = explained_variance[:top_k]

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.plot(
        range(1, len(explained_variance) + 1),
        explained_variance,
        marker='o',
        markersize=dot_size / 10,  # Adjust size for better appearance
        label='Explained Variance'
    )
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Variance Explained')
    plt.title('PCA Explained Variance')
    plt.legend()
    plt.grid()
    plt.show()

    
    
    