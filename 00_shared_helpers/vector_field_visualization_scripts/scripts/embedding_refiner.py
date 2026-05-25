"""
flowmap.embedding_refiner
=========================

Embedding refinement via geometry-aware optimization.

This module provides two refinement strategies:

1. EmbeddingRefiner      : Full-batch L-BFGS optimization
2. EmbeddingSGDRefiner   : Mini-batch stochastic refinement

Both optimize embedding coordinates by minimizing:

    L = ||X - spline(X_emb)||²
        + λ ||V - J_spline(X_emb) · spline_vf(X_emb)||²
        + α ||X_emb - X_emb_init||²

This improves geometric consistency between:

- The manifold reconstruction
- The pushforward of the vector field
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from tqdm import trange


# ======================================================================
# Full-batch refinement (L-BFGS)
# ======================================================================

class EmbeddingRefiner:
    """
    Global embedding refinement using full-batch optimization.

    Parameters
    ----------
    spline : Spline
        Manifold spline mapping embedding → input space.

    spline_vf : Spline
        Velocity spline mapping embedding → embedded velocity.

    X : ndarray (N, p)
        Input-space coordinates.

    V : ndarray (N, p)
        Input-space vector field.

    X_emb : ndarray (N, d)
        Initial embedding.

    lam : float
        Weight for velocity reconstruction term.

    alpha : float, default=0
        Anchor regularization weight.
    """

    def __init__(self, spline, spline_vf, X, V, X_emb, lam, alpha=0.0):
        self.spline = spline
        self.spline_vf = spline_vf

        self.X = X
        self.V = V
        self.X_emb = X_emb
        self.X_init = X_emb.copy()

        self.lam = lam if lam is not None else self._estimate_lambda()
        self.alpha = alpha

        self._loss_cache = None
        self._grad_cache = None


    # ------------------------------------------------------------------
    # Lambda estimation
    # ------------------------------------------------------------------

    def _estimate_lambda(self, batch_size=100, ratio=10.0):
        idx = np.random.choice(len(self.X), size=min(batch_size, len(self.X)), replace=False)

        X_batch = self.X[idx]
        V_batch = self.V[idx]
        X_emb_batch = self.X_emb[idx]

        X_pred = self.spline.predict(X_emb_batch)
        loss1 = np.sum((X_batch - X_pred) ** 2)

        vf_pred = self.spline_vf.predict(X_emb_batch)
        J = self.spline.compute_jacobians(X_emb_batch)
        V_pred = np.einsum("naj,nj->na", J, vf_pred)
        loss2 = np.sum((V_batch - V_pred) ** 2)

        if loss2 < 1e-6:
            return 1.0

        return np.clip((loss1 / loss2) * ratio, 1e-3, 1e3)


    # ------------------------------------------------------------------
    # Loss + gradient
    # ------------------------------------------------------------------

    def _loss_and_grad(self, X_flat):
        X_emb = X_flat.reshape(self.X_emb.shape)

        # --- manifold reconstruction ---
        X_pred = self.spline.predict(X_emb)
        J = self.spline.compute_jacobians(X_emb)
        H = self.spline.compute_hessians(X_emb)

        loss1 = np.sum((self.X - X_pred) ** 2)

        # --- velocity reconstruction ---
        vf_pred = self.spline_vf.predict(X_emb)
        V_pred = np.einsum("naj,nj->na", J, vf_pred)
        loss2 = np.sum((self.V - V_pred) ** 2)

        # --- anchor ---
        anchor_diff = X_emb - self.X_init
        anchor_loss = np.sum(anchor_diff ** 2)

        # --- gradients ---
        grad1 = -2 * np.einsum("nai,na->ni", J, (self.X - X_pred))

        A = -2 * (self.V - V_pred)
        B = np.einsum("naij,nj->nai", H, vf_pred)
        C = np.einsum("naj,nji->nai", J, self.spline_vf.compute_jacobians(X_emb))
        grad2 = np.einsum("na,nai->ni", A, (B + C))

        grad_anchor = 2 * anchor_diff

        total_loss = loss1 + self.lam * loss2 + self.alpha * anchor_loss
        total_grad = grad1 + self.lam * grad2 + self.alpha * grad_anchor

        return total_loss, total_grad.flatten()


    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def refine_embedding(self, method="L-BFGS-B", tol=1e-4, verbose=False):
        """
        Run global embedding optimization.

        Returns
        -------
        X_optimized : ndarray (N, d)
        result : OptimizeResult
        """
        X_flat = self.X_emb.flatten()

        result = minimize(
            fun=lambda x: self._loss_and_grad(x)[0],
            x0=X_flat,
            jac=lambda x: self._loss_and_grad(x)[1],
            method=method,
            tol=tol,
            options={"gtol": tol, "ftol": tol, "disp": verbose},
        )

        return result.x.reshape(self.X_emb.shape), result


# ======================================================================
# Mini-batch SGD refinement
# ======================================================================

class EmbeddingSGDRefiner:
    """
    Stochastic embedding refinement using mini-batch gradient descent.
    """

    def __init__(self, spline, spline_vf, X, V, X_emb, lam):
        self.spline = spline
        self.spline_vf = spline_vf
        self.X = X
        self.V = V
        self.X_emb = X_emb

        self.lam = lam if lam is not None else 1.0


    def _batch_loss_grad(self, X_flat, batch_idx, alpha=1.0):
        X_emb = X_flat.reshape(self.X_emb.shape)

        X_batch = X_emb[batch_idx]
        X_ref = self.X[batch_idx]
        V_ref = self.V[batch_idx]
        X_init = self.X_emb[batch_idx]

        X_pred = self.spline.predict(X_batch)
        J = self.spline.compute_jacobians(X_batch)
        H = self.spline.compute_hessians(X_batch)

        loss1 = np.sum((X_ref - X_pred) ** 2)

        vf_pred = self.spline_vf.predict(X_batch)
        V_pred = np.einsum("naj,nj->na", J, vf_pred)
        loss2 = np.sum((V_ref - V_pred) ** 2)

        anchor_loss = np.sum((X_batch - X_init) ** 2)

        grad1 = -2 * np.einsum("nai,na->ni", J, (X_ref - X_pred))

        A = -2 * (V_ref - V_pred)
        B = np.einsum("naij,nj->nai", H, vf_pred)
        C = np.einsum("naj,nji->nai", J, self.spline_vf.compute_jacobians(X_batch))
        grad2 = np.einsum("na,nai->ni", A, (B + C))

        grad_anchor = 2 * (X_batch - X_init)

        total_loss = loss1 + self.lam * loss2 + alpha * anchor_loss

        total_grad = np.zeros_like(X_emb)
        total_grad[batch_idx] = grad1 + self.lam * grad2 + alpha * grad_anchor

        return total_loss, total_grad.flatten()


    def refine_embedding(self, epochs=50, batch_size=64, lr=1e-2, seed=1, verbose=False):
        """
        Run mini-batch refinement.

        Returns
        -------
        X_optimized : ndarray (N, d)
        """
        rng = np.random.default_rng(seed)

        X_flat = self.X_emb.flatten()
        N = self.X_emb.shape[0]
        indices = np.arange(N)

        for _ in trange(epochs, desc="Embedding refinement"):
            rng.shuffle(indices)

            for i in range(0, N, batch_size):
                batch_idx = indices[i:i + batch_size]
                _, grad = self._batch_loss_grad(X_flat, batch_idx)
                X_flat -= lr * np.nan_to_num(grad)

        return X_flat.reshape(self.X_emb.shape)
        