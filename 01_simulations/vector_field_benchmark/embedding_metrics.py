import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.manifold import trustworthiness
from scipy.stats import pearsonr


def jaccard_knn_similarity(X1, X2, k=30):
    nn1 = NearestNeighbors(n_neighbors=k+1).fit(X1)
    nn2 = NearestNeighbors(n_neighbors=k+1).fit(X2)

    knn1 = nn1.kneighbors(return_distance=False)[:, 1:]  # Exclude self
    knn2 = nn2.kneighbors(return_distance=False)[:, 1:]

    jaccard_scores = [
        len(set(knn1[i]) & set(knn2[i])) / len(set(knn1[i]) | set(knn2[i]))
        for i in range(X1.shape[0])
    ]
    return np.mean(jaccard_scores)


def position_embedding_evaluation_metric(X1, X2, k=30):
    return {
        "jaccard_similarity": jaccard_knn_similarity(X1, X2, k=k),
        "trustworthiness": trustworthiness(X1, X2, n_neighbors=k)
    }


def cosine_angle_matrix(V):
    sim = V @ V.T
    norms = np.linalg.norm(V, axis=1)
    denom = np.outer(norms, norms)
    denom[denom == 0] = 1e-8        # Avoid division by zero
    return sim / denom


def vector_field_local_smoothness(X, V, k=15, eps=1e-8):
    nn = NearestNeighbors(n_neighbors=k + 1).fit(X)
    knn = nn.kneighbors(return_distance=False)[:, 1:]  # drop self

    ratios = []
    for i, nbrs in enumerate(knn):
        vi = V[i]
        vj = V[nbrs]

        diff    = np.linalg.norm(vi - vj, axis=1)        # d_ij
        denom   = np.linalg.norm(vi) + np.linalg.norm(vj, axis=1) + eps  # s_ij
        ratios.extend(diff / denom)                      # r_ij in [0,2]

    mean_ratio = np.mean(ratios)                         # ⟨r_ij⟩
    smoothness = 1 - 0.5 * mean_ratio                    # map [0,2] → [1,0]
    return smoothness


def vector_field_evaluation_metric(X1, X2, V1, V2, k=30):
    n = X2.shape[0]

    # --- 1. global magnitude correlation ----------------------------------
    mags1 = np.linalg.norm(V1, axis=1)
    mags2 = np.linalg.norm(V2, axis=1)
    magnitude_corr = pearsonr(mags1, mags2)[0]

    # --- 2. build neighbour index matrix ----------------------------------
    nbrs = NearestNeighbors(n_neighbors=k + 1).fit(X1)
    idx_mat = nbrs.kneighbors(return_distance=False)[:, 1:]  # drop self

    # --- 3. local angular similarity --------------------------------------
    def cos_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

    diffs = []
    for i in range(n):
        for j in idx_mat[i]:
            diffs.append(
                cos_sim(V1[i], V1[j]) - cos_sim(V2[i], V2[j])
            )
    local_avg_cos_sim = 1 - np.mean(np.abs(diffs))
    
    # --- 4. smoothness --------------------------------------
    smooth = vector_field_local_smoothness(X2, V2, k=k)
    
    return {
        "magnitude_correlation": magnitude_corr,
        "avg_cosine_similarity": local_avg_cos_sim,
        "smoothness": smooth
    }


def evaluate_embedding_method(X_gt, X_emb, V_gt, V_emb, k=30):
    pos_scores = position_embedding_evaluation_metric(X_gt, X_emb, k=k)
    vec_scores = vector_field_evaluation_metric(X_gt, X_emb, V_gt, V_emb)

    # Combine into one result table
    result = {
        "jaccard_similarity": pos_scores["jaccard_similarity"],
        "trustworthiness": pos_scores["trustworthiness"],
        "magnitude_correlation": vec_scores["magnitude_correlation"],
        "avg_cosine_similarity": vec_scores["avg_cosine_similarity"],
        "smoothness": vec_scores["smoothness"]
    }
    return result



