#!/usr/bin/env python
"""Run the veloViz negative-control benchmark.

The benchmark generates isotropic high-dimensional point clouds with tiny random
velocity noise, embeds them with veloViz through rpy2, projects the velocities
onto the veloViz layout with scVelo, and saves the quiver-panel figure.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


SCVELO_ENV = Path("/Users/jh/micromamba/envs/scvelo")
R_HOME = SCVELO_ENV / "lib" / "R"


def ensure_scvelo_r_environment() -> None:
    desired_env = {
        "R_HOME": str(R_HOME),
        "RPY2_R_HOME": str(R_HOME),
        "DYLD_FALLBACK_LIBRARY_PATH": f"{SCVELO_ENV / 'lib'}:{R_HOME / 'lib'}",
        "NUMBA_CACHE_DIR": "/private/tmp/numba_scvelo_cache",
        "MPLCONFIGDIR": "/private/tmp/mpl_scvelo_cache",
        "XDG_CACHE_HOME": "/private/tmp/scvelo_xdg_cache",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
    }
    desired_path = f"{SCVELO_ENV / 'bin'}:/usr/bin:/bin:/usr/sbin:/sbin"

    needs_reexec = os.environ.get("_VELOVIZ_SCVELO_ENV_READY") != "1"
    for key, value in desired_env.items():
        if os.environ.get(key) != value:
            needs_reexec = True
            os.environ[key] = value

    if os.environ.get("PATH") != desired_path:
        needs_reexec = True
        os.environ["PATH"] = desired_path

    for cache_key in ("NUMBA_CACHE_DIR", "MPLCONFIGDIR", "XDG_CACHE_HOME"):
        Path(os.environ[cache_key]).mkdir(parents=True, exist_ok=True)

    if needs_reexec:
        os.environ["_VELOVIZ_SCVELO_ENV_READY"] = "1"
        python = SCVELO_ENV / "bin" / "python"
        if python.exists() and Path(sys.executable).resolve() != python.resolve():
            os.execve(str(python), [str(python), *sys.argv], os.environ)
        os.execve(sys.executable, [sys.executable, *sys.argv], os.environ)


ensure_scvelo_r_environment()

import anndata as ad
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scvelo as scv
from rpy2 import robjects as ro
from rpy2.robjects import conversion, numpy2ri, pandas2ri
from rpy2.robjects.vectors import StrVector


BENCHMARK_DIR = Path(__file__).resolve().parent
DATA_DIR = BENCHMARK_DIR / "data" / "neg_control"
FIGURE_DIR = BENCHMARK_DIR / "figures"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-cells", type=int, default=500)
    parser.add_argument("--dims", type=int, nargs="+", default=[2, 8, 32, 128])
    parser.add_argument("--noise-std", type=float, default=1e-2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--similarity-threshold", type=float, default=0.25)
    parser.add_argument("--distance-threshold", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=FIGURE_DIR / "negative_control_veloviz.png")
    return parser.parse_args()


def sample_unit_ball(n_cells: int, dim: int, rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(size=(n_cells, dim))
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    radii = rng.random(n_cells) ** (1.0 / dim)
    return x * radii[:, None]


def generate_negative_controls(
    data_dir: Path,
    n_cells: int,
    dims: list[int],
    noise_std: float,
    seed: int,
) -> dict[str, dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    data_dir.mkdir(parents=True, exist_ok=True)
    datasets = {}

    for dim in dims:
        tag = f"d{dim}"
        x_path = data_dir / f"X_{tag}.csv"
        v_path = data_dir / f"V_{tag}.csv"

        if x_path.exists() and v_path.exists():
            X = pd.read_csv(x_path).to_numpy()
            V = pd.read_csv(v_path).to_numpy()
        else:
            X = sample_unit_ball(n_cells, dim, rng)
            V = rng.normal(0.0, noise_std, size=X.shape)
            pd.DataFrame(X).to_csv(x_path, index=False)
            pd.DataFrame(V).to_csv(v_path, index=False)

        datasets[tag] = {"X": X, "V": V}

    return datasets


def run_veloviz(
    X: np.ndarray,
    V: np.ndarray,
    args: argparse.Namespace,
) -> tuple[np.ndarray, np.ndarray]:
    proj = X + V
    cell_names = [f"cell_{i}" for i in range(X.shape[0])]

    with conversion.localconverter(ro.default_converter + numpy2ri.converter + pandas2ri.converter):
        ro.globalenv["curr"] = X.T
        ro.globalenv["proj"] = proj.T
        ro.globalenv["cell_names"] = StrVector(cell_names)

        ro.r(
            f"""
            suppressPackageStartupMessages(library(veloviz))

            colnames(curr) <- cell_names
            colnames(proj) <- cell_names

            vv <- buildVeloviz(
                curr = curr,
                proj = proj,
                normalize.depth = FALSE,
                use.ods.genes = FALSE,
                alpha = 1,
                pca = FALSE,
                center = FALSE,
                scale = FALSE,
                k = {args.k},
                similarity.threshold = {args.similarity_threshold},
                distance.weight = 1,
                distance.threshold = {args.distance_threshold},
                weighted = FALSE,
                verbose = FALSE
            )

            veloviz_embedding <- vv$fdg_coords
            cell_names_used <- rownames(vv$fdg_coords)
            """
        )

        emb = np.asarray(ro.r["veloviz_embedding"], dtype=float)
        used_names = list(ro.r["cell_names_used"])

    keep_idx = np.array([int(str(name).split("_")[-1]) for name in used_names], dtype=int)
    return emb, keep_idx


def project_velocity(X: np.ndarray, V: np.ndarray, emb: np.ndarray) -> np.ndarray:
    adata = ad.AnnData(X)
    adata.layers["position"] = X
    adata.layers["velocity"] = V
    adata.obsm["X_veloviz"] = emb

    n_neighbors = max(2, min(30, adata.n_obs - 1))
    scv.pp.neighbors(adata, use_rep="X", n_neighbors=n_neighbors)
    scv.tl.velocity_graph(
        adata,
        xkey="position",
        vkey="velocity",
        n_jobs=1,
        backend="threading",
        show_progress_bar=False,
    )
    scv.tl.velocity_embedding(adata, basis="veloviz")
    return np.asarray(adata.obsm["velocity_veloviz"], dtype=float)


def plot_negative_controls(datasets: dict[str, dict[str, np.ndarray]], args: argparse.Namespace) -> None:
    fig, axes = plt.subplots(1, len(datasets), figsize=(2.5 * len(datasets), 4), constrained_layout=True)
    axes = np.atleast_1d(axes)

    for ax, (tag, data) in zip(axes, datasets.items()):
        X, V = data["X"], data["V"]
        emb, keep_idx = run_veloviz(X, V, args)
        Xk, Vk = X[keep_idx], V[keep_idx]
        V_emb = project_velocity(Xk, Vk, emb)

        ax.scatter(emb[:, 0], emb[:, 1], c="#FFD700", s=150, alpha=0.10, edgecolors="none")
        ax.quiver(
            emb[:, 0],
            emb[:, 1],
            V_emb[:, 0],
            V_emb[:, 1],
            color="black",
            angles="xy",
            scale_units="xy",
            scale=0.5,
            width=0.004,
            headwidth=3,
            headlength=4,
            headaxislength=3,
        )

        ax.set_title(tag)
        ax.set_aspect("equal")
        ax.axis("off")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300, bbox_inches="tight")
    print(f"Saved figure to {args.output}")


def main() -> None:
    args = parse_args()
    datasets = generate_negative_controls(
        DATA_DIR,
        n_cells=args.n_cells,
        dims=args.dims,
        noise_std=args.noise_std,
        seed=args.seed,
    )
    plot_negative_controls(datasets, args)


if __name__ == "__main__":
    main()
