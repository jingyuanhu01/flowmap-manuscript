import numpy as np
from scipy.spatial.distance import cdist
from numpy.linalg import solve, svd
from scipy.optimize import root_scalar
from sklearn.cluster import KMeans
from scipy.stats import f
from statsmodels.stats.multitest import multipletests


class ThinPlateSpline:
    def __init__(self, X, n_control_points=1000, max_n=4000):
        """
        Thin Plate Spline initializer.

        Args:
            X (np.ndarray): Training input points of shape (N, d).
            n_control_points (int): Number of control points to use.
            max_n (int): Warning threshold — recommend subsampling if N > max_n.
        """
        self.full_X = X  # For debugging/inspection
        self.N_total, self.d = X.shape

        # --- issue warning if too large ---
        if self.N_total > max_n:
            print(f"[TPS ⚠️] Input has {self.N_total} points. "
                  f"This may be slow — consider subsampling ≤ {max_n} points.")

        self.X = X
        self.N = X.shape[0]

        # --- control point selection ---
        if n_control_points is None or n_control_points >= self.N:
            self.control_indices = np.arange(self.N)
        else:
            self.control_indices = self._select_control_points_kmeans(X, n_control_points)
        self.control_points = self.X[self.control_indices]

        # --- kernel computation ---
        pairwise_distances = cdist(self.X, self.control_points)
        self.Phi = self.tps_kernel(pairwise_distances)
        self.K = self.Phi


    def tps_kernel(self, r):
        """
        Compute dimension-aware TPS kernel.

        φ_d(r) =
            r^2 * log(r),   if d == 2
            r,              if d == 3
            r^(2 - d),      otherwise (up to constant scaling)

        Ensures φ(0) = 0 to avoid singularities.
        """
        d = self.d  # embedding dimension
        r = np.asarray(r, dtype=float)
        result = np.zeros_like(r)

        mask = r > 0
        if d == 2:
            result[mask] = (r[mask] ** 2) * np.log(r[mask])
        elif d == 3:
            result[mask] = r[mask]
        else:
            result[mask] = r[mask] ** (2 - d)

        return result
    

    def _select_control_points_kmeans(self, X, n_control_points):
        """
        Selects control points from the training data using k-means clustering.
        For each cluster center, the training point closest to the center is chosen.

        Args:
            X (np.ndarray): Training input points of shape (N, d).
            n_control_points (int): Number of control points (clusters) desired.

        Returns:
            np.ndarray: Indices of the selected control points.
        """
        kmeans = KMeans(n_clusters=n_control_points, random_state=0)
        kmeans.fit(X)
        centers = kmeans.cluster_centers_
        
        # For each cluster center, find the index of the closest training point.
        indices = []
        for center in centers:
            distances = np.linalg.norm(X - center, axis=1)
            indices.append(np.argmin(distances))
        return np.array(indices)

    
    def compute_dof(self, lambda_reg):
        """
        Computes the degrees of freedom using the squared singular values of the kernel matrix.

        The formula is:
            dof = sum( s_i^2 / (s_i^2 + lambda_reg) )
        where s_i are the singular values of the kernel matrix.

        Args:
            lambda_reg (float): Regularization parameter.

        Returns:
            float: Computed degrees of freedom.
        """
        Phi = getattr(self, "K", self.Phi)
        if self.singular_values is None:
            _, S, _ = svd(Phi)
            self.singular_values = S  # Cache singular values.
        S = self.singular_values
        radial_dof = np.sum(S**2 / (S**2 + lambda_reg))
        
        # Polynomial (affine) part: d+1
        poly_dof = self.d + 1  # if self.d is dimensionality
        
        return radial_dof + poly_dof
    
    
    def find_lambda_for_dof(self, dof, tol=1e-3, fallback_lambda=1e6):
        """
        Finds the regularization parameter (lambda_reg) that achieves a target degrees 
        of freedom using a numerical root solver. Falls back to a fixed lambda if search fails.
        """
        def f(lam):
            return self.compute_dof(lam) - dof

        try:
            f_low = f(1e-6)
            f_high = f(1e6)

            if f_low * f_high > 0:
                raise ValueError(
                    f"The specified dof_target ({dof}) is too small or otherwise infeasible. "
                    f"f(1e-6) = {f_low} and f(1e6) = {f_high} do not have opposite signs."
                )

            sol = root_scalar(f, bracket=[1e-6, 1e6], xtol=tol, method='brentq')
            if sol.converged:
                return sol.root
            else:
                raise RuntimeError("Lambda finding did not converge.")

        except Exception as e:
            print(f"Warning: Lambda search failed: {e}")
            print(f"Setting lambda_reg = {fallback_lambda}")
            computed_dof = self.compute_dof(fallback_lambda)
            print(f"Resulting degrees of freedom: {computed_dof:.2f}")
            return fallback_lambda
    
    
    def fit(self, Y, lambda_reg=None, dof=None, dof_target=None):
        """
        Fits the Thin Plate Spline model using a ridge-regression formulation.

        The model is expressed as:
             f(x) = Phi(x) * w + P(x) * a,
        where Phi(x) = [phi(||x - c_1||), ..., phi(||x - c_m||)] and
        P(x) = [1, x_1, ..., x_d].

        The parameters z = [w; a] are found by minimizing
             ||Y - [Phi, P] * z||^2 + lambda * ||w||^2.
        If dof is specified, lambda_reg is computed to achieve the desired
        effective degrees of freedom.

        Args:
            Y (np.ndarray): Output data of shape (N, D).
            lambda_reg (float or None): Regularization parameter. If None and dof_target
                                        is provided, lambda_reg is determined automatically.
            dof (float or None): Target degrees of freedom.

        Returns:
            self: The fitted model, with attributes:
                  - self.weights (w): radial basis weights, shape (m, D)
                  - self.coeffs (a): affine coefficients, shape (d+1, D)
                  - self.lambda_reg: used regularization parameter.
        """
        # Initialize attributes that will be set during fitting.
        self.weights = None
        self.coeffs = None
        self.dof = None
        self.singular_values = None  # Cache singular values for DOF calculation
        self.lambda_reg = None       # Store the used regularization parameter
        
        
        N = self.N
        D = Y.shape[1]
        m = self.control_points.shape[0]  # number of control points

        # Backward compatibility for older notebooks.
        if dof is None and dof_target is not None:
            dof = dof_target

        # Determine lambda_reg based on target DOF if specified.
        if dof is not None:
            lambda_reg = self.find_lambda_for_dof(dof)
        if lambda_reg is None:
            lambda_reg = 0.0
        self.lambda_reg = lambda_reg

        # Compute the design matrices.
        # Phi: shape (N, m) [this is self.K as computed in __init__]
        Phi = getattr(self, "K", self.Phi)
        # P: affine design matrix, shape (N, d+1)
        P = np.hstack((np.ones((N, 1)), self.X))
        # Combined design matrix: X_design: shape (N, m + d + 1)
        X_design = np.hstack((Phi, P))

        # Build the augmentation for the ridge penalty.
        # We only penalize the first m parameters (the w's).
        # Create a block for regularization: shape (m, m+d+1)
        reg_block = np.hstack((np.sqrt(lambda_reg) * np.eye(m), np.zeros((m, self.d + 1))))

        # Augment the design matrix and target.
        A_aug = np.vstack((X_design, reg_block))  # shape: (N + m, m+d+1)
        Y_aug = np.vstack((Y, np.zeros((m, D))))    # shape: (N + m, D)

        # Solve the augmented least-squares problem.
        z, residuals, rank, s = np.linalg.lstsq(A_aug, Y_aug, rcond=None)

        # Partition the solution.
        self.weights = z[:m]       # radial basis weights, shape (m, D)
        self.coeffs  = z[m:]       # affine coefficients, shape (d+1, D)

        # Optionally, update the effective degrees of freedom.
        # (For ridge regression, a common formula is:
        #   dof = sum_{i=1}^{m} s_i^2/(s_i^2 + lambda_reg),
        # where s_i are the singular values of Phi.)
        self.dof = self.compute_dof(lambda_reg)
        self.Y_train = Y

        return self
    
    def predict(self, X_new):
        """
        Predicts outputs for new input data.

        Args:
            X_new (np.ndarray): New input points of shape (M, d) or (d,).

        Returns:
            np.ndarray: Predicted outputs of shape (M, D) or (D,) if input was 1D.
        """
        # Ensure X_new is 2D
        X_new = np.atleast_2d(X_new)
        was_1d = (X_new.shape[0] == 1 and X_new.shape[1] == self.control_points.shape[1])

        # Compute the kernel matrix between new inputs and the control points.
        pairwise_distances = cdist(X_new, self.control_points, metric="euclidean")
        K_new = self.tps_kernel(pairwise_distances)

        # Build the affine term for the new inputs.
        P_new = np.hstack((np.ones((X_new.shape[0], 1)), X_new))
        predictions = K_new @ self.weights + P_new @ self.coeffs

        if was_1d:
            return predictions[0]  # Return 1D output for single input point
        return predictions


    def compute_jacobians(self, evaluation_points, eps=1e-10):
        """
        Compute the Jacobians of the Thin Plate Spline (TPS) function for multiple evaluation points.

        Parameters:
            evaluation_points (np.ndarray): Evaluation points of shape (num_evals, d) in d-dimensional space.
        
        Uses:
            self.control_points (np.ndarray): Control points (num_controls, d).
            self.weights (np.ndarray): TPS weights of shape (num_controls, target_dim).
            self.coeffs (np.ndarray): Affine transformation coefficients of shape (d+1, target_dim).

        Returns:
            np.ndarray: Jacobians for all evaluation points with shape (num_evals, target_dim, d).
        """
        control_points = self.control_points
        weights = self.weights
        coeffs = self.coeffs

        # Get dimensions.
        num_evals, d = evaluation_points.shape  # Number of evaluation points & space dimension.
        num_controls = control_points.shape[0]    # Number of control points.
        target_dim = weights.shape[1]             # Output dimension.

        # Compute pairwise differences: shape (num_evals, num_controls, d)
        diffs = evaluation_points[:, None, :] - control_points[None, :, :]

        # Compute distances r_i(x_j): shape (num_evals, num_controls, 1)
        r_i = np.linalg.norm(diffs, axis=2, keepdims=True)

        # Mask to avoid division by zero.
        valid_mask = r_i > 1e-10

        # Compute normalized direction vectors (only where r_i > 0).
        direction_vectors = np.zeros_like(diffs)
        direction_vectors[valid_mask[..., 0], :] = diffs[valid_mask[..., 0], :] / r_i[valid_mask[..., 0]]

        # Compute the derivative term.
        derivative_term = np.zeros_like(r_i)
        derivative_term[valid_mask] = (1 + 2 * np.log(r_i[valid_mask])) * r_i[valid_mask]

        # Compute derivative contributions (fully vectorized).
        derivative_vectors = weights.T @ (derivative_term * direction_vectors)
        # derivative_vectors now has shape (target_dim, num_evals, d)

        # Add linear (affine) part.
        affine_term = coeffs[1:, :].T[None, :, :]  # shape (1, target_dim, d)

        # Combine derivative and affine terms.
        Jacobians = derivative_vectors + affine_term  # shape (target_dim, num_evals, d)

        return Jacobians

    def compute_tps_jacobians(self, evaluation_points, eps=1e-10):
        """Backward-compatible alias used by older notebooks."""
        return self.compute_jacobians(evaluation_points, eps=eps)
    
    def compute_hessians(self, evaluation_points, eps=1e-10):
        # Extract TPS parameters
        control_points = self.control_points
        weights = self.weights

        # Get dimensions
        M, d_dim = evaluation_points.shape  # Number of evaluation points and input dimension
        N = control_points.shape[0]         # Number of control points
        output_dim = weights.shape[1]       # Number of output dimensions

        # Compute differences for all eval points and control points: shape (M, N, d)
        d = evaluation_points[:, None, :] - control_points[None, :, :]

        # Compute r = ||d|| for each pair (M, N)
        r = np.linalg.norm(d, axis=2) + eps  # Shape (M, N)
        r = r[:, :, None, None]  # Reshape for broadcasting: (M, N, 1, 1)

        # Identity matrix (d, d)
        I = np.eye(d_dim)

        # Compute the outer product efficiently for all eval points: shape (M, N, d, d)
        outer = np.einsum('mni,mnj->mnij', d, d)

        # Compute Hessian for all control points at once: shape (M, N, d, d)
        H_individual = 2 * outer / (r**2) + (2 * np.log(r) + 1) * I

        # Compute weighted sum over control points: shape (M, output_dim, d, d)
        H = np.einsum("mnij,nk->mkij", H_individual, weights)

        return H
    
       
    def compute_metric(self, evaluation_points, eps=1e-8):
        jacobians = self.compute_jacobians(evaluation_points, eps=eps)
        metrics = np.einsum('ndi,ndj->nij', jacobians, jacobians)
        return metrics
    
    
    def compute_christoffels(self, evaluation_points, eps=1e-8):
        """
        Return Γ^k_{ij} for every evaluation point.
        Shapes:
            J  : (N, d, 2)          – Jacobians  ∂x/∂u^i
            H  : (N, d, 2, 2)       – Hessians   ∂²x/∂u^i∂u^j
            g  : (N, 2, 2)          – metric     g_{ij}=e_i·e_j
            g⁻¹: (N, 2, 2)          – inverse
            S  : (N, 2, 2, 2)       – inner prods 〈H_{ij},e_m〉
            Γ  : (N, 2, 2, 2)       – Christoffels Γ^k_{ij}
        """
        J = self.compute_jacobians(evaluation_points, eps=eps)          # (N,d,2)
        H = self.compute_hessians(evaluation_points, eps=eps)           # (N,d,2,2)

        # metric g_{ij}=e_i·e_j   (einsum over ambient dim d)
        g = np.einsum('ndi,ndj->nij', J, J)                             # (N,2,2)
        g_inv = np.linalg.inv(g)                                        # (N,2,2)

        # S_{ijm}=〈H_{ij},e_m〉   (dot ambient dim d)
        S = np.einsum('ndij,ndm->nijm', H, J)                           # (N,2,2,2)

        # Γ^k_{ij}=g^{km} S_{ijm}
        Gamma = np.einsum('nkm,nijm->nijk', g_inv, S)                   # (N,2,2,2)

        return Gamma            # shape (N, k, i, j)  with k,i,j = 0,1

    
    def compute_torsion(self, evaluation_points, eps=1e-8):
        """
        Compute torsion tensor T^k_{ij} = Γ^k_{ij} - Γ^k_{ji}.

        Parameters:
            Gamma (N, k, i, j): Christoffel symbols at N points, shape (N, 2, 2, 2).

        Returns:
            torsion (N, 2, 2, 2): Torsion tensor.
            torsion_norm (N,): Scalar "torsion magnitude" per point.
        """
        Gamma = self.compute_christoffels(evaluation_points, eps=1e-8)
        T = Gamma - np.swapaxes(Gamma, axis1=2, axis2=3)  # T^k_{ij} = Γ^k_{ij} - Γ^k_{ji}
        return T
    
    
    def curvature(self, evaluation_points, eps=1e-12):
        # 1. first & second derivatives of embedding F=(t,x,y)
        J  = self.compute_jacobians(evaluation_points, eps=eps)       # (N,3,2)
        H  = self.compute_hessians (evaluation_points, eps=eps)       # (N,3,2,2)

        # 2. metric g_ij = e_i·e_j   and its inverse
        g      = np.einsum('nki,nkj->nij', J, J)            # (N,2,2)
        g_inv  = np.linalg.inv(g)

        # J: (N, D, 2)   H: (N, D, 2, 2)
        D = J.shape[1]

        # --- step 3: orthonormal normal basis -----------------------------
        # SVD batch-wise
        U, S, Vh = np.linalg.svd(J, full_matrices=True)
        Nmat = U[:, :, 2:]            # (N, D, D-2)  normal basis vectors

        # project Hessian on every normal
        #   K_A[n,i,j,A] = <H[n,:,i,j], nA>
        K = np.einsum('ndij,ndA->nAij', H, Nmat)   # (N, D-2, 2, 2)

        # 5. Gauss equation  R_ijkl = h_ik h_jl - h_il h_jk
        #    Build outer products of K
        h1 = np.einsum('nAik,nAjl->nAijkl', K, K)
        h2 = np.einsum('nAil,nAjk->nAijkl', K, K)
        Riem = np.sum(h1 - h2, axis=1)               # sum over A  → (N,2,2,2,2)

        # 6. Ricci  R_jl = g^{ik} R_ijkl
        Ric = np.einsum('nik,nijkl->njl', g_inv, Riem)      # (N,2,2)

        # 7. Scalar  R = g^{jl} R_jl
        Rsc = np.einsum('njl,njl->n', g_inv, Ric)           # (N,)

        return K, Riem, Ric, Rsc, Nmat
    
    
    @staticmethod
    def fdr_bh_logp(log_p):
        """FDR correction directly on log p-values (Benjamini–Hochberg)."""
        m = len(log_p)
        idx = np.argsort(log_p)  # ascending: most negative (smallest p) first
        log_p_sorted = log_p[idx]

        log_m = np.log(m)
        log_i = np.log(np.arange(1, m + 1, dtype=float))

        # Compute log(p * m / i)
        log_p_adj = log_p_sorted + (log_m - log_i)

        # Enforce monotonicity (non-decreasing adj p)
        for i in range(m - 2, -1, -1):
            log_p_adj[i] = np.minimum(log_p_adj[i], log_p_adj[i + 1])

        # Reorder back
        log_p_adj_unsorted = np.empty_like(log_p)
        log_p_adj_unsorted[idx] = log_p_adj
        return log_p_adj_unsorted

    
    def evaluate_fit(self, X, Y=None):
        """Evaluate TPS model fit with FDR-corrected statistics."""
        if Y is None:
            # Older notebooks called evaluate_fit(Y) after fit(Y).
            # Interpret a dimensionality mismatch as that legacy calling style.
            X = np.asarray(X)
            if X.ndim == 2 and X.shape[1] != self.d:
                Y = X
                X = self.X
            elif hasattr(self, "Y_train"):
                Y = self.Y_train
            else:
                raise ValueError("Y must be provided when the TPS model has no stored training target.")
        Y_pred = self.predict(X)
        N, D = Y.shape

        RSS = np.sum((Y - Y_pred) ** 2, axis=0)
        TSS = np.sum((Y - np.mean(Y, axis=0)) ** 2, axis=0)
        rmse = np.sqrt(np.mean((Y - Y_pred) ** 2))
        R2 = 1 - RSS / (TSS + 1e-12)

        gcv = (np.sum(RSS) / N) / (1 - (self.dof / N)) ** 2

        edf = min(self.dof, N - 2)
        F_stat = (R2 / edf) / ((1 - R2) / (N - edf - 1))
        F_stat = np.maximum(F_stat, 0)

        log_p = f.logsf(F_stat, edf, N - edf - 1)
        log_p_adj = self.fdr_bh_logp(log_p)

        # optional: for readability or legacy comparison
        p_value = np.exp(log_p)
        _, p_adj, _, _ = multipletests(p_value, method="fdr_bh")

        return {
            "RMSE": rmse,
            "R2": R2,
            "GCV": gcv,
            "F_stat": F_stat,
            "log_p": log_p,
            "log_p_adj": log_p_adj,
            "p_value": p_value,
            "p_adj": p_adj,
        }
    
    
    def map_velocities(self, V):
        """
        Projects velocities using the TPS Jacobians.

        Args:
            X_2d (np.ndarray): Input 2D points of shape (n, 2).
            Y (np.ndarray): Target velocities of shape (n, d).

        Returns:
            np.ndarray: Projected velocities of shape (n, 2).
        """
        jacobians = self.compute_jacobians(self.X)
        mapped_velocities = np.zeros_like(self.X)

        for i in range(self.X.shape[0]):
            mapped_velocities[i], _, _, _ = np.linalg.lstsq(jacobians[i], V[i], rcond=None)

        return mapped_velocities

    def project_velocities(self, *args):
        """Backward-compatible alias used by older notebooks."""
        V = args[-1]
        return self.map_velocities(V)
    
