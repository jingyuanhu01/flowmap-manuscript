import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import coo_matrix
import time


class PhaseDistanceGraphSolver:
    def __init__(self, X, V, k=30, alpha=0.5):
        """
        Parameters
        ----------
        X : ndarray (n, d)
            Input positions
        V : ndarray (n, d)
            Velocity or vector data
        k : int
            Number of neighbors for kNN
        alpha : float
            Hyperparameter for hybrid distance
        """
        self.X = X
        self.V = V
        self.k = k
        self.alpha = alpha

        self.n, self.d = X.shape

        # --- Build kNN graph ---
        start = time.perf_counter()
        nn = NearestNeighbors(n_neighbors=k + 1, algorithm="auto").fit(X)
        distances, neighbors = nn.kneighbors(X)
        neighbors = neighbors[:, 1:]  # remove self

        self.i_idx = np.repeat(np.arange(self.n), k)
        self.j_idx = neighbors.flatten()
        self.n_edges = self.n * k

        # --- Compute t_ls ---
        self.t_ls = self._compute_tls()

    def _compute_tls(self):
        """Compute least-squares time estimates t_ls."""
        Y = self.V
        X = self.X
        i_idx, j_idx = self.i_idx, self.j_idx

        # Step 2: Compute Q
        diag_Y = np.einsum("nd,nd->n", Y, Y)
        Y_dot = np.einsum("nd,nd->n", Y[i_idx], Y[j_idx])

        Q = np.zeros((self.n_edges, 2, 2))
        Q[:, 0, 0] = diag_Y[i_idx]
        Q[:, 1, 1] = diag_Y[j_idx]
        Q[:, 0, 1] = -Y_dot
        Q[:, 1, 0] = -Y_dot

        # Step 3: Inverse of Q
        q00, q01, q10, q11 = Q[:, 0, 0], Q[:, 0, 1], Q[:, 1, 0], Q[:, 1, 1]
        det = q00 * q11 - q01 * q10 + 1e-12
        inv_Q = np.empty_like(Q)
        inv_Q[:, 0, 0] = q11 / det
        inv_Q[:, 0, 1] = -q01 / det
        inv_Q[:, 1, 0] = -q10 / det
        inv_Q[:, 1, 1] = q00 / det

        # Step 4: Construct B
        diag_YX = np.einsum("nd,nd->n", Y, X)
        YX_ij = np.einsum("nd,nd->n", Y[i_idx], X[j_idx])
        YX_ji = np.einsum("nd,nd->n", Y[j_idx], X[i_idx])

        B = np.zeros((self.n_edges, 2))
        B[:, 0] = YX_ij - diag_YX[i_idx]
        B[:, 1] = YX_ji - diag_YX[j_idx]

        # Step 5: t_ls
        t_ls = np.einsum("eij,ej->ei", inv_Q, B)

        return t_ls

    def compute_graph(self):
        """Build hybrid distance graph as a sparse COO matrix."""
        X = self.X
        i_idx, j_idx = self.i_idx, self.j_idx
        t_ls = self.t_ls

        dist_sq = np.sum((X[i_idx] - X[j_idx]) ** 2, axis=1)
        t_dist_sq = (t_ls[:, 0] - t_ls[:, 1]) ** 2

        lam = self.alpha * np.linalg.norm(dist_sq) / (np.linalg.norm(t_dist_sq) + 1e-12)
        hybrid_dist = np.sqrt(dist_sq + lam * t_dist_sq)

        # Duplicate edges for symmetry
        i_sym = np.concatenate([i_idx, j_idx])
        j_sym = np.concatenate([j_idx, i_idx])
        hybrid_dist_sym = np.concatenate([hybrid_dist, hybrid_dist])

        graph = coo_matrix((hybrid_dist_sym, (i_sym, j_sym)), shape=(self.n, self.n))
        return graph
