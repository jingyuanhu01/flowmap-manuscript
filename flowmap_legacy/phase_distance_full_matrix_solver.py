import numpy as np


class PhaseDistanceSolver:

    def __init__(self, X, Y):
        """
        Initialize the solver with data matrices X, Y and constraint c.

        Parameters:
        - X: (n, d) numpy array
        - Y: (n, d) numpy array
        - c: scalar constraint controlling maximum perturbation size
        """
        self.X = X
        self.Y = Y
        self.n = X.shape[0]

        YY = Y @ Y.T
        diag_Y = np.diag(YY)

        # Construct 2x2 matrix Q for each (i,j) pair
        Q = np.zeros((self.n, self.n, 2, 2))
        Q[:, :, 0, 0] = diag_Y[:, np.newaxis]
        Q[:, :, 1, 1] = diag_Y[np.newaxis, :]
        Q[:, :, 0, 1] = -YY
        Q[:, :, 1, 0] = -YY

        # Inverse of each 2x2 Q matrix
        q00 = Q[..., 0, 0]
        q01 = Q[..., 0, 1]
        q10 = Q[..., 1, 0]
        q11 = Q[..., 1, 1]
        det = q00 * q11 - q01 * q10
        det += 1e-12  # For numerical stability

        inv_Q = np.empty_like(Q)
        inv_Q[..., 0, 0] = q11 / det
        inv_Q[..., 0, 1] = -q01 / det
        inv_Q[..., 1, 0] = -q10 / det
        inv_Q[..., 1, 1] = q00 / det

        # Construct B matrix of cross terms
        YX = Y @ X.T
        diag_YX = np.diag(YX)

        B = np.zeros((self.n, self.n, 2))
        B[:, :, 0] = YX - diag_YX[:, np.newaxis]
        B[:, :, 1] = YX.T - diag_YX[np.newaxis, :]

        # Least-squares solution t for unregularized perturbation
        t_ls = np.einsum("mnij, mnj -> mni", inv_Q, B)

        # Eigenvalues (lam) and eigenvectors (Q_eigen) of Q
        trace = Q[:, :, 0, 0] + Q[:, :, 1, 1]
        delta = np.sqrt((Q[:, :, 0, 0] - Q[:, :, 1, 1]) ** 2 + 4 * Q[:, :, 0, 1] ** 2)
        lambda1 = (trace + delta) / 2
        lambda2 = (trace - delta) / 2
        eigvals = np.stack([lambda1, lambda2], axis=-1)

        Q_eigen = np.empty_like(Q)
        Q_eigen[:, :, 0, 0] = Q[:, :, 0, 1]
        Q_eigen[:, :, 1, 1] = Q[:, :, 1, 0]
        Q_eigen[:, :, 0, 1] = Q[:, :, 0, 0] - lambda1
        Q_eigen[:, :, 1, 0] = Q[:, :, 1, 1] - lambda2

        norms = np.sqrt(np.einsum('ijkl, ijkl -> ijk', Q_eigen, Q_eigen)) + 1e-12
        Q_eigen = np.einsum('ijkl,ijk->ijkl', Q_eigen, 1 / norms)

        # Store everything
        self.Q = Q
        self.inv_Q = inv_Q
        self.B = B
        self.t_ls = t_ls
        self.eigvals = eigvals
        self.Q_eigen = Q_eigen
        self.UB = np.einsum("ijkl, ijk -> ijl", Q_eigen, B)


    def find_reg(self, rounds=30, c=None, quantile=0.75):
        """
        Finds the optimal regularization value for each (i,j) pair using binary search
        such that the perturbation size does not exceed constraint `c`.

        Parameters:
        - rounds: number of binary search iterations

        Returns:
        - reg: (n, n) matrix of regularization strengths
        """
        B = self.B
        t_ls = self.t_ls
        
        if c is None:
            t_diff = np.abs(self.t_ls[:, :, 0] - self.t_ls[:, :, 1])
            i_upper = np.triu_indices_from(t_diff, k=1)
            upper_vals = t_diff[i_upper]
            self.c_threshold = np.quantile(upper_vals, quantile)
            self.c_threshold = max(self.c_threshold, 0.001)
            c = self.c_threshold
        c_squared = c ** 2
        
        reg_upper = np.sqrt(np.sum(B ** 2, axis=-1) / c_squared)
        reg_lower = np.zeros_like(reg_upper) + 1e-7

        t_ls_size = np.sum(t_ls ** 2, axis=-1)
        reg_upper[t_ls_size <= c_squared] = 1e-7

        for _ in range(rounds):
            reg_mid = (reg_upper + reg_lower) / 2
            t_mid_size = self.size(reg_mid)

            reg_lower[t_mid_size > c_squared] = reg_mid[t_mid_size > c_squared]
            reg_upper[t_mid_size < c_squared] = reg_mid[t_mid_size < c_squared]

        return reg_mid

    
    def size(self, reg):
        """
        Computes the squared norm of the perturbation vector (after applying regularization)
        for each (i,j) pair.

        Parameters:
        - reg: (n, n) matrix of regularization strengths

        Returns:
        - size: (n, n) array of perturbation magnitudes
        """
        reg = np.stack([reg, reg], axis=-1)
        E = 1 / (self.eigvals + reg)
        F = (E ** 2) * self.UB
        G = np.einsum("ijk, ijk -> ij", self.UB, F)
        return G

    
    def compute_phase_shift_l2(self, reg=1):
        """
        Computes the regularized perturbation vector in the original basis (not eigenbasis).

        Parameters:
        - reg: (n, n) matrix of regularization strengths

        Returns:
        - t: (n, n, 2) array of regularized perturbation vectors
        """
        B = self.B
        reg = np.stack([reg, reg], axis=-1)
        E = 1 / (self.eigvals + reg)
        F = np.einsum("ijkl, ijl -> ijkl", self.Q_eigen, E)
        G = np.einsum("ijkl, ijtl -> ijkt", F, self.Q_eigen)
        H = np.einsum("ijlk, ijl -> ijk", G, B)
        return H

    
    def pairwise_min_position_distance(self, rounds=30, c=None):
        """
        Computes the pairwise perturbation-based distance matrix between X[i] and X[j],
        incorporating information from Y-space through optimal perturbations.

        Parameters:
        - rounds: number of binary search iterations in regularization

        Returns:
        - dist: (n, n) matrix of perturbation-based distances
        """

        X_squared = np.sum(self.X ** 2, axis=1, keepdims=True)
        X_dist_squared = X_squared + X_squared.T - 2 * self.X @ self.X.T
        
        if c == 0:
            return np.sqrt(X_dist_squared)
        elif c is None:
            c = self.c_threshold
        
        reg = self.find_reg(c=c, rounds=rounds)
        t = self.compute_phase_shift_l2(reg)
        t1 = t[:, :, 0]
        t2 = t[:, :, 1]
        
        Y_squared = np.sum(self.Y ** 2, axis=1, keepdims=True)
        YY = self.Y @ self.Y.T
        XY = self.Y @ self.X.T
        A = np.diag(XY)[:, np.newaxis] - XY

        Y_dist_squared = t1**2 * Y_squared + t2**2 * Y_squared.T - 2 * t1 * t2 * YY
        XY_cross_dist = 2 * t1 * A + 2 * t2 * A.T
        
        dist = X_dist_squared + Y_dist_squared + XY_cross_dist
        dist = np.maximum(dist, 0)       # ensure all values are non-negative
        dist = np.minimum(dist, dist.T) # make the matrix symmetric by taking elementwise min
        dist = np.sqrt(dist)
        return dist
    
    
    def phase_ridge_distance(self, reg=1):
        if reg == 0:
            t = self.t_ls
        else:
            t = self.compute_phase_shift_l2(reg)
        dist = np.abs(t[:, :, 0] - t[:, :, 1])
        dist = np.minimum(dist, dist.T)
        return dist
    
    
    def phase_constrained_L2_distance(self, c=None, rounds=30):
        if c == 0:
            return np.zeros((self.n, self.n))

        reg = self.find_reg(c=c, rounds=rounds)
        t = self.compute_phase_shift_l2(reg)

        dist = np.abs(t[:, :, 0] - t[:, :, 1])
        dist = np.minimum(dist, dist.T)
        return dist
    
        
    def hybrid_position_phase_distance(self, alpha=0.5, method="ridge", rounds=30, c=None, reg=1):
        self.alpha = alpha
        X_norm_sq = np.sum(self.X ** 2, axis=1, keepdims=True)
        dist_sq = X_norm_sq + X_norm_sq.T - 2 * self.X @ self.X.T
        np.fill_diagonal(dist_sq, 0.0)

        if method == "L2_constrained":
            t_dist = self.phase_constrained_L2_distance(c=c, rounds=rounds)
        elif method == "ridge":
            t_dist = self.phase_ridge_distance(reg=reg)
        else:
            raise ValueError(f"Unknown method: {method}")

        t_dist_sq = t_dist ** 2

        if alpha is None:
            # Just normalize both terms equally
            norm1 = np.linalg.norm(dist_sq)
            norm2 = np.linalg.norm(t_dist_sq)
            dist_scaled = dist_sq / norm1
            t_scaled = t_dist_sq / norm2
            return np.sqrt(dist_scaled + t_scaled)
        else:
            # Scale time term so its norm is alpha * norm of dist_sq
            norm1 = np.linalg.norm(dist_sq)
            norm2 = np.linalg.norm(t_dist_sq)
            lam = (alpha * norm1) / (norm2 + 1e-12)  # avoid div by zero
            return np.sqrt(dist_sq + lam * t_dist_sq)

