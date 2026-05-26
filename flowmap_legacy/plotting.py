import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from sklearn.neighbors import NearestNeighbors
from scipy.stats import norm as normal
from scipy.interpolate import griddata
from .TPS import ThinPlateSpline
from scipy.ndimage import gaussian_filter1d
import matplotlib.patheffects as pe

try:
    from adjustText import adjust_text
except ImportError:
    adjust_text = None

try:
    import seaborn as sns
except ImportError:
    sns = None
try:
    from .VectorFieldGeometry import compute_velocity_on_grid
except ImportError:
    from VectorFieldGeometry import compute_velocity_on_grid


def plot_3d(points, points_color, title="",
            azim=-60, elev=9,
            grid_interval=2,
            dot_size=5, alpha=0.4):
    
    x, y, z = points.T

    fig, ax = plt.subplots(
        figsize=(6, 6),
        facecolor="white",
        subplot_kw={"projection": "3d"},
    )
    fig.suptitle(title, size=16)

    # Set transparent plot background
    ax.set_facecolor((0, 0, 0, 0))

    # Scatter with user-defined size and transparency
    col = ax.scatter(x, y, z, c=points_color,
                     s=dot_size, alpha=alpha,
                     edgecolors='none')

    # View angle
    ax.view_init(azim=azim, elev=elev)

    # Sparse grid, no tick labels
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_major_locator(ticker.MultipleLocator(grid_interval))
        axis.set_ticklabels([])

    ax.grid(True)

    # Colorbar
    fig.colorbar(col, ax=ax,
                 orientation="horizontal",
                 shrink=0.6, aspect=60, pad=0.01)

    plt.show()


def add_2d_scatter(ax, points, points_color, *,
                   title=None, cmap='viridis',
                   categorical_threshold=20,
                   force_discrete=False, force_continuous=False,
                   color_map=None,  # <-- new argument
                   vmin=None, vmax=None,
                   show_legend=True, show_axes=True,
                   **kwargs):
    x, y = points.T
    points_color = np.asarray(points_color)

    if force_discrete and force_continuous:
        raise ValueError("Choose only one of force_discrete / force_continuous.")

    if force_discrete:
        is_discrete = True
    elif force_continuous:
        is_discrete = False
    else:
        is_stringish = points_color.dtype.kind in {"U", "S", "O"}
        is_integer = np.issubdtype(points_color.dtype, np.integer)
        n_unique = len(np.unique(points_color))
        is_discrete = is_stringish or (is_integer and n_unique <= categorical_threshold)

    if is_discrete:
        unique_labels = np.unique(points_color)

        if color_map is not None:
            # Use user-provided mapping, fill in rest with base_cmap if needed
            base_cmap = plt.get_cmap('tab10' if cmap == 'viridis' else cmap, len(unique_labels))
            default_map = {lab: mcolors.to_hex(base_cmap(i)) for i, lab in enumerate(unique_labels)}
            colour_map = {**default_map, **color_map}
        else:
            base_cmap = plt.get_cmap('tab10' if cmap == 'viridis' else cmap, len(unique_labels))
            colour_map = {lab: mcolors.to_hex(base_cmap(i)) for i, lab in enumerate(unique_labels)}

        mapped_colours = np.array([colour_map[lab] for lab in points_color])

        ax.scatter(x, y, color=mapped_colours, edgecolors='none', **kwargs)

        if show_legend:
            handles = [plt.Line2D([], [], marker='o', linestyle='',
                                  color=colour_map[lab], label=str(lab))
                       for lab in unique_labels]
            ax.legend(handles=handles, fontsize=8, loc='upper right')

    else:
        if vmin is None: vmin = np.nanmin(points_color)
        if vmax is None: vmax = np.nanmax(points_color)
        sc = ax.scatter(x, y, c=points_color, cmap=cmap,
                        vmin=vmin, vmax=vmax, edgecolors='none', **kwargs)
        plt.colorbar(sc, ax=ax, label='Value')

    if title:
        ax.set_title(title, fontsize=10)

    if not show_axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_frame_on(False)



def plot_2d(points, points_color, title="", color_map=None,
            figsize=(6, 6), show_legend=True, show_axes=True,
            **kwargs):
    fig, ax = plt.subplots(figsize=figsize, facecolor="white", constrained_layout=True)
    fig.suptitle(title, size=12)
    ax.tick_params(axis='both', which='major', labelsize=8)

    add_2d_scatter(ax, points, points_color,
                   show_legend=show_legend,
                   show_axes=show_axes,color_map=color_map,
                   **kwargs)

    if show_axes:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()    
    
    
