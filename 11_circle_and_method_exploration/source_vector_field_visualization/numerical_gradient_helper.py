import numpy as np

# -------------------------
# Action with fixed (uniform) dt
# -------------------------
def action_value(path, f, D=1.0, dt=1.0):
    """
    S = (1/(2D)) * Σ_k || (x_{k+1}-x_k)/dt - f((x_{k+1}+x_k)/2) ||^2 * dt
    """
    path = np.asarray(path, float)
    segs = path[1:] - path[:-1]                 # (n, d)
    mids = 0.5 * (path[1:] + path[:-1])         # (n, d)
    f_mids = np.array([f(y) for y in mids])     # (n, d)
    v = segs / dt                               # (n, d)
    r = v - f_mids                              # (n, d)
    S = 0.5 / D * np.sum(np.sum(r**2, axis=1) * dt)
    return float(S)

# ---------------------------------------------
# Analytic gradient (fixed uniform dt; midpoint Jacobian)
# ---------------------------------------------
def grad_action_analytic(path, f, jac_mid, D=1.0, dt=1.0):
    """
    ∂S/∂x_m = (1/D)*[(g_{m-1}-g_m) - (dt/2)*(J_{m-1}^T g_{m-1} + J_m^T g_m)]
    with g_k = (x_{k+1}-x_k)/dt - f( (x_{k+1}+x_k)/2 ), J_k = J_f(midpoint).
    Endpoints fixed -> gradient zero there.
    """
    path = np.asarray(path, float)
    n_plus_1, d = path.shape
    n = n_plus_1 - 1
    grad = np.zeros_like(path)

    segs = path[1:] - path[:-1]
    mids = 0.5 * (path[1:] + path[:-1])
    f_mids = np.array([f(y) for y in mids])
    v = segs / dt
    g = v - f_mids
    Jm = np.array([jac_mid(y) for y in mids])  # (n, d, d)

    for m in range(1, n):
        term_main = g[m-1] - g[m]
        term_jac  = (Jm[m-1].T @ g[m-1]) + (Jm[m].T @ g[m])
        grad[m] = (term_main - 0.5 * dt * term_jac) / D

    # endpoints fixed
    grad[0] = 0.0
    grad[-1] = 0.0
    return grad

# ---------------------------------
# Numerical gradient (forward diff)
# ---------------------------------
def grad_action_numeric(path, f, D=1.0, dt=1.0, eps=1e-7):
    """Finite-difference gradient of S wrt path; endpoints fixed."""
    path = np.asarray(path, float)
    grad = np.zeros_like(path)
    base = action_value(path, f, D=D, dt=dt)

    for i in range(1, len(path) - 1):   # interior only
        for j in range(path.shape[1]):
            pert = path.copy()
            pert[i, j] += eps
            val_plus = action_value(pert, f, D=D, dt=dt)
            grad[i, j] = (val_plus - base) / eps
    return grad

# -------------------------
# Simple optimizer (GD)
# -------------------------
def lap_optimize(path, f, jac_mid, D=1.0, numeric_grad=False, lr=1e-3, iters=200, callback=None):
    """
    Gradient descent on the fixed-dt action.
    - Always uses uniform dt = 1 / n_segments (computed inside).
    - If `numeric_grad` is True, uses finite-diff gradient; else analytic.
    - `callback(it, action)` is called every iteration if provided.
    """
    path = np.asarray(path, float).copy()
    n_segments = len(path) - 1
    dt = 1.0 / float(n_segments)  # uniform dt inside, as requested

    for it in range(iters):
        if numeric_grad:
            g = grad_action_numeric(path, f, D=D, dt=dt)
        else:
            g = grad_action_analytic(path, f, jac_mid=jac_mid, D=D, dt=dt)

        path[1:-1] -= lr * g[1:-1]  # keep endpoints fixed

        if callback is not None:
            S = action_value(path, f, D=D, dt=dt)
            callback(it, S)

    return path, dt
