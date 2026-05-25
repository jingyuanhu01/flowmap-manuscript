# flowmap/geometry/gene_gradient_analyzer.py

from __future__ import annotations
import numpy as np
from typing import Optional, Dict


class GeneGradientAnalyzer:
    """
    Analyze gene-expression gradients relative to the local velocity field.

    This class evaluates how gene-level gradients align with
    the embedded vector field along a specified trajectory
    or neighborhood.

    It uses the pullback metric and spline Jacobians to compute:

        - Parallel gradient component
        - Orthogonal gradient component
        - Relative orientation angle
        - Gradient magnitude

    Notes
    -----
    Let f(z) denote the spline mapping from embedding coordinates
    to gene-expression space, with Jacobian J(z).

    The gene gradient in embedding coordinates is:

        ∇_z g = g^{-1} J

    where g is the pullback Riemannian metric.

    Gradients are decomposed relative to the unit velocity direction.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        emb,
        *,
        mode: str = "gene",
    ):
        """
        Parameters
        ----------
        emb : VectorFieldEmbedder
            Embedding object containing fitted splines.

        mode : {"gene", "pc"}, default="gene"
            Level of gradient analysis.

            - "gene": use gene-level spline.
            - "pc":   use embedding-level spline.

        Raises
        ------
        RuntimeError
            If required splines are not fitted.
        """

        self.emb = emb

        if mode == "gene":
            if not hasattr(emb, "spline_gene"):
                raise RuntimeError("Gene-level splines not fitted.")
            self.spline = emb.spline_gene
        elif mode == "pc":
            self.spline = emb.spline
        else:
            raise ValueError("mode must be 'gene' or 'pc'.")

        self.mode = mode

        # Precompute Jacobians and metric tensors
        self.J_all = self.spline.compute_jacobians(emb.X_emb)
        self.metric = self.spline.compute_metric(emb.X_emb)

        self.X_emb = emb.X_emb
        self.V_emb = emb.V_emb


    # ------------------------------------------------------------------
    # Neighborhood selection
    # ------------------------------------------------------------------

    def find_neighbors(
        self,
        trajectory: np.ndarray,
        epsilon: float = 0.05,
    ) -> np.ndarray:
        """
        Select cells near a trajectory.

        Parameters
        ----------
        trajectory : ndarray (m, d)
            Path in embedding space.
        epsilon : float
            Relative radius (fraction of embedding diameter).

        Returns
        -------
        ndarray
            Indices of neighboring cells.
        """

        scale = np.mean(np.ptp(self.X_emb, axis=0))
        radius = epsilon * scale

        dists = np.linalg.norm(
            self.X_emb[:, None, :] - trajectory[None, :, :],
            axis=2,
        ).min(axis=1)

        return np.where(dists <= radius)[0]


    # ------------------------------------------------------------------
    # Gradient decomposition
    # ------------------------------------------------------------------

    def compute_relative_orientations(
        self,
        cell_idx: np.ndarray,
        feature_idx: Optional[np.ndarray] = None,
        *,
        weight: str = "magnitude",
    ) -> Dict[str, np.ndarray]:
        """
        Compute gradient orientation relative to velocity field.

        Parameters
        ----------
        cell_idx : ndarray
            Cell indices defining neighborhood.
        feature_idx : ndarray, optional
            Subset of genes/features to evaluate.
        weight : {"magnitude", "uniform"}
            Weighting scheme for averaging across cells.

        Returns
        -------
        dict
            Contains:

            - angles      : ndarray (n_features,)
            - magnitudes  : ndarray (n_features,)
        """

        if feature_idx is None:
            feature_idx = np.arange(self.J_all.shape[1])

        angles = []
        magnitudes = []

        for g_idx in feature_idx:

            vec_sum = np.zeros(2)
            total_w = 0.0

            for c in cell_idx:

                g = self.metric[c]
                J = self.J_all[c, g_idx]
                v = self.V_emb[c]

                # Raise index via metric inverse
                grad = np.linalg.solve(g + 1e-8 * np.eye(g.shape[0]), J)

                # Local Euclideanization
                L = np.linalg.cholesky(g + 1e-8 * np.eye(g.shape[0]))
                grad_E = L @ grad
                v_E = L @ v

                v_norm = np.linalg.norm(v_E)
                if v_norm < 1e-8:
                    continue

                e1 = v_E / v_norm
                e2 = np.array([-e1[1], e1[0]])

                parallel = grad_E @ e1
                orth = grad_E @ e2

                w = np.linalg.norm(grad_E) if weight == "magnitude" else 1.0

                vec_sum += w * np.array([parallel, orth])
                total_w += w

            if total_w > 0:
                mean_vec = vec_sum / total_w
                angles.append(np.arctan2(mean_vec[1], mean_vec[0]))
                magnitudes.append(np.linalg.norm(mean_vec))
            else:
                angles.append(np.nan)
                magnitudes.append(np.nan)

        return dict(
            angles=np.array(angles),
            magnitudes=np.array(magnitudes),
        )
        