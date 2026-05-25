import numpy as np
from numpy.linalg import lstsq, eigvals, norm as l2norm
from scipy.spatial import cKDTree, ConvexHull
from scipy.stats   import norm as normal
from sklearn.neighbors import NearestNeighbors


# ---------------------------------------------------------------------
# 0.  Grid builder  (unchanged – included for completeness)
# ---------------------------------------------------------------------
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



# ---------------------------------------------------------------------
# 1.  Fixed-point finder  (pure grid + threshold + merge)
# ---------------------------------------------------------------------
def find_fixed_points_grid(
    tps_vf,
    X_emb,
    grid_size=100,
    tol_vec_percent=0.01,
    tol_merge_percent=0.1
):
    """
    Detect candidate fixed points on a grid using DBSCAN to merge.

    tol_vec_percent   : threshold ‖v‖ percentile (e.g. 0.01 for bottom 1%)
    tol_merge_percent : distance threshold as % of embedding diameter
    """
    # --- call grid builder correctly ---
    Xg, keep, Vg = compute_velocity_on_grid(
        X_emb,
        tps_vf=tps_vf,
        grid_size=grid_size,
        grid_density=1.0,
        min_mass=0.01,
        return_mesh=False
    )

    if Vg is None or len(Vg) == 0:
        raise ValueError("No valid grid velocities returned.")

    # --- compute norms ---
    vnorm_data = np.linalg.norm(tps_vf.predict(X_emb), axis=1)
    vnorm = np.linalg.norm(Vg, axis=1)

    # --- threshold for near-zero velocity (fixed points) ---
    tol_vec = np.percentile(vnorm_data, tol_vec_percent * 100)
    mask = vnorm < tol_vec
    cands = Xg[mask]
    vnorm = vnorm[mask]

    if cands.size == 0:
        return np.empty((0, X_emb.shape[1]))

    # --- merge close candidates ---
    from sklearn.cluster import DBSCAN
    emb_diameter = np.max(X_emb, axis=0) - np.min(X_emb, axis=0)
    tol_merge = tol_merge_percent * np.linalg.norm(emb_diameter)

    db = DBSCAN(eps=tol_merge, min_samples=1).fit(cands)

    keep_idx = []
    for label in set(db.labels_):
        group_idx = np.where(db.labels_ == label)[0]
        best = group_idx[np.argmin(vnorm[group_idx])]
        keep_idx.append(best)

    return cands[np.array(keep_idx)]



# ---------------------------------------------------------------------
# 2.  Jacobian from grid data  (local linear regression)
# ---------------------------------------------------------------------
def jacobian_from_data(tps_vf, fp, X_2d, V,
                       radius_percent=0.2,
                       weighted=True):
    """
    Fit J such that   V ≈ J·(x - fp)  using actual data points.

    radius_percent : relative to average dimension of embedding
    Returns J  (d×d)  or raises ValueError if too few neighbours.
    """
    emb_range = np.ptp(X_2d, axis=0)
    radius    = radius_percent * np.mean(emb_range)

    diffs = X_2d - fp
    mask  = np.linalg.norm(diffs, axis=1) < radius
    Xloc  = diffs[mask]
    Vloc  = V[mask]

    if Xloc.shape[0] < Xloc.shape[1] * 3:
        raise ValueError("Neighbourhood too small for reliable fit.")

    if weighted:
        w   = np.exp(-np.sum(Xloc**2, axis=1) / (2*(radius*0.5)**2))[:, None]
        Xw  = Xloc * w
        Vw  = Vloc * w
    else:
        Xw, Vw = Xloc, Vloc

    J, *_ = lstsq(Xw, Vw, rcond=None)
    return J


# ---------------------------------------------------------------------
# 3.  Fixed-point classifier  (eigen-spectrum)
# ---------------------------------------------------------------------
def classify_fixed_point(J, eps=1e-4):
    eigs = eigvals(J)
    re, im = eigs.real, eigs.imag
    has_im = np.any(np.abs(im) > eps)

    def all_pos(a):   return np.all(a >  eps)
    def all_neg(a):   return np.all(a < -eps)
    def any_pos(a):   return np.any(a >  eps)
    def any_neg(a):   return np.any(a < -eps)
    def all_zero(a):  return np.all(np.abs(a) < eps)

    if not has_im:
        if all_neg(re):                   return "Stable node (sink)"
        if all_pos(re):                   return "Unstable node (source)"
        if any_pos(re) and any_neg(re):   return "Saddle"
        if all_zero(re):                  return "Neutral / line"
        return "Degenerate node"

    # complex part present
    a = re[np.abs(im) > eps][0]   # common real part
    if np.abs(a) < eps:           return "Center (pure rotation)"
    if a < 0:                     return "Spiral in (stable focus)"
    if a > 0:                     return "Spiral out (unstable focus)"
    return "Mixed focus"

