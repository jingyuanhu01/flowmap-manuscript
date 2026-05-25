import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


class LagrangianPathOptimizer:
    def __init__(self, vf, jacobian, D=1.0, lam=0.0):
        """
        vf: callable(pos) -> velocity vector (d,)
        jacobian: callable(pos) -> Jacobian matrix (d, d) or batched (n, d, d)
        D: diffusion constant
        lam: arc-length regularization weight
        """
        self.vf = vf
        self.jacobian = jacobian
        self.D = D
        self.lam = lam

    # ----------------------------------------------------------------------
    # Core LAP math
    # ----------------------------------------------------------------------
    def dt_uniform(self, n_segments):
        return 1.0 / max(1, n_segments)

    def dt_estimate(self, path, eps=1e-12):
        segs = path[1:] - path[:-1]
        mids = 0.5 * (path[1:] + path[:-1])
        b = np.array([self.vf(y) for y in mids])
        num = np.sum(np.einsum("ij,ij->i", segs, segs))
        den = np.sum(np.einsum("ij,ij->i", b, b))
        return 1.0 if den <= eps else float(np.sqrt(num / den))

    def action_value(self, path, dt=1.0):
        path = np.asarray(path, float)
        segs = path[1:] - path[:-1]
        mids = 0.5 * (path[1:] + path[:-1])
        vf_mids = np.array([self.vf(y) for y in mids])
        v = segs / dt
        residuals = v - vf_mids
        S = 0.5 / self.D * np.sum(np.sum(residuals**2, axis=1) * dt)
        if self.lam > 0:
            S += self.lam * np.sum(np.sum(segs**2, axis=1))
        return float(S)

    def grad_action_analytic(self, path, dt=1.0):
        path = np.asarray(path, float)
        n_plus_1, d = path.shape
        n = n_plus_1 - 1
        grad = np.zeros_like(path)

        segs = path[1:] - path[:-1]
        mids = 0.5 * (path[1:] + path[:-1])
        vf_mids = np.array([self.vf(y) for y in mids])
        v = segs / dt
        g = v - vf_mids
        Jm = self.jacobian(mids)  # (n, d, d)

        for m in range(1, n):
            term_main = g[m - 1] - g[m]
            term_jac = (Jm[m - 1].T @ g[m - 1]) + (Jm[m].T @ g[m])
            grad[m] = (term_main - 0.5 * dt * term_jac) / self.D
            if self.lam > 0:
                grad[m] += 2 * self.lam * (
                    (path[m] - path[m - 1]) - (path[m + 1] - path[m])
                )
        return grad

    def optimize(self, path, dt=None, lr=1e-3, iters=200, callback=None):
        path = np.asarray(path, float).copy()
        n_segments = len(path) - 1
        if dt is None:
            dt = self.dt_uniform(n_segments)

        for it in range(iters):
            g = self.grad_action_analytic(path, dt=dt)
            path[1:-1] -= lr * g[1:-1]  # freeze endpoints
            if callback and (it % 10 == 0 or it == iters - 1):
                S = self.action_value(path, dt=dt)
                callback(it, S)
        return path, dt

    # ----------------------------------------------------------------------
    # Utilities for initialization
    # ----------------------------------------------------------------------
    @staticmethod
    def resample_polyline(points, n_segments=100):
        P = np.asarray(points, float)
        segs = P[1:] - P[:-1]
        lens = np.linalg.norm(segs, axis=1)
        cum = np.r_[0.0, np.cumsum(lens)]
        total = cum[-1]
        targets = np.linspace(0.0, total, n_segments + 1)
        out = np.zeros((n_segments + 1, P.shape[1]))
        j = 0
        for i, s in enumerate(targets):
            while j < len(cum) - 1 and cum[j + 1] < s:
                j += 1
            if cum[j + 1] == cum[j]:
                out[i] = P[j]
            else:
                t = (s - cum[j]) / (cum[j + 1] - cum[j])
                out[i] = P[j] + t * (P[j + 1] - P[j])
        return out

    # ----------------------------------------------------------------------
    # Dijkstra initialization + LAP wrapper
    # ----------------------------------------------------------------------
    def fit_path(self, X, V, start, end, *,
                 X_orig=None,
                 distance_mode="embed",   # {"embed", "orig"}
                 subsample_n=4000, k=20, alpha=0.0,
                 n_segments=100, lr=5e-3, iters=300,
                 plot=True, color=None, **kwargs):
    
        if distance_mode == "orig" and X_orig is None:
            raise ValueError("X_orig must be provided when distance_mode='orig'")
    
        # ------------------------------------------------------------------
        # 1. Subsample points (for graph tractability)
        # ------------------------------------------------------------------
        N = X.shape[0]
        subsample_n = min(subsample_n, N)
        idx_sub = np.random.choice(N, subsample_n, replace=False)
    
        X_sub = X[idx_sub]
        V_sub = V[idx_sub] if V is not None else None
        Xo_sub = X_orig[idx_sub] if X_orig is not None else None
    
        # ------------------------------------------------------------------
        # 2. Force start / end to be present
        # ------------------------------------------------------------------
        start_idx_full = np.argmin(np.linalg.norm(X - start[None, :], axis=1))
        end_idx_full   = np.argmin(np.linalg.norm(X - end[None, :], axis=1))
    
        X_sub = np.vstack([
            X[start_idx_full],
            X[end_idx_full],
            X_sub
        ])
    
        if V_sub is not None:
            V_sub = np.vstack([
                V[start_idx_full],
                V[end_idx_full],
                V_sub
            ])
    
        if Xo_sub is not None:
            Xo_sub = np.vstack([
                X_orig[start_idx_full],
                X_orig[end_idx_full],
                Xo_sub
            ])
    
        root_idx, target_idx = 0, 1
    
        # ------------------------------------------------------------------
        # 3. Choose geometry for graph distances
        # ------------------------------------------------------------------
        X_graph = X_sub if distance_mode == "embed" else Xo_sub
    
        # ------------------------------------------------------------------
        # 4. Build kNN graph
        # ------------------------------------------------------------------
        nbrs = NearestNeighbors(n_neighbors=k + 1, n_jobs=-1).fit(X_graph)
        dists, idxs = nbrs.kneighbors(X_graph)
        idxs, dists = idxs[:, 1:], dists[:, 1:]
    
        rows, cols, weights = [], [], []
    
        for i in range(X_graph.shape[0]):
            for j, d in zip(idxs[i], dists[i]):
                w = d
    
                # Optional velocity alignment penalty (always in embedding space)
                if alpha > 0 and V_sub is not None:
                    v_i = V_sub[i]
                    dir_ij = X_sub[j] - X_sub[i]
                    cos_sim = np.dot(v_i, dir_ij) / (
                        np.linalg.norm(v_i) * np.linalg.norm(dir_ij) + 1e-8
                    )
                    w *= (1 + alpha * (1 - cos_sim))
    
                rows.append(i)
                cols.append(j)
                weights.append(w)
    
        W = csr_matrix(
            (weights, (rows, cols)),
            shape=(X_graph.shape[0], X_graph.shape[0])
        )
    
        # ------------------------------------------------------------------
        # 5. Dijkstra shortest path
        # ------------------------------------------------------------------
        _, predecessors = shortest_path(
            W, directed=False, return_predecessors=True
        )
    
        path = []
        i = target_idx
        while i != root_idx and i != -9999:
            path.append(i)
            i = predecessors[root_idx, i]
        path.append(root_idx)
    
        path_idx = path[::-1]
        path_coords = X_sub[path_idx]  # ALWAYS embedding coords
    
        # ------------------------------------------------------------------
        # 6. Resample + LAP refinement
        # ------------------------------------------------------------------
        path_init = self.resample_polyline(
            path_coords, n_segments=n_segments
        )
    
        def cb(it, S):
            if it % 50 == 0 or it == iters - 1:
                print(f"[LAP] iter={it:03d}, S={S:.6f}")
    
        path_refined, dt = self.optimize(
            path_init, lr=lr, iters=iters, callback=cb
        )
    
        return {
            "path_init": path_init,
            "path_refined": path_refined,
            "dt": dt,
            "X_sub": X_sub,
            "idx_sub": idx_sub,
        }