def plot_3d_with_quiver(
    points,
    derivatives,
    points_color,
    s=20,
    alpha=0.3,
    arrow_size=0.2,
    normalize=True,
    title="",
    cmap="coolwarm",
    show_colorbar=True,
    show_axes=True
):
    x, y, z = points.T
    dx, dy, dz = derivatives.T

    fig, ax = plt.subplots(
        figsize=(6, 6),
        facecolor="white",
        tight_layout=True,
        subplot_kw={"projection": "3d"},
    )
    fig.suptitle(title, size=16)

    # --- colormap & normalization ---
    cmap_obj = cm.get_cmap(cmap)
    norm = mcolors.Normalize(
        vmin=np.min(points_color),
        vmax=np.max(points_color),
    )

    # --- scatter ---
    col = ax.scatter(
        x, y, z,
        c=points_color,
        s=s,
        alpha=alpha,
        cmap=cmap_obj,
        norm=norm,
    )

    # --- quiver ---
    arrow_colors = cmap_obj(norm(points_color))
    ax.quiver(
        x, y, z,
        dx, dy, dz,
        length=arrow_size,
        normalize=normalize,
        color=arrow_colors,
        alpha=1.0,
        arrow_length_ratio=0.6,
    )

    ax.view_init(azim=-60, elev=9)

    # --------------------------------------------------
    # AXIS CLEANUP (this is the key part)
    # --------------------------------------------------
    if not show_axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_zlabel("")

        # remove panes (the grey boxes)
        ax.xaxis.pane.set_visible(False)
        ax.yaxis.pane.set_visible(False)
        ax.zaxis.pane.set_visible(False)

        # remove grid lines
        ax.grid(False)

    if show_colorbar:
        fig.colorbar(
            col,
            ax=ax,
            orientation="horizontal",
            shrink=0.6,
            aspect=60,
            pad=0.01,
            label="Point Color",
        )

    plt.show()


