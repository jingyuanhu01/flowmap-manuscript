from __future__ import annotations

import random
import warnings
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
import umap.umap_ as umap

from scripts.phase_distance_solver import PhaseDistanceGraphSolver
from scripts.TPS import ThinPlateSpline
from scripts.embedding_refiner import EmbeddingSGDRefiner, EmbeddingRefiner

# Silence warnings
warnings.simplefilter("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=UserWarning)


class VectorFieldEmbedder:
    def __init__(
        self,
        X,
        V,
        *,
        method="umap",
        embedding_dim=2,
        dof=30,
        dof_vf=None,
        dof_vf_pca=None,
        dist_method="phase",
        custom_dist=None,
        X_emb=None,
        dist_kwargs=None,
        embed_kwargs=None,
        tps_kwargs=None,
        tps_vf_kwargs=None,
        knn_k=30,
        alpha=0.5,             
        use_PCA=True,
        pca_components=30,
        max_tps_points=4000
    ):
        self.X_raw = X.copy()
        self.V_raw = V.copy()

        self.X, self.V = X, V
        self.max_tps_points = max_tps_points
        self.knn_k = knn_k
        self.alpha = alpha      # <-- Save it
        self.embedding_dim = embedding_dim
        
        self.dof = dof
        self.dof_vf = dof if dof_vf is None else dof_vf
        self.dof_vf_pca = dof if dof_vf_pca is None else dof_vf_pca
        self.method = method.lower()
        self.dist_method = dist_method.lower()
        self.custom_dist = custom_dist

        self.embed_kwargs = embed_kwargs or {}
        self.dist_kwargs = dist_kwargs or {}
        self.tps_kwargs = tps_kwargs or {}
        self.tps_vf_kwargs = tps_vf_kwargs or {}

        self.tps = None
        self.tps_vf = None

        if use_PCA and X.shape[1] > 50:
            self.use_PCA = True
            print(f"[PCA] Applying PCA (input dim = {X.shape[1]}) …")
            self._project_with_pca(n_components=pca_components)
        else:
            self.use_PCA = False
            print(f"[PCA] Skipped (input dim = {X.shape[1]})")
        self.X_emb = X_emb

    # ------------------------------------------- dimensionality reduction
    def _project_with_pca(self, *, n_components=30, pca_smoothing=False):
        print(f"[PCA] TruncatedSVD → {n_components} components …")
        svd = TruncatedSVD(n_components=n_components, random_state=0)
        self.X = svd.fit_transform(self.X)
        self.V = self.V @ svd.components_.T
        self.PCA_component = svd.components_

        self._pca = svd
        if pca_smoothing:
            print("[PCA] TPS‑smoothing vector field …")
            tps_tmp = ThinPlateSpline(self.X, **self.tps_vf_kwargs)
            tps_tmp.fit(self.V, dof=self.dof_vf_pca)
            self.V = tps_tmp.predict(self.X)

    # ------------------------------------------------ distance utilities
    def _compute_distance_graph(self):
        if self.custom_dist is not None:
            return self.custom_dist
        if self.dist_method == "phase":
            solver = PhaseDistanceGraphSolver(
                self.X, self.V,
                k=self.knn_k,
                alpha=self.alpha,    # <-- Pass alpha here
                **self.dist_kwargs
            )
            return solver.compute_graph()
        return None   # euclidean doesn't need graph

    # ------------------------------------------------ initial embedding
    def initialize_embedding(self, seed=None):
        if self.X_emb is None:
            np.random.seed(seed)
            random.seed(seed)

            embed_dim = getattr(self, "embedding_dim", self.embed_kwargs.get("n_components", 2))
            print(f"[Init] Target embedding dimension: {embed_dim}D")

            if self.dist_method == "phase":
                print("[Init] Computing phase distance graph …")
                self.dist_graph = self._compute_distance_graph()

                print(f"[Init] Embedding with {self.method.upper()} (precomputed) …")
                if self.method == "umap":
                    reducer = umap.UMAP(metric="precomputed", random_state=seed, **self.embed_kwargs)
                elif self.method == "tsne":
                    reducer = TSNE(metric="precomputed", init="random", random_state=seed, **self.embed_kwargs)
                else:
                    raise ValueError(f"Unsupported embedding method: {self.method}")

                self.X_emb = reducer.fit_transform(self.dist_graph)

            elif self.dist_method == "euclidean":
                # >>> new PCA-aware branch here <<<
                print(f"[Init] Embedding with {self.method.upper()} …")

                if self.method == "umap":
                    reducer = umap.UMAP(metric="euclidean",
                                        n_components=embed_dim,
                                        random_state=seed,
                                        **self.embed_kwargs)
                    self.X_emb = reducer.fit_transform(self.X)

                elif self.method == "tsne":
                    reducer = TSNE(metric="euclidean",
                                   n_components=embed_dim,
                                   init="random",
                                   random_state=seed,
                                   **self.embed_kwargs)
                    self.X_emb = reducer.fit_transform(self.X)

                elif self.method == "pca":
                    print(f"[Init][PCA] Applying linear PCA to {embed_dim} components …")
                    svd = TruncatedSVD(n_components=embed_dim, random_state=seed)
                    self.X_emb = svd.fit_transform(self.X)
                    self._pca_emb = svd

                else:
                    raise ValueError(f"Unsupported embedding method: {self.method}")

            else:
                raise ValueError(f"Unknown distance method: {self.dist_method}")

            self.X_emb_init = self.X_emb.copy()

        # ---- Subsample points for TPS fitting ----
        np.random.seed(seed)
        n_points = min(self.max_tps_points, self.X.shape[0])
        self.tps_idx = np.random.choice(self.X.shape[0], n_points, replace=False) if n_points < self.X.shape[0] else np.arange(self.X.shape[0])

        self._fit_splines(self.X_emb[self.tps_idx], idx=self.tps_idx)
        print("[Init] Done.")



    
    def regenerate_embedding(self, seed=None, embed_kwargs=None):
        """
        Re-run the embedding (UMAP/TSNE) with a new seed using the same distance graph
        or X (if using Euclidean). Re-fits TPS using the same subsampling logic.
        """
        # If distance graph doesn't exist, compute it
        if not hasattr(self, "dist_graph") and self.dist_method == "phase":
            print("[Regen] No distance graph found — recomputing …")
            self.dist_graph = self._compute_distance_graph()

        np.random.seed(seed)
        random.seed(seed)
        print(f"[Regen] Regenerating embedding with {self.method.upper()} …")

        # Reuse embed kwargs if none are provided
        embed_kwargs = embed_kwargs or self.embed_kwargs

        # Re-embed based on distance method
        if self.dist_method == "phase":
            if self.method == "umap":
                default = dict(metric="precomputed", random_state=seed)
                reducer = umap.UMAP(**{**default, **embed_kwargs})
            elif self.method == "tsne":
                default = dict(metric="precomputed", init="random", random_state=seed)
                reducer = TSNE(**{**default, **embed_kwargs})
            else:
                raise ValueError(f"Unsupported embedding method: {self.method}")

            self.X_emb = reducer.fit_transform(self.dist_graph)

        elif self.dist_method == "euclidean":
            if self.method == "umap":
                default = dict(metric="euclidean", random_state=seed)
                reducer = umap.UMAP(**{**default, **embed_kwargs})
            elif self.method == "tsne":
                default = dict(metric="euclidean", init="random", random_state=seed)
                reducer = TSNE(**{**default, **embed_kwargs})
            else:
                raise ValueError(f"Unsupported embedding method: {self.method}")

            self.X_emb = reducer.fit_transform(self.X)

        else:
            raise ValueError(f"Unknown distance method: {self.dist_method}")

        # Update initial embedding
        self.X_emb_init = self.X_emb.copy()

        # Re-fit TPS on subsampled points
        n_points = min(self.max_tps_points, self.X.shape[0])
        self.tps_idx = np.random.choice(self.X.shape[0], n_points, replace=False)
        self._fit_splines(self.X_emb[self.tps_idx], idx=self.tps_idx)
    
    
    # ----------------------------------- unified spline helper
    def _fit_splines(self, embedding, idx=None):
        X_sub = self.X if idx is None else self.X[idx]
        V_sub = self.V if idx is None else self.V[idx]

        print("[TPS] Fitting geometry spline …")
        self.tps = ThinPlateSpline(embedding, **self.tps_kwargs)
        self.tps.fit(X_sub, dof=self.dof)

        print("[TPS] Mapping vector field …")
        vec_field = self.tps.map_velocities(V_sub)

        print("[TPS] Fitting vector-field spline …")
        self.tps_vf = ThinPlateSpline(embedding, **self.tps_vf_kwargs)
        self.tps_vf.fit(vec_field, dof=self.dof_vf)

        self.V_emb_init = self.tps_vf.predict(self.X_emb)
        self.V_emb = self.V_emb_init.copy()
    
    
    def fit_gene_level_splines(self, dof_gene=30, dof_vf_gene=30, X=None, V=None):
        assert self.X_emb is not None, "Run `initialize_embedding()` first."

        # --- Case 1: custom X and V ---
        if X is not None and V is not None:
            # Save full inputs
            self.X_gene, self.V_gene = X, V

            # Use TPS index if available
            idx = getattr(self, "tps_idx", None)
            if idx is not None:
                X_sub, V_sub, X_emb_sub = X[idx], V[idx], self.X_emb[idx]
            else:
                X_sub, V_sub, X_emb_sub = X, V, self.X_emb

            print(f"[TPS-Gene] Fitting expression spline on {X_sub.shape[0]} cells …")
            self.tps_gene = ThinPlateSpline(X_emb_sub, **self.tps_kwargs)
            self.tps_gene.fit(X_sub, dof=dof_gene)

            print("[TPS-Gene] Mapping velocities …")
            vec_field_gene = self.tps_gene.map_velocities(V_sub)

            print(f"[TPS-Gene] Fitting velocity spline on {V_sub.shape[0]} cells …")
            self.tps_vf_gene = ThinPlateSpline(X_emb_sub, **self.tps_vf_kwargs)
            self.tps_vf_gene.fit(vec_field_gene, dof=dof_vf_gene)

        # --- Case 2: default path, PCA used ---
        elif getattr(self, "use_PCA", False):
            # Save full raw matrices
            self.X_gene, self.V_gene = self.X_raw, self.V_raw

            # Use TPS index if available
            idx = getattr(self, "tps_idx", None)
            if idx is not None:
                X_sub, V_sub, X_emb_sub = self.X_raw[idx], self.V_raw[idx], self.X_emb[idx]
            else:
                X_sub, V_sub, X_emb_sub = self.X_raw, self.V_raw, self.X_emb

            print(f"[TPS-Gene] Fitting expression spline on {X_sub.shape[0]} cells …")
            self.tps_gene = ThinPlateSpline(X_emb_sub, **self.tps_kwargs)
            self.tps_gene.fit(X_sub, dof=dof_gene)

            print("[TPS-Gene] Mapping velocities …")
            vec_field_gene = self.tps_gene.map_velocities(V_sub)

            print(f"[TPS-Gene] Fitting velocity spline on {V_sub.shape[0]} cells …")
            self.tps_vf_gene = ThinPlateSpline(X_emb_sub, **self.tps_vf_kwargs)
            self.tps_vf_gene.fit(vec_field_gene, dof=dof_vf_gene)

        # --- Case 3: no PCA, no refit ---
        else:
            print("[TPS-Gene] Skipping fit. Copying existing splines …")
            self.tps_gene = self.tps
            self.tps_vf_gene = self.tps_vf
            self.X_gene = self.X
            self.V_gene = self.V

        print(f"[TPS-Gene] Done. Saved X_gene {self.X_gene.shape}, V_gene {self.V_gene.shape}")
        

    # ---------------------------------------------------- optimization
    def optimize(self, lam=None, method="batch", batch_size=64, lr=1e-3, epochs=50, tol=1e-2, verbose=False, optimise_viz=False):
        if self.tps is None or self.tps_vf is None:
            self._fit_splines(self.X_emb)

        if method == "batch":
            refiner = EmbeddingSGDRefiner(self.tps, self.tps_vf, self.X, self.V, self.X_emb, lam)
            self.X_emb = refiner.refine_embedding(epochs=epochs, batch_size=batch_size, lr=lr, verbose=verbose)
        elif method == "global":
            refiner = EmbeddingRefiner(self.tps, self.tps_vf, self.X, self.V, self.X_emb, lam)
            self.X_emb, self.opt_result = refiner.refine_embedding(tol=tol, verbose=verbose)
        else:
            raise ValueError(f"Unknown optimisation method: {method}")

        self.refiner = refiner
        print("[Opt] Re‑fitting unified splines …")
        self._fit_splines(self.X_emb)

        if optimise_viz:
            self._fit_splines(self.X_emb)

