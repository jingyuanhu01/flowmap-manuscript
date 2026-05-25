# flowmap/evaluation/spline_fit_evaluator.py

from __future__ import annotations
import numpy as np
from sklearn.cluster import KMeans
from typing import Optional, Dict


class SplineFitEvaluator:
    """
    Evaluate reconstruction accuracy of manifold and velocity splines.

    This class quantifies how well a fitted spline model reconstructs:

        1. Feature values (e.g. genes or principal components)
        2. Vector field values

    It supports evaluation at two levels:

        - Gene-level splines (``spline_gene``, ``spline_vf_gene``)
        - Embedding-level splines (``spline``, ``spline_vf``)

    If ``mode`` is not specified, gene-level splines are used when
    available; otherwise embedding-level splines are evaluated.

    Notes
    -----
    Let :math:`f(z)` denote the spline mapping from embedding
    coordinates :math:`z` to feature space, and let
    :math:`J(z) = \\nabla f(z)` denote its Jacobian.

    Expression reconstruction is evaluated via:

    .. math::

        R^2 = 1 - \\frac{\\|X - \\hat{X}\\|^2}{\\|X - \\bar{X}\\|^2}

    Velocity reconstruction is evaluated using the local linear
    pushforward:

    .. math::

        \\hat{V} = J(z) \\beta,

    where :math:`\\beta` is obtained by least-squares fitting to
    the observed velocity.

    This provides both global and per-feature metrics.
    """

    def __init__(
        self,
        emb,
        *,
        mode: Optional[str] = None,
        cell_idx: Optional[np.ndarray] = None,
    ):
        """
        Initialize spline reconstruction evaluator.

        Parameters
        ----------
        emb : VectorFieldEmbedder
            Fitted embedding object containing:

            - ``X_emb``        : embedding coordinates
            - ``V_emb``        : embedded vector field
            - ``spline``       : manifold spline
            - ``spline_vf``    : velocity spline

            Optionally:

            - ``spline_gene``  : gene-level spline
            - ``spline_vf_gene`` : gene-level velocity spline

        mode : {"gene", "pc"}, optional
            Evaluation mode:

            - "gene" → evaluate gene-level splines.
            - "pc"   → evaluate embedding-level splines.
            - None   → automatically select gene-level if available.

        cell_idx : ndarray, optional
            Indices of cells to include in evaluation.
            If None, all cells are used.

        Raises
        ------
        ValueError
            If an invalid mode is provided.
        RuntimeError
            If gene mode is requested but gene splines are unavailable.
        """

        self.emb = emb

        # --------------------------------------------------------------
        # Select evaluation mode
        # --------------------------------------------------------------

        if mode is None:
            if hasattr(emb, "spline_gene"):
                mode = "gene"
            else:
                mode = "pc"

        if mode not in {"gene", "pc"}:
            raise ValueError("mode must be 'gene' or 'pc'.")

        self.mode = mode

        # --------------------------------------------------------------
        # Select splines and data
        # --------------------------------------------------------------

        if mode == "gene":
            if not hasattr(emb, "spline_gene"):
                raise RuntimeError("Gene-level splines not fitted.")
            self.spline = emb.spline_gene
            self.spline_vf = emb.spline_vf_gene
            self.X_ref = emb.X_gene
            self.V_ref = emb.V_gene
        else:
            self.spline = emb.spline
            self.spline_vf = emb.spline_vf
            self.X_ref = emb.X
            self.V_ref = emb.V

        # --------------------------------------------------------------
        # Cell selection
        # --------------------------------------------------------------

        n = emb.X_emb.shape[0]
        self.cell_idx = np.arange(n) if cell_idx is None else np.asarray(cell_idx)

        self.X_emb = emb.X_emb[self.cell_idx]
        self.V_emb = emb.V_emb[self.cell_idx]
        self.X_ref = self.X_ref[self.cell_idx]
        self.V_ref = self.V_ref[self.cell_idx]

        # --------------------------------------------------------------
        # Precompute predictions and Jacobians
        # --------------------------------------------------------------

        self.X_pred = self.spline.predict(self.X_emb)
        self.J = self.spline.compute_jacobians(self.X_emb)


    def evaluate(self) -> Dict:
        """
        Compute reconstruction metrics.

        Returns
        -------
        dict
            Dictionary containing:

            expr_r2 : float
                Mean expression R² across features.

            vel_r2 : float
                Mean velocity R² across features.

            expr_r2_gene : list of float
                Per-feature expression R² values.

            vel_r2_gene : list of float
                Per-feature velocity R² values.

            expr_corr_gene : list of float
                Per-feature Pearson correlation (expression).

            vel_corr_gene : list of float
                Per-feature Pearson correlation (velocity).

            X_pred : ndarray
                Reconstructed feature values.

            V_pred : ndarray
                Reconstructed velocity values.

        Notes
        -----
        Expression reconstruction evaluates the spline prediction:

        .. math::

            \\hat{X} = f(z)

        Velocity reconstruction evaluates the local linear pushforward:

        .. math::

            \\hat{V} = J(z) \\beta

        where :math:`\\beta` is obtained via least-squares fit at
        each cell independently.
        """

        X_obs, V_obs = self.X_ref, self.V_ref
        X_pred, J = self.X_pred, self.J

        N, G = X_obs.shape

        # --- reconstruct velocity via Jacobian pushforward ---
        V_pred = np.zeros_like(V_obs)

        for i in range(N):
            beta, *_ = np.linalg.lstsq(J[i], V_obs[i], rcond=None)
            V_pred[i] = J[i] @ beta

        # --- R² computation ---
        def r2(A, B):
            SSE = np.sum((A - B) ** 2, axis=0)
            TSS = np.sum((A - A.mean(axis=0)) ** 2, axis=0) + 1e-12
            return 1.0 - SSE / TSS

        expr_r2_gene = r2(X_obs, X_pred)
        vel_r2_gene = r2(V_obs, V_pred)

        expr_r2 = float(np.mean(expr_r2_gene))
        vel_r2 = float(np.mean(vel_r2_gene))

        # --- correlations ---
        def corr_per_feature(A, B):
            out = []
            for i in range(A.shape[1]):
                if np.std(A[:, i]) > 1e-12 and np.std(B[:, i]) > 1e-12:
                    out.append(float(np.corrcoef(A[:, i], B[:, i])[0, 1]))
                else:
                    out.append(np.nan)
            return np.array(out)

        expr_corr = corr_per_feature(X_obs, X_pred)
        vel_corr = corr_per_feature(V_obs, V_pred)

        return dict(
            expr_r2=expr_r2,
            vel_r2=vel_r2,
            expr_r2_gene=expr_r2_gene.tolist(),
            vel_r2_gene=vel_r2_gene.tolist(),
            expr_corr_gene=expr_corr.tolist(),
            vel_corr_gene=vel_corr.tolist(),
            X_pred=X_pred,
            V_pred=V_pred,
        )


    def evaluate(self) -> Dict:
        """
        Compute reconstruction metrics.

        Returns
        -------
        dict
            Dictionary containing:

            expr_r2 : float
                Mean expression R² across features.

            vel_r2 : float
                Mean velocity R² across features.

            expr_r2_gene : list of float
                Per-feature expression R² values.

            vel_r2_gene : list of float
                Per-feature velocity R² values.

            expr_corr_gene : list of float
                Per-feature Pearson correlation (expression).

            vel_corr_gene : list of float
                Per-feature Pearson correlation (velocity).

            X_pred : ndarray
                Reconstructed feature values.

            V_pred : ndarray
                Reconstructed velocity values.

        Notes
        -----
        Expression reconstruction evaluates the spline prediction:

        .. math::

            \\hat{X} = f(z)

        Velocity reconstruction evaluates the local linear pushforward:

        .. math::

            \\hat{V} = J(z) \\beta

        where :math:`\\beta` is obtained via least-squares fit at
        each cell independently.
        """

        rng = np.random.default_rng(random_state)

        X_obs = self.X_ref
        V_obs = self.V_ref
        X_pred = res["X_pred"]
        V_pred = res["V_pred"]

        N, G = X_obs.shape

        R2_expr_obs = np.array(res["expr_r2_gene"])
        R2_vel_obs = np.array(res["vel_r2_gene"])

        bins = KMeans(
            n_clusters=min(n_bins, max(2, int(np.sqrt(N)))),
            n_init=5,
            random_state=random_state,
        ).fit_predict(self.X_emb)

        ge_expr = np.zeros(G)
        ge_vel = np.zeros(G)

        for _ in range(n_perm):
            perm_idx = np.arange(N)
            for b in np.unique(bins):
                idx = np.where(bins == b)[0]
                perm_idx[idx] = rng.permutation(idx)

            X_perm = X_obs[perm_idx]
            V_perm = V_obs[perm_idx]

            expr_null = 1 - np.sum((X_perm - X_pred)**2, axis=0) / (
                np.sum((X_perm - X_perm.mean(axis=0))**2, axis=0) + 1e-12
            )
            vel_null = 1 - np.sum((V_perm - V_pred)**2, axis=0) / (
                np.sum((V_perm - V_perm.mean(axis=0))**2, axis=0) + 1e-12
            )

            ge_expr += (expr_null >= R2_expr_obs)
            ge_vel += (vel_null >= R2_vel_obs)

        p_expr = (ge_expr + 1) / (n_perm + 1)
        p_vel = (ge_vel + 1) / (n_perm + 1)

        return dict(
            expr_p=p_expr.tolist(),
            vel_p=p_vel.tolist(),
            n_perm=n_perm,
        )
        