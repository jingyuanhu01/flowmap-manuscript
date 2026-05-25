from dataclasses import dataclass
import numpy as np
from scipy.spatial import cKDTree
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import pairwise_distances
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter1d, maximum_filter

# Optional: turn this on if you want reproducible randomness across runs
# np.random.seed(0)

class StochasticPseudotime:
    """
    Stochastic pseudotime inference using a continuous vector field.
    Boundary detection is handled by a KDE-based inlier set and a KD-tree
    with a hard distance cutoff. Metric-aware noise uses a cached Cholesky of G^{-1}
    from nearest inliers for speed.
    """

    # ------------------------------------------------------------------ #
    # 1) INIT: KDE inliers, KD-tree, boundary cutoff, metric cache
    # ------------------------------------------------------------------ #
    def __init__(
        self,
        X,
        vector_field,
        tps=None,
        sample_size=4000,
        density_percentile=1.0,
        distance_cutoff_factor=4.0,   # tighter default than 10
        random_state=0,
        use_float32=True,
        kde_bw="scott",
        speed_sample_size=4000,
    ):
        """
        Parameters
        ----------
        X : (N,d) array
            Chart coordinates.
        vector_field : object with .predict(array)->(N,d)
            Continuous vector field in chart space.
        tps : object or None
            If provided, must have .compute_metric(points)->(N,d,d).
        sample_size : int
            If N > sample_size, downsample for *model building* (KDE/KD-tree).
            Original full X is kept for evaluation where needed.
        density_percentile : float in [0,100]
            Keep points >= this KDE density percentile as inliers.
        distance_cutoff_factor : float
            Multiplier on average 1-NN distance to define boundary cutoff.
        random_state : int
            RNG seed.
        use_float32 : bool
            Cast large arrays to float32 to reduce memory & speed up math.
        kde_bw : str or float
            Bandwidth for KDE calls.
        speed_sample_size : int
            Subsample size to estimate average speed / dt robustly.
        """
        rng = np.random.default_rng(random_state)
        X = np.asarray(X)
        if use_float32:
            X = X.astype(np.float32, copy=False)
        self.X_full = X  # keep the full data for pseudotime density eval, etc.

        # === Downsample for model building (KDE/KD-tree) ===
        if X.shape[0] > sample_size:
            idx = rng.choice(X.shape[0], sample_size, replace=False)
            self.X = X[idx]
        else:
            self.X = X

        self.vector_field = vector_field
        self.tps = tps
        self.kde_bw = kde_bw
        self.use_float32 = use_float32

        # Metric function
        if tps is None:
            print("No TPS surface provided — using identity metric.")
            def metric(x):
                d = x.shape[-1]
                return np.eye(d, dtype=X.dtype)
        else:
            print("TPS surface provided — using its pullback metric.")
            def metric(x):
                x = np.atleast_2d(x)
                g = tps.compute_metric(x)[0]  # assume single point -> (d,d)
                return g.astype(X.dtype, copy=False)
        self.metric = metric

        # === KDE on (downsampled) X to pick inliers ===
        print("Fitting Gaussian KDE on downsampled X ...")
        self.kde = gaussian_kde(self.X.T, bw_method=self.kde_bw)
        densities = self.kde(self.X.T)
        self.density_threshold = np.percentile(densities, density_percentile)
        inliers_mask = densities >= self.density_threshold
        self.X_inliers = self.X[inliers_mask]
        print(f"Inliers kept: {self.X_inliers.shape[0]} / {self.X.shape[0]} (from full N={X.shape[0]})")

        # === KD-tree on inliers ===
        self.kd_tree = cKDTree(self.X_inliers)

        # === Boundary cutoff from avg 1-NN distance (fast) ===
        nn = NearestNeighbors(n_neighbors=2, n_jobs=-1).fit(self.X_inliers)
        dists = nn.kneighbors(self.X_inliers, return_distance=True)[0][:, 1]
        avg_nn_dist = float(np.mean(dists))
        self.boundary_distance_cutoff = float(distance_cutoff_factor * avg_nn_dist)
        print(f"Boundary cutoff distance: {self.boundary_distance_cutoff:.4f}")

        # === Cache metric noise factors: Cholesky of G^{-1} at inliers ===
        print("Precomputing metric noise factors (Cholesky of G^{-1}) at inliers ...")
        d = self.X.shape[1]
        chol_list = []
        eps = 1e-6
        I = np.eye(d, dtype=X.dtype)
        for xi in self.X_inliers:
            g = self.metric(xi)
            Ginv = np.linalg.inv(g + eps * I)
            L = np.linalg.cholesky(Ginv)  # Ginv = L L^T
            chol_list.append(L)
        self.Ginv_chol_inliers = np.stack(chol_list)  # (M,d,d)

        # Containers
        self.params = None
        self.P = self.P_smooth = self.tau = None
        self.root = self.root_kde = None
        self.reverse_paths = self.all_paths = None
        self.simulation_params = None

        # Store config for dt/sigma estimation
        self._rng = rng
        self._speed_sample_size = speed_sample_size

    # ------------------------------------------------------------------ #
    # 2) PARAM ESTIMATION
    # ------------------------------------------------------------------ #
    def _estimate_stochastic_params(self, step_size_scale=30, randomness_scale=1.0):
        # Estimate average speed on a subsample
        N = self.X.shape[0]
        k = min(self._speed_sample_size, N)
        idx = self._rng.choice(N, k, replace=False)
        V = self.vector_field.predict(self.X[idx])
        avg_speed = float(np.linalg.norm(V, axis=1).mean())

        # Fast diameter via bounding box (avoid O(N^2))
        mins, maxs = self.X.min(0), self.X.max(0)
        max_distance = float(np.linalg.norm(maxs - mins))

        dt = max_distance / (avg_speed * step_size_scale + 1e-8)
        return {
            "step_size_dt": float(dt),
            "randomness_sigma": float(randomness_scale * avg_speed),
        }

    # ------------------------------------------------------------------ #
    # 3) ROOT FINDING (reverse sims -> KDE mode)
    # ------------------------------------------------------------------ #
    def find_root(
        self,
        n_simulations_per_cell=3,
        max_boundary_hits=5,
        max_steps=60,
        step_size_scale=20,
        randomness_scale=0.1,
        min_velocity_threshold=0.01
    ):
        self.params = self._estimate_stochastic_params(step_size_scale, randomness_scale)

        # Repeat inliers
        starts = np.repeat(self.X_inliers, n_simulations_per_cell, axis=0)

        # Backward simulation, no jitter
        self.reverse_paths = self.simulate_path(
            starts,
            reverse=True,
            use_jitter=False,
            time_jitter_steps=0,
            max_boundary_hits=max_boundary_hits,
            max_steps=max_steps,
            min_velocity_threshold=min_velocity_threshold
        )

        finals = [p[-1] for p in self.reverse_paths if len(p) > 0]
        if len(finals) == 0:
            raise ValueError("No valid reverse paths produced any steps—try increasing max_steps or randomness_scale.")

        final_positions = np.asarray(finals)
        self.root_kde = gaussian_kde(final_positions.T, bw_method=self.kde_bw)
        dens = self.root_kde(final_positions.T)
        self.root = final_positions[np.argmax(dens)]

        root_str = ", ".join(f"{c:.4f}" for c in self.root)
        print(f"Automatically identified root: ({root_str})")
        return self.root

    def find_multiple_roots(self, grid_size=100, threshold_rel=0.5):
        if self.root_kde is None:
            raise ValueError("No KDE available. Run find_root() first.")
        if self.X.shape[1] != 2:
            raise ValueError("find_multiple_roots currently supports 2D only.")

        x_min, x_max = self.X_inliers[:, 0].min(), self.X_inliers[:, 0].max()
        y_min, y_max = self.X_inliers[:, 1].min(), self.X_inliers[:, 1].max()
        x_grid = np.linspace(x_min, x_max, grid_size)
        y_grid = np.linspace(y_min, y_max, grid_size)
        xx, yy = np.meshgrid(x_grid, y_grid)
        grid_coords = np.vstack([xx.ravel(), yy.ravel()])

        zz = self.root_kde(grid_coords).reshape(grid_size, grid_size)
        neighborhood = maximum_filter(zz, size=5) == zz
        thr = zz.max() * float(threshold_rel)
        peaks = np.where((zz >= thr) & neighborhood)

        roots = np.stack([x_grid[peaks[1]], y_grid[peaks[0]]], axis=1)
        if roots.size == 0:
            print("No secondary root peaks found at the given threshold. Try lowering threshold_rel.")
            return roots
        print("Found multiple root candidates:")
        for i, r in enumerate(roots):
            print(f"  Root {i+1}: ({r[0]:.4f}, {r[1]:.4f})")
        return roots

    # ------------------------------------------------------------------ #
    # 4) CORE SIMULATOR (vectorized; metric-noise cached)
    # ------------------------------------------------------------------ #
    def simulate_path(
        self,
        starts,
        n_particles=1000,
        start_jitter=0.1,
        time_jitter_steps=5,
        min_velocity_threshold=0.01,
        reverse=False,
        use_jitter=True,
        max_boundary_hits=5,
        max_steps=60,
        step_size_scale=30,
        randomness_scale=0.05,
    ):
        """
        Simulate stochastic trajectories from one or more start points.
        If 'starts' is (d,), launch n_particles with jitter; if (N,d), use them as-is (optionally jittered).
        """
        # Auto-estimate params if missing
        if self.params is None:
            self.params = self._estimate_stochastic_params(step_size_scale, randomness_scale)

        dt    = self.params["step_size_dt"]
        sigma = self.params["randomness_sigma"]
        d     = self.X.shape[1]

        starts = np.asarray(starts, dtype=self.X.dtype)

        # Handle single-root vs array starts
        if starts.ndim == 1:
            if use_jitter:
                # avg distance via a small subsample to avoid O(N^2)
                mins, maxs = self.X.min(0), self.X.max(0)
                avg_span = float(np.mean(maxs - mins))
                jitter_scale = float(start_jitter) * avg_span
                starts = starts[None, :] + jitter_scale * np.random.randn(n_particles, d).astype(self.X.dtype)
            else:
                starts = np.tile(starts[None, :], (n_particles, 1))
        elif starts.ndim == 2:
            n_particles = starts.shape[0]
            if use_jitter:
                mins, maxs = self.X.min(0), self.X.max(0)
                avg_span = float(np.mean(maxs - mins))
                jitter_scale = float(start_jitter) * avg_span
                starts = starts + jitter_scale * np.random.randn(*starts.shape).astype(self.X.dtype)
        else:
            raise ValueError("`starts` must be a 1D point or a 2D array of start points.")

        # Containers
        paths = [[starts[i].copy()] for i in range(n_particles)]
        boundary_hits = np.zeros(n_particles, dtype=np.int16)
        active = np.ones(n_particles, dtype=bool)

        # Vectorized one-step advance using cached metric Cholesky
        def advance(positions):
            V = self.vector_field.predict(positions).astype(self.X.dtype, copy=False) * 3.0
            if reverse:
                V = -V
            # nearest inlier for metric
            _, idx = self.kd_tree.query(positions)
            Ls = self.Ginv_chol_inliers[idx]                       # (n,d,d)
            z  = np.random.randn(*positions.shape).astype(self.X.dtype)
            noise = (sigma * np.sqrt(dt)) * np.einsum('nij,nj->ni', Ls, z)
            return positions + V * dt + noise, V

        # Pseudotime jitter burn-in (masked)
        pos = starts.copy()
        if use_jitter and time_jitter_steps > 0:
            burn = self._rng.integers(0, time_jitter_steps + 1, size=n_particles)
            for t in range(burn.max()):
                mask = burn > t
                if not np.any(mask):
                    break
                pos[mask], _ = advance(pos[mask])
            for i in range(n_particles):
                paths[i][0] = pos[i].copy()

        # Main loop
        for step in range(max_steps):
            if not np.any(active):
                break
            last_pos = np.array([p[-1] for p in paths], dtype=self.X.dtype)
            proposed, V = advance(last_pos)

            dists, _ = self.kd_tree.query(proposed)
            in_bounds = dists < self.boundary_distance_cutoff
            low_vel   = np.linalg.norm(V, axis=1) < float(min_velocity_threshold)

            reject = low_vel | ~in_bounds
            accept = ~reject & active
            boundary_hits += (~low_vel & ~in_bounds & active)
            active &= ~(low_vel | (boundary_hits >= max_boundary_hits))

            accept_idx = np.where(accept)[0]
            for i in accept_idx:
                paths[i].append(proposed[i])

        return paths

    # ------------------------------------------------------------------ #
    # 5) PSEUDOTIME ESTIMATION (KDE over time; slimmer by design)
    # ------------------------------------------------------------------ #
    def compute_pseudotime(
        self,
        roots,
        n_particles_per_root=2000,
        max_steps=60,
        start_jitter=0.15,
        step_size_scale=30,
        randomness_scale=0.6,
        bandwidth='scott',
        pseudotime_smoothing_width=1.0,
        pseudotime_quantile=0.1,
        min_total_mass=1e-6,
        particle_subsample=0,     # 0 -> keep all; >0 to subsample particles for KDE
        keep_every_k_path_step=1, # 1 -> keep all steps; >1 to thin in time
    ):
        """
        Estimate pseudotime by simulating forward from roots, KDE over time,
        and taking a CDF quantile per cell.
        """
        print("=== Estimating stochastic parameters ===")
        self.params = self._estimate_stochastic_params(step_size_scale, randomness_scale)
        self.simulation_params = dict(
            step_size_scale=step_size_scale,
            randomness_scale=randomness_scale,
            max_steps=max_steps,
            n_particles_per_root=n_particles_per_root,
            start_jitter=start_jitter,
            bandwidth=bandwidth,
            pseudotime_smoothing_width=pseudotime_smoothing_width,
            pseudotime_quantile=pseudotime_quantile,
            min_total_mass=min_total_mass,
        )

        if isinstance(roots, np.ndarray) and roots.ndim == 1:
            roots = [roots]

        # Launch particles per root
        print(f"=== Starting simulations from {len(roots)} root(s) ===")
        mins, maxs = self.X.min(0), self.X.max(0)
        avg_span = float(np.mean(maxs - mins))
        jitter_scale = start_jitter * avg_span

        all_paths = []
        for i, root in enumerate(roots):
            root = np.asarray(root, dtype=self.X.dtype)
            print(f"  > Root {i+1}: {root} — launching {n_particles_per_root} particles")
            starts = root[None, :] + jitter_scale * np.random.randn(n_particles_per_root, root.shape[0]).astype(self.X.dtype)
            paths = self.simulate_path(starts, reverse=False, max_steps=max_steps)
            all_paths.extend(paths)

        # Optional: subsample particles for KDE to save time
        if particle_subsample > 0 and len(all_paths) > particle_subsample:
            idx = self._rng.choice(len(all_paths), particle_subsample, replace=False)
            all_paths = [all_paths[i] for i in idx]
            print(f"  > Subsampled particles to {len(all_paths)} for KDE.")

        # Optional: thin time steps
        if keep_every_k_path_step > 1:
            for i in range(len(all_paths)):
                all_paths[i] = all_paths[i][::keep_every_k_path_step]

        self.all_paths = all_paths
        n_steps = max(len(p) for p in all_paths)
        dim = self.X_full.shape[1]
        N_full = self.X_full.shape[0]
        P_full = np.zeros((N_full, n_steps), dtype=np.float32 if self.use_float32 else np.float64)

        print(f"=== Estimating densities and pseudotime for {N_full} total cells ===")
        for t in range(n_steps):
            if t % 10 == 0:
                print(f"  > Time step {t+1}/{n_steps}")
            # Gather particle positions at time t
            pos_t = np.array([p[t] if t < len(p) else np.full(dim, np.nan, dtype=self.X_full.dtype) for p in all_paths])
            valid = ~np.isnan(pos_t).any(axis=1)
            if np.sum(valid) < 10:
                continue
            kde = gaussian_kde(pos_t[valid].T, bw_method=bandwidth)
            P_full[:, t] = kde(self.X_full.T)

        print("=== Smoothing pseudotime matrix ===")
        P_smooth_full = gaussian_filter1d(P_full, sigma=pseudotime_smoothing_width, axis=1)
        total_mass_full = np.sum(P_smooth_full, axis=1)
        mask_full = total_mass_full > float(min_total_mass)

        print("=== Computing CDF and pseudotime quantiles ===")
        tau_full = np.full(P_full.shape[0], np.nan)
        cdf_full = np.cumsum(P_smooth_full[mask_full], axis=1) / (total_mass_full[mask_full, None] + 1e-10)
        tau_full[mask_full] = np.argmax(cdf_full >= float(pseudotime_quantile), axis=1)

        print("=== Done! ===")
        print(f"  Assigned pseudotime to {np.sum(~np.isnan(tau_full))} / {P_full.shape[0]} cells")

        self.P = P_full
        self.P_smooth = P_smooth_full
        self.tau = tau_full
        return tau_full