def plot_2d_quiver(
    X,
    vectors,
    color,
    s=10,
    alpha=0.3,
    scale=1,
    cmap="coolwarm",
    use_normalized=False,
    title="",
    arrow_color=None,
):
    """
    Plots a 2D quiver (vector field) with matched point/arrow colors
    and minimal framing (no box, no axis labels).
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib import cm

    # --- optionally normalize vectors ---
    if use_normalized:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms

    # --- colormap + normalization ---
    cmap_obj = cm.get_cmap(cmap)
    norm = mcolors.Normalize(
        vmin=np.min(color),
        vmax=np.max(color),
    )
    rgba_colors = cmap_obj(norm(color))

    # --- plot ---
    fig, ax = plt.subplots(figsize=(10,10), facecolor="white")

    ax.scatter(
        X[:, 0],
        X[:, 1],
        color=arrow_color if arrow_color is not None else rgba_colors,
        s=s,
        alpha=alpha,
        edgecolors="none",
    )

    ax.quiver(
        X[:, 0],
        X[:, 1],
        vectors[:, 0],
        vectors[:, 1],
        color=rgba_colors,
        angles="xy",
        scale_units="xy",
        scale=scale,
        width=0.003,
        alpha=1.0,
    )

    # --- styling: no box, no ticks, no labels ---
    ax.set_title(title, fontsize=12)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_frame_on(False)

    plt.show()


def plot_vector_field_grid(
    X_emb,
    tps_vf=None,
    V=None,
    grid_size=50,
    grid_density=1.0,
    smooth=0.5,
    n_neighbors=None,
    min_mass=0.01,
    scatter_color=None,
    scatter_size=80,
    scatter_alpha=0.1,
    stream_color="black",
    stream_alpha=0.9,
    stream_scale=3.0,
    arrow_width=0.0025,
    figsize=(6, 6),
    cmap="viridis",
    vmin=None,
    vmax=None,
):
    """
    Quiver plot of a 2D velocity field from either:
      - a fitted ThinPlateSpline (tps_vf), or
      - raw point velocities (V) that will be locally smoothed via a new TPS.
    """

    # --- build or reuse TPS model ---
    if tps_vf is None:
        if V is None:
            raise ValueError("Either `tps_vf` or `V` must be provided.")
        from .TPS import ThinPlateSpline

        n_points = X_emb.shape[0]
        max_points = 4000
        if n_points > max_points:
            idx = np.random.choice(n_points, max_points, replace=False)
            X_fit = X_emb[idx]
            V_fit = V[idx]
            print(f"[TPS] Subsampling {max_points}/{n_points} points for fitting …")
        else:
            X_fit = X_emb
            V_fit = V
            print(f"[TPS] Using all {n_points} points for fitting …")

        tps_vf = ThinPlateSpline(X_fit, n_control_points=100)
        tps_vf.fit(V_fit, dof=15)

    # --- evaluate field on grid ---
    Xg, keep, Vg, (xx, yy) = compute_velocity_on_grid(
        X_emb,
        tps_vf=tps_vf,
        grid_size=grid_size,
        grid_density=grid_density,
        smooth=smooth,
        n_neighbors=n_neighbors,
        min_mass=min_mass,
        return_mesh=True
    )

    # --- start plot ---
    plt.figure(figsize=figsize)

    # ----- scatter -----
    if scatter_color is None:
        plt.scatter(X_emb[:, 0], X_emb[:, 1], s=scatter_size, color="gray", alpha=scatter_alpha)
    else:
        scatter_color = np.array(scatter_color)
        if np.issubdtype(scatter_color.dtype, np.number):
            sc = plt.scatter(
                X_emb[:, 0], X_emb[:, 1],
                s=scatter_size, c=scatter_color,
                alpha=scatter_alpha, cmap=cmap,
                vmin=vmin, vmax=vmax
            )
            plt.colorbar(sc, shrink=0.75)
        else:
            uniq = np.unique(scatter_color)
            lut = {k: i for i, k in enumerate(uniq)}
            numeric_color = np.array([lut[val] for val in scatter_color])
            cmap_obj = plt.get_cmap(cmap, len(uniq))
            plt.scatter(
                X_emb[:, 0], X_emb[:, 1],
                s=scatter_size, c=numeric_color,
                cmap=cmap_obj, alpha=scatter_alpha
            )

    # ----- quiver arrows -----
    plt.quiver(
        Xg[:, 0], Xg[:, 1],
        Vg[:, 0], Vg[:, 1],
        angles="xy",
        scale_units="xy",
        scale=stream_scale,
        width=arrow_width,
        headwidth=3,
        color=stream_color,
        alpha=stream_alpha
    )

    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.show() 
    

def quiver_autoscale(X_grid, V_grid):
    # A simple autoscale: maximum speed among grid points.
    speeds = np.sqrt(np.sum(V_grid**2, axis=1))
    return speeds.max() if speeds.max() != 0 else 1


def plot_curve_and_twist(
    emb,
    seed=None,
    ax_top=None,
    ax_bot=None,
    cmap=plt.cm.viridis,
    twist_vmin=0.0,
    twist_vmax=1.0,
    smooth=10,
):
    # Fit principal curve
    pc, twist_mag = emb.fit_principal_curve(smooth=smooth)
    curve_pts = pc.points
    lam_curve = pc.pseudotimes

    # Smooth twist
    twist_smooth = gaussian_filter1d(twist_mag, sigma=2)

    # Color mapping
    norm = mcolors.Normalize(vmin=twist_vmin, vmax=twist_vmax)
    base_colors = cmap(norm(np.clip(twist_mag, twist_vmin, twist_vmax)))
    alphas = np.clip((twist_mag - twist_vmin) / (twist_vmax - twist_vmin), 0, 1) * 0.8 + 0.2
    base_colors[:, -1] = alphas

    # Sort for better rendering
    sort_idx = np.argsort(twist_mag)
    pts_sorted = curve_pts[sort_idx]
    colors_sorted = base_colors[sort_idx]

    # Create axes if needed
    if ax_top is None or ax_bot is None:
        fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(6, 8), gridspec_kw={'height_ratios': [3, 1]})
    else:
        fig = None

    # Top: principal curve plot
    ax_top.scatter(emb.X_emb[:, 0], emb.X_emb[:, 1], c='lightgrey', s=12, alpha=0.4)
    ax_top.scatter(pts_sorted[:, 0], pts_sorted[:, 1], color=colors_sorted, s=30)
    ax_top.set_title(f"Seed {seed}: Principal Curve", fontsize=14)
    ax_top.axis('equal')
    ax_top.axis('off')

    # Colorbar
    sm = cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = plt.colorbar(sm, ax=ax_top, pad=0.01)
    cbar.set_label("Twist Magnitude", fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Bottom: twist magnitude plot
    ax_bot.plot(lam_curve, twist_smooth, color='steelblue', lw=2)
    ax_bot.set_xlabel(r"λ (curve parameter)", fontsize=12)
    ax_bot.set_title("Twist Magnitude", fontsize=13)
    ax_bot.grid(ls='--', lw=0.4)
    ax_bot.set_ylim([0, twist_vmax])
    ax_bot.tick_params(labelsize=10)
    ax_bot.set_ylabel("")

    if fig is not None:
        plt.tight_layout()
        plt.show()


def add_cluster_labels(X_2d, labels, ax, font_size=12, font_color="black"):
    labels = np.asarray(labels)
    unique_labels = np.unique(labels)

    for label in unique_labels:
        points = X_2d[labels == label]
        if len(points) == 0:
            continue
        center = points.mean(axis=0)
        text = ax.text(center[0], center[1], str(label),
                       fontsize=font_size, color=font_color,
                       ha="center", va="center")
        text.set_path_effects([
            pe.Stroke(linewidth=3, foreground="white"),
            pe.Normal()
        ])


def plot_velocity_streamplot(
    X_2d, tps_vf=None, V=None, scatter_color="grey",
    grid_size=50, grid_density=1.0, stream_density=1.0, title=None,
    scatter_size=10, scatter_alpha=0.5, arrowsize=1.5,
    ax=None, figsize=(8, 6), aspect="equal", cmap="tab10",
    vmin=None, vmax=None, show_axes=True, show_colorbar=False,
    streamline_thickness=4.0, show_labels=True, use_cmap=True,
    pad_frac=0.0,
):

    # --- fit model if not provided ---
    if tps_vf is None:
        if V is None:
            raise ValueError("Either tps_vf or V must be provided.")
        from .TPS import ThinPlateSpline

        # --- subsample if too many points ---
        n_points = X_2d.shape[0]
        max_points = 4000
        if n_points > max_points:
            idx = np.random.choice(n_points, max_points, replace=False)
            X_fit = X_2d[idx]
            V_fit = V[idx]
            print(f"[TPS] Subsampling {max_points}/{n_points} points for fitting …")
        else:
            X_fit = X_2d
            V_fit = V
            print(f"[TPS] Using all {n_points} points for fitting …")

        # --- fit thin-plate spline on 2D subset ---
        tps_vf = ThinPlateSpline(X_fit, n_control_points=100)
        tps_vf.fit(V_fit, dof=15)

    # --- compute filtered grid ---
    Xg, keep, Vg, (xx, yy) = compute_velocity_on_grid(
        X_2d, tps_vf=tps_vf,
        grid_size=grid_size, grid_density=grid_density,
        min_mass=0.01, return_mesh=True
    )
    
    # --- reconstruct full grid ---
    ny, nx = yy.shape[0], xx.shape[1]
    grid_x, grid_y = xx[0, :], yy[:, 0]
    Vx = np.full((ny, nx), np.nan)
    Vy = np.full((ny, nx), np.nan)

    dx = (grid_x[-1] - grid_x[0]) / (nx - 1)
    dy = (grid_y[-1] - grid_y[0]) / (ny - 1)
    j_idx = np.clip(np.rint((Xg[:, 0] - grid_x[0]) / dx).astype(int), 0, nx - 1)
    i_idx = np.clip(np.rint((Xg[:, 1] - grid_y[0]) / dy).astype(int), 0, ny - 1)
    Vx[i_idx, j_idx] = Vg[:, 0]
    Vy[i_idx, j_idx] = Vg[:, 1]

    U = np.ma.masked_invalid(Vx)
    V = np.ma.masked_invalid(Vy)

    # --- plotting ---
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        created_fig = True

    # ---------- robust scatter coloring ----------
    scatter_color = np.array(scatter_color)
    if scatter_color.dtype.kind in {"U", "S", "O"}:  # categorical labels
        unique_vals = np.unique(scatter_color)
        cmap_obj = plt.get_cmap(cmap, len(unique_vals))
        color_map = {val: mcolors.to_hex(cmap_obj(i)) for i, val in enumerate(unique_vals)}
        mapped_colors = np.array([color_map[val] for val in scatter_color])
        ax.scatter(
            X_2d[:, 0], X_2d[:, 1],
            s=scatter_size, alpha=scatter_alpha,
            edgecolors="none", color=mapped_colors
        )
    else:  # numeric or pre-colored array
        if np.issubdtype(scatter_color.dtype, np.number):
            sc = ax.scatter(
                X_2d[:, 0], X_2d[:, 1],
                s=scatter_size, alpha=scatter_alpha,
                c=scatter_color, cmap=cmap, vmin=vmin, vmax=vmax,
                edgecolors="none"
            )
            if show_colorbar:
                plt.colorbar(sc, ax=ax)
        else:
            ax.scatter(
                X_2d[:, 0], X_2d[:, 1],
                s=scatter_size, alpha=scatter_alpha,
                edgecolors="none", color=scatter_color
            )
    # ---------------------------------------------

    # --- streamlines ---
    speed = np.sqrt(Vx**2 + Vy**2)
    smax = np.nanmax(speed) if np.isfinite(speed).any() else 0.0
    linewidth = streamline_thickness * (speed / smax) if smax > 0 else 1.0

    ax.streamplot(
        grid_x, grid_y, U, V,
        linewidth=linewidth,
        density=stream_density,
        color="k",
        arrowsize=arrowsize,
        arrowstyle="-|>",
        maxlength=4,
        integration_direction="both"
    )

    # --- optional axis padding (robust) ---
    if pad_frac > 0:
        # use both data points and grid extent
        xmin = np.nanmin([X_2d[:, 0].min(), grid_x.min()])
        xmax = np.nanmax([X_2d[:, 0].max(), grid_x.max()])
        ymin = np.nanmin([X_2d[:, 1].min(), grid_y.min()])
        ymax = np.nanmax([X_2d[:, 1].max(), grid_y.max()])

        dx = xmax - xmin
        dy = ymax - ymin

        ax.set_xlim(xmin - pad_frac * dx, xmax + pad_frac * dx)
        ax.set_ylim(ymin - pad_frac * dy, ymax + pad_frac * dy)
    
    ax.set_aspect(aspect)
    if not show_axes:
        ax.set_xticks([]); ax.set_yticks([]); ax.set_frame_on(False)
    else:
        ax.grid(True, linestyle='--', alpha=0.3)
    if title:
        ax.set_title(title)

    if created_fig:
        plt.tight_layout()
        plt.show()


def plot_gene_r2_scatter(
    r2,
    genes,
    thr_expr=0.7,
    thr_vel=0.4,
    figsize=(8, 8),
    bins=40,
    highlight_color="darkorange",
    base_color="steelblue"
):
    if sns is None:
        raise ImportError("plot_gene_r2_scatter requires seaborn. Install seaborn or skip this plotting helper.")

    # metrics
    x = np.array(r2["expr_corr_gene"])
    y = np.array(r2["vel_corr_gene"])
    genes = np.array(genes)

    # drop NaNs
    mask = np.isfinite(x) & np.isfinite(y)
    x, y, genes = x[mask], y[mask], genes[mask]

    sns.set_style("whitegrid")
    sns.set_context("talk", font_scale=1.3)

    g = sns.jointplot(
        x=x, y=y,
        kind="scatter",
        color=base_color,
        edgecolor="white",
        s=90, alpha=0.8,
        marginal_kws=dict(bins=bins, fill=True),
        height=figsize[0]
    )

    # regression line
    sns.regplot(x=x, y=y, scatter=False, ax=g.ax_joint,
                color="crimson", line_kws={"lw":2.5, "alpha":0.8})

    # thresholds
    good = (x > thr_expr) & (y > thr_vel)

    # highlight points
    g.ax_joint.scatter(
        x[good], y[good],
        color=highlight_color, s=150,
        edgecolor="black", lw=0.6, zorder=3
    )

    # text annotations without boxes
    texts = []
    for xi, yi, gene in zip(x[good], y[good], genes[good]):
        texts.append(
            g.ax_joint.text(
                xi, yi, str(gene),
                fontsize=14, weight="bold", color="black",
                ha="center", va="center"
            )
        )

    # improved text dodging
    if adjust_text is not None:
        adjust_text(
            texts,
            x=x[good], y=y[good],
            ax=g.ax_joint,
            arrowprops=dict(arrowstyle="-", color="black", lw=1),
            expand_points=(1.4, 1.6),
            expand_text=(1.4, 1.6),
            force_points=1.5,
            force_text=1.5,
            only_move={'points': 'y', 'text': 'xy'}  # allow text to move flexibly
        )

    # axis & labels
    g.set_axis_labels(
        "Expression correlation (y, ŷ)",
        "Velocity correlation (v, v̂)",
        fontsize=18
    )

    # grid & ticks
    g.ax_joint.axhline(thr_vel, color="grey", ls="--", lw=1.2, alpha=0.7)
    g.ax_joint.axvline(thr_expr, color="grey", ls="--", lw=1.2, alpha=0.7)
    g.ax_joint.tick_params(axis='both', labelsize=14)

    plt.tight_layout()
    plt.show()
    return g
