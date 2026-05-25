import numpy as np
from numpy.linalg import lstsq, eigvals
from scipy.ndimage import gaussian_filter
from sklearn.neighbors import NearestNeighbors
from scipy.stats import norm as normal


def compute_velocity_on_grid(
    X_emb,
    tps_vf=None,
    *,
    grid_size=100,
    grid_density=1.0,
    smooth=0.5,
    n_neighbors=None,
    min_mass=0.01,
    margin_ratio=0.0,
    return_mesh=False
):
    """
    Build a rectilinear grid over the embedding, filter low-density cells,
    and (optionally) evaluate a velocity field.
    """
    idx_valid = np.isfinite(X_emb).all(axis=1)
    X_emb = X_emb[idx_valid]
    if X_emb.size == 0:
        raise ValueError("No valid points.")

    n_obs, d = X_emb.shape
    if n_neighbors is None:
        n_neighbors = max(10, int(n_obs / 30))

    # --- define grid bounds ---
    bounds, grids = [], []
    for i in range(d):
        lo, hi = np.min(X_emb[:, i]), np.max(X_emb[:, i])
        pad = 0.01 * (hi - lo + 1e-5)
        lo, hi = lo - pad, hi + pad
        bounds.append((lo, hi))
        grids.append(np.linspace(lo, hi, int(grid_size * grid_density)))

    meshes = np.meshgrid(*grids, indexing="xy")
    X_grid = np.vstack([g.ravel() for g in meshes]).T

    # --- density weighting ---
    nn = NearestNeighbors(n_neighbors=n_neighbors, n_jobs=-1).fit(X_emb)
    dists, _ = nn.kneighbors(X_grid)
    scale = np.mean([(g[1] - g[0]) for g in grids]) * smooth
    p_mass = normal.pdf(dists, scale=scale).sum(1)
    keep = p_mass > (np.percentile(p_mass, 99) * min_mass)

    Xg = X_grid[keep]

    # --- boundary cropping ---
    if margin_ratio > 0:
        mask_margin = np.ones(len(Xg), bool)
        for i in range(d):
            lo, hi = bounds[i]
            margin = margin_ratio * (hi - lo)
            mask_margin &= (Xg[:, i] > lo + margin) & (Xg[:, i] < hi - margin)
        Xg = Xg[mask_margin]

    # --- optional velocity prediction ---
    Vg = tps_vf.predict(Xg) if tps_vf is not None else None

    if return_mesh:
        return Xg, keep, Vg, meshes
    return Xg, keep, Vg



