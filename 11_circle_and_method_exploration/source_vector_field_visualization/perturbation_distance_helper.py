import numpy as np

class PerturbDistanceSolver:
    """
    Computes a regularized perturbation-based distance metric between data points in X and Y.
    The core idea is to learn a minimal perturbation in Y-space that aligns with X, under
    a quadratic regularization constraint.
    """

    def __init__(self, X, Y, method="L2_constrained"):
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
        a = Q[..., 0, 0]
        b = Q[..., 0, 1]
        c = Q[..., 1, 0]
        d = Q[..., 1, 1]
        det = a * d - b * c
        det += 1e-8 * np.eye(self.n)  # For numerical stability

        inv_Q = np.empty_like(Q)
        inv_Q[..., 0, 0] = d / det
        inv_Q[..., 0, 1] = -b / det
        inv_Q[..., 1, 0] = -c / det
        inv_Q[..., 1, 1] = a / det

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
        lam = np.stack([lambda1, lambda2], axis=-1)

        Q_eigen = np.empty_like(Q)
        Q_eigen[:, :, 0, 0] = Q[:, :, 0, 1]
        Q_eigen[:, :, 1, 1] = Q[:, :, 1, 0]
        Q_eigen[:, :, 0, 1] = Q[:, :, 0, 0] - lambda1
        Q_eigen[:, :, 1, 0] = Q[:, :, 1, 1] - lambda2

        norms = np.sqrt(np.einsum('ijkl, ijkl -> ijk', Q_eigen, Q_eigen)) + 1e-8
        Q_eigen = np.einsum('ijkl,ijk->ijkl', Q_eigen, 1 / norms)

        # Store everything
        self.Q = Q
        self.inv_Q = inv_Q
        self.B = B
        self.t_ls = t_ls
        self.lam = lam
        self.Q_eigen = Q_eigen
        self.UB = np.einsum("ijkl, ijk -> ijl", Q_eigen, B)
        
        

    def find_reg(self, c=0.5, rounds=10):
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
        c_squared = c ** 2
        
        reg_upper = np.sqrt(np.sum(B ** 2, axis=-1) / c_squared)
        reg_lower = np.zeros_like(reg_upper) + 1e-8

        t_ls_size = np.sum(t_ls ** 2, axis=-1)
        reg_upper[t_ls_size <= c_squared] = 1e-8

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
        E = 1 / (self.lam + reg)
        F = (E ** 2) * self.UB
        G = np.einsum("ijk, ijk -> ij", self.UB, F)
        return G

    def time_l2(self, reg):
        """
        Computes the regularized perturbation vector in the original basis (not eigenbasis).

        Parameters:
        - reg: (n, n) matrix of regularization strengths

        Returns:
        - t: (n, n, 2) array of regularized perturbation vectors
        """
        B = self.B
        reg = np.stack([reg, reg], axis=-1)
        E = 1 / (self.lam + reg)
        F = np.einsum("ijkl, ijl -> ijkl", self.Q_eigen, E)
        G = np.einsum("ijkl, ijtl -> ijkt", F, self.Q_eigen)
        H = np.einsum("ijlk, ijl -> ijk", G, B)
        return H

    
    def pairwise_min_position_distance(self, rounds, c=0.5):
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
        
        reg = self.find_reg(c=c, rounds=rounds)
        t = self.time_l2(reg)
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
    
    
    def pairwise_time_ridge_distance(self, reg):
        if reg == 0:
            t = self.t_ls
        else:
            t = self.time_l2(reg)
        dist = np.abs(t[:, :, 0] - t[:, :, 1])
        dist = np.minimum(dist, dist.T)
        return dist
    
    
    def pairwise_time_constrained_L2_distance(self, c=0.5, rounds=30):
        X_squared = np.sum(self.X ** 2, axis=1, keepdims=True)
        X_dist_squared = X_squared + X_squared.T - 2 * self.X @ self.X.T

        if c == 0:
            return np.sqrt(X_dist_squared)

        reg = self.find_reg(c=c, rounds=rounds)
        t = self.time_l2(reg)

        dist = np.abs(t[:, :, 0] - t[:, :, 1])
        dist = np.minimum(dist, dist.T)
        return dist
    
        
    def pairwise_perturb_distance(self, alpha, method="L2_constrained", c=0.5, rounds=30, reg=10):
        X_norm_sq = np.sum(self.X ** 2, axis=1, keepdims=True)
        dist_sq = X_norm_sq + X_norm_sq.T - 2 * self.X @ self.X.T

        if method == "L2_constrained":
            t_dist = self.pairwise_time_constrained_L2_distance(c=c, rounds=rounds)
        elif method == "ridge":
            t_dist = self.pairwise_time_ridge_distance(reg)
        else:
            raise ValueError(f"Unknown method: {method}")

        return np.sqrt(dist_sq + alpha * t_dist ** 2)

    
    
    
        