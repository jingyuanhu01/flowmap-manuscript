import numpy as np


def compute_flow_curvature(emb, X_emb, eps=1e-12):
    """
    Compute geometric curvature quantities for a vector field flowing on a TPS-reconstructed
    surface ψ : R^d → R^D.

    Returned quantities
    -------------------
    k_total : (N,)
        Total curvature of the ambient trajectory γ(t) = ψ(X_emb(t)), normalized by speed^2.
        Combines geodesic steering curvature and normal (extrinsic) curvature:
            k_total^2 = k_geod^2 + k_normal^2.

    k_geod : (N,)
        Geodesic curvature: curvature *within* the tangent plane of the surface.
        Measures how much the trajectory turns while remaining on the surface.
        Computed from the component of acceleration orthogonal to the flow direction
        but tangent to the manifold.

    k_normal : (N,)
        Normal (extrinsic) curvature: acceleration orthogonal to the surface.
        Measures how the surface geometry itself forces a deviation in ambient space.

    A : (N, D)
        Full ambient acceleration vector d²γ/dt² in gene space.

    V : (N, D)
        Ambient velocity vector dγ/dt = Jψ v, where v is the chart-space velocity field.

    A_tan : (N, d)
        Component of acceleration projected onto the tangent space of the surface.

    A_along : (N, D)
        Tangential acceleration in the direction of motion (along the unit tangent T).
        Controls speed changes along the trajectory.

    A_steer : (N, d)
        Tangential acceleration orthogonal to the direction of motion.
        Responsible for turning within the surface; used to compute k_geod.

    A_nor : (N, D)
        Normal acceleration orthogonal to the surface; used to compute k_normal.

    T : (N, D)
        Unit ambient tangent vector V / ||V||.
    """

    # ------------------------------------------
    # 1. Geometry of the surface ψ : R^d → R^D
    # ------------------------------------------
    J_f = emb.tps.compute_jacobians(X_emb)    # (N, D, d)
    H_f = emb.tps.compute_hessians(X_emb)     # (N, D, d, d)

    # ------------------------------------------
    # 2. Vector field on the chart
    # ------------------------------------------
    v  = emb.tps_vf.predict(X_emb)            # (N, d)
    Jv = emb.tps_vf.compute_jacobians(X_emb)  # (N, d, d)

    # ------------------------------------------
    # 3. Ambient velocity
    # ------------------------------------------
    V = np.einsum("ndk,nk->nd", J_f, v)       # (N, D)
    speed2 = np.einsum("nd,nd->n", V, V)
    speed  = np.sqrt(speed2 + eps)
    T = V / speed[:, None]                   # unit tangent

    # ------------------------------------------
    # 4. Ambient acceleration A
    # ------------------------------------------
    A1 = np.einsum("ndij,ni,nj->nd", H_f, v, v)
    a_u = np.einsum("nij,nj->ni", Jv, v)
    A2 = np.einsum("ndk,nk->nd", J_f, a_u)
    A = A1 + A2

    # ------------------------------------------
    # 5. Tangent / Normal projectors
    # ------------------------------------------
    g = np.einsum("ndk,ndl->nkl", J_f, J_f)
    g_inv = np.linalg.inv(g + eps * np.eye(g.shape[-1]))

    P_tan = np.einsum("ndi,nij,ncj->ndc", J_f, g_inv, J_f)
    N_pts, D = V.shape
    I = np.eye(D)[None, :, :]
    P_nor = I - P_tan

    # ------------------------------------------
    # 6. Acceleration decomposition
    # ------------------------------------------
    A_tan = np.einsum("ndj,nd->nj", P_tan, A)
    A_nor = np.einsum("ndj,nd->nj", P_nor, A)

    a_long_scalar = np.einsum("nd,nd->n", A_tan, T)
    A_along = a_long_scalar[:, None] * T

    A_steer = A_tan - A_along

    # ------------------------------------------
    # 7. Curvatures
    # ------------------------------------------
    k_geod   = np.linalg.norm(A_steer, axis=1) / (speed2 + eps)
    k_normal = np.linalg.norm(A_nor, axis=1)   / (speed2 + eps)

    k_total  = np.sqrt(k_geod**2 + k_normal**2)

    # ------------------------------------------
    # Return
    # ------------------------------------------
    return {
        "k_total":   k_total,
        "k_normal":  k_normal,
        "k_geod":    k_geod,
        "A":         A,
        "V":         V,
        "A_tan":     A_tan,
        "A_along":   A_along,
        "A_steer":   A_steer,
        "A_nor":     A_nor,
        "T":         T,
    }