class FixedPointAnalyzer:
    def __init__(self, emb):
        self.emb = emb
        self.X_emb = emb.X_emb          # (N, d)
        self.V_emb = emb.V_emb          # (N, d)
        self.tps = emb.tps
        self.tps_vf = emb.tps_vf

        self.fixed_points = []
        self.fixed_point_info = []

    # ---------------------------------------------------------------
    # Fixed-point identification with metric-aware smoothing
    # ---------------------------------------------------------------
    def identify_fixed_points(
        self,
        *,
        grid_size=100,
        speed_smooth_sigma=1.0,
        global_speed_quantile=0.10,
        radius_percent=0.2,
        weighted=True,
    ):
        """
        Identify and classify fixed points of the vector field by:

        1) Evaluating metric speed on a dense grid
        2) Applying Gaussian smoothing to the speed field
        3) Detecting local minima on the smoothed grid
        4) Performing local metric flattening and Jacobian-based classification
        """

        # -----------------------------------------------------------
        # 1. Grid sampling + metric speed
        # -----------------------------------------------------------
        Xg, keep, Vg, meshes = compute_velocity_on_grid(
            self.X_emb,
            tps_vf=self.tps_vf,
            grid_size=grid_size,
            grid_density=1.0,
            min_mass=0.01,
            return_mesh=True,
        )

        Gg = self.tps.compute_metric(Xg)
        speed = np.sqrt(np.einsum("ni,nij,nj->n", Vg, Gg, Vg))

        # -----------------------------------------------------------
        # 2. Reconstruct full grid speed field
        # -----------------------------------------------------------
        speed_full = np.full(meshes[0].shape, np.nan)
        speed_full.ravel()[keep] = speed

        # fill NaNs with large value to avoid boundary artifacts
        fill_value = np.nanmax(speed_full)
        speed_filled = np.nan_to_num(speed_full, nan=fill_value)

        # -----------------------------------------------------------
        # 3. Gaussian smoothing (tunable bandwidth)
        # -----------------------------------------------------------
        from scipy.ndimage import gaussian_filter
        speed_smooth = gaussian_filter(
            speed_filled,
            sigma=speed_smooth_sigma,
            mode="nearest",
        )

        # -----------------------------------------------------------
        # 4. Local minimum detection on smoothed grid
        # -----------------------------------------------------------
        def local_minima_2d(Z):
            mask = np.ones_like(Z, dtype=bool)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    mask &= Z < np.roll(np.roll(Z, di, axis=0), dj, axis=1)
            mask[0, :] = mask[-1, :] = False
            mask[:, 0] = mask[:, -1] = False
            return mask

        min_mask = local_minima_2d(speed_smooth)
        idx = np.argwhere(min_mask)
        
        if len(idx) == 0:
            self.fixed_points = []
            self.fixed_point_info = []
            return []
        
        # -----------------------------------------------------------
        # 4.1 Loose global speed filter (exclude local deceleration)
        # -----------------------------------------------------------
        global_thresh = np.nanquantile(speed, global_speed_quantile)
        
        # map grid indices -> flat indices
        flat_idx = np.ravel_multi_index(
            (idx[:, 0], idx[:, 1]),
            dims=speed_full.shape
        )
        
        candidate_speed = speed_full.ravel()[flat_idx]
        keep = candidate_speed <= global_thresh
        
        idx = idx[keep]
        
        if len(idx) == 0:
            self.fixed_points = []
            self.fixed_point_info = []
            return []
        
        fps = np.column_stack([
            meshes[0][idx[:, 0], idx[:, 1]],
            meshes[1][idx[:, 0], idx[:, 1]],
        ])
        
        # -----------------------------------------------------------
        # 4.2 Optional refinement of fixed-point candidates
        # -----------------------------------------------------------
        from scipy.optimize import minimize

        def vf_energy(x, tps_vf):
            v = tps_vf.predict(x[None, :])[0]
            return np.dot(v, v)
     
        # estimate grid spacing from meshes
        dx = float(meshes[0][0, 1] - meshes[0][0, 0])
        dy = float(meshes[1][1, 0] - meshes[1][0, 0])
        grid_step = np.mean([dx, dy])
        
        # max allowed refinement distance
        bound_radius = np.sqrt(dx**2 + dy**2)
        refined_fps = []
        
        for fp0 in fps:
            bounds = [
                (fp0[i] - bound_radius, fp0[i] + bound_radius)
                for i in range(fp0.shape[0])
            ]
        
            try:
                res = minimize(
                    vf_energy,
                    x0=fp0,
                    args=(self.tps_vf,),
                    method="L-BFGS-B",
                    bounds=bounds,
                    options=dict(
                        maxiter=15,     # small, safe
                        ftol=1e-8,
                        gtol=1e-6,
                    ),
                )
                if res.success:
                    refined_fps.append(res.x)
                else:
                    refined_fps.append(fp0)
        
            except Exception:
                refined_fps.append(fp0)
        
        fps = np.asarray(refined_fps)

        # -----------------------------------------------------------
        # 5. Local metric flattening + Jacobian + classification
        # -----------------------------------------------------------
        for fp in fps:
            # --- choose radius in embedding space ---
            emb_range = np.ptp(self.X_emb, axis=0)
            radius = radius_percent * np.mean(emb_range)
            
            # --- robust local metric (independent of data points) ---
            eps = 0.25 * radius
            g_fp = self.estimate_local_metric(
                fp,
                eps=eps,
                n_samples=32,
            )
            
            L = np.linalg.cholesky(g_fp)
            
            # --- neighborhood selection using metric ---
            dx = self.X_emb - fp
            dist2 = np.einsum("ni,ij,nj->n", dx, g_fp, dx)
            mask = dist2 < radius**2

            if np.sum(mask) < 10:
                continue

            x_flat = dx[mask] @ L.T
            v_flat = self.V_emb[mask] @ L.T

            x_flat = dx[mask]
            v_flat = self.V_emb[mask]

            try:
                J = self.fit_vf_jacobian(
                    fp=np.zeros(fp.shape[0]),
                    x_flat=x_flat,
                    v_flat=v_flat,
                    radius_percent=1.0,
                    weighted=weighted,
                )
                fp_type = self.classify_fixed_point(J)
            except ValueError:
                J = None
                fp_type = "Unclassified"

            self.fixed_point_info.append(
                dict(
                    position=fp,
                    metric=g_fp,
                    jacobian=J,
                    type=fp_type,
                )
            )

        return self.fixed_point_info

    
    def estimate_local_metric(
        self,
        fp,
        *,
        eps,
        n_samples=32,
        jitter=1e-6,
        random_state=None,
    ):
        """
        Robust local metric estimation by averaging g(x)
        over random samples in a small epsilon-ball.
        """
        rng = np.random.default_rng(random_state)
    
        d = fp.shape[0]
    
        # sample points uniformly in a unit ball
        Z = rng.normal(size=(n_samples, d))
        Z /= np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12
        r = rng.uniform(0.0, 1.0, size=(n_samples, 1)) ** (1.0 / d)
        Z = r * Z
    
        X_probe = fp[None, :] + eps * Z
    
        # evaluate metric at probe points
        G = self.tps.compute_metric(X_probe)  # (n_samples, d, d)
    
        # simple Euclidean average (sufficiently local)
        g_avg = G.mean(axis=0)
    
        # enforce symmetry + jitter
        g_avg = 0.5 * (g_avg + g_avg.T)
        g_avg += jitter * np.eye(d)
    
        return g_avg

    
    # ---------------------------------------------------------------
    # Local Jacobian fitting (locally flat coordinates)
    # ---------------------------------------------------------------
    @staticmethod
    def fit_vf_jacobian(
        fp,
        x_flat,
        v_flat,
        *,
        radius_percent=0.2,
        weighted=True,
    ):
        """
        Estimate the Jacobian of the vector field in locally flattened
        coordinates via weighted least squares.
        """
        emb_range = np.ptp(x_flat, axis=0)
        radius = radius_percent * np.mean(emb_range)

        dx = x_flat - fp
        mask = np.linalg.norm(dx, axis=1) < radius

        Xloc = dx[mask]
        Vloc = v_flat[mask]

        if Xloc.shape[0] < 3 * Xloc.shape[1]:
            raise ValueError("Neighborhood too small for Jacobian fit.")

        if weighted:
            sigma = 0.5 * radius
            w = np.exp(-np.sum(Xloc**2, axis=1) / (2 * sigma**2))[:, None]
            Xw = Xloc * w
            Vw = Vloc * w
        else:
            Xw, Vw = Xloc, Vloc

        J, *_ = lstsq(Xw, Vw, rcond=None)
        return J

    # ---------------------------------------------------------------
    # Fixed-point classification from Jacobian spectrum
    # ---------------------------------------------------------------
    @staticmethod
    def classify_fixed_point(J, eps=1e-4):
        eigs = eigvals(J)
        re, im = eigs.real, eigs.imag
        has_im = np.any(np.abs(im) > eps)

        if not has_im:
            if np.all(re < -eps): return "Stable node (sink)"
            if np.all(re >  eps): return "Unstable node (source)"
            if np.any(re > eps) and np.any(re < -eps): return "Saddle"
            return "Degenerate node"

        a = re[np.abs(im) > eps][0]
        if np.abs(a) < eps: return "Center (rotation)"
        if a < 0: return "Spiral in (stable)"
        if a > 0: return "Spiral out (unstable)"
        return "Mixed focus"
