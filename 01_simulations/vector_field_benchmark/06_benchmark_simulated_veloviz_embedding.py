#!/usr/bin/env python
"""Benchmark veloViz on the simulated vector-field collection."""

from __future__ import annotations

import argparse
import os
import sys
import time
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
REPO_ROOT = BENCHMARK_DIR
while not (REPO_ROOT / "flowmap_legacy").exists():
    if REPO_ROOT.parent == REPO_ROOT:
        raise RuntimeError("Could not find repository root containing flowmap_legacy")
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flowmap_legacy.evaluation import evaluate_embedding_method

DATA_ROOT = BENCHMARK_DIR / "data"
OUT_DATA_DIR = BENCHMARK_DIR / "data" / "8_vf_collection"
OUT_FIG_DIR = BENCHMARK_DIR / "figures" / "simulation"

DATASET_PATHS = {
    "straight_line": DATA_ROOT / "1d" / "straight_line.csv",
    "sine_curve": DATA_ROOT / "1d" / "sine_curve.csv",
    "branch_2": DATA_ROOT / "1d" / "branch_2.csv",
    "branch_4": DATA_ROOT / "1d" / "branch_4.csv",
    "rotation": DATA_ROOT / "2d" / "rotation.csv",
    "spiral": DATA_ROOT / "2d" / "spiral.csv",
    "saddle": DATA_ROOT / "2d" / "saddle.csv",
    "quadratic_source_sink": DATA_ROOT / "2d" / "quadratic_source_sink.csv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=list(DATASET_PATHS),
        choices=list(DATASET_PATHS),
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--noise", type=float, default=0.3)
    parser.add_argument("--extra-dim", type=int, default=5)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--similarity-threshold", type=float, default=0.25)
    parser.add_argument("--distance-threshold", type=float, default=0.5)
    return parser.parse_args()


def load_vector_field(csv_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    df = pd.read_csv(csv_path)
    return df[["x", "y"]].to_numpy(), df[["vx", "vy"]].to_numpy(), df["time"].to_numpy()


def make_noisy_input(
    X_gt: np.ndarray,
    V_gt: np.ndarray,
    noise: float,
    extra_dim: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    X_noisy = X_gt + rng.normal(scale=noise, size=X_gt.shape)
    V_noisy = V_gt + rng.normal(scale=noise, size=V_gt.shape)
    X_dummy = rng.normal(scale=noise, size=(X_gt.shape[0], extra_dim))
    V_dummy = rng.normal(scale=noise, size=(V_gt.shape[0], extra_dim))
    return np.hstack([X_noisy, X_dummy]), np.hstack([V_noisy, V_dummy])


def run_veloviz(X: np.ndarray, V: np.ndarray, args: argparse.Namespace) -> tuple[np.ndarray, np.ndarray]:
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


def project_velocity(X: np.ndarray, V: np.ndarray, emb: np.ndarray, time_values: np.ndarray) -> tuple[ad.AnnData, np.ndarray]:
    adata = ad.AnnData(X)
    adata.layers["position"] = X
    adata.layers["velocity"] = V
    adata.obsm["X_veloviz"] = emb
    adata.obs["time"] = time_values

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
    return adata, np.asarray(adata.obsm["velocity_veloviz"], dtype=float)


def jaccard_knn_similarity(X1: np.ndarray, X2: np.ndarray, k: int = 30) -> float:
    from sklearn.neighbors import NearestNeighbors

    if X1.shape[0] <= 2:
        return np.nan
    k = max(1, min(k, X1.shape[0] - 2))
    nn1 = NearestNeighbors(n_neighbors=k + 1).fit(X1)
    nn2 = NearestNeighbors(n_neighbors=k + 1).fit(X2)
    knn1 = nn1.kneighbors(return_distance=False)[:, 1:]
    knn2 = nn2.kneighbors(return_distance=False)[:, 1:]
    return float(
        np.mean(
            [
                len(set(knn1[i]) & set(knn2[i])) / len(set(knn1[i]) | set(knn2[i]))
                for i in range(X1.shape[0])
            ]
        )
    )


def vector_field_local_smoothness(X: np.ndarray, V: np.ndarray, k: int = 30, eps: float = 1e-8) -> float:
    from sklearn.neighbors import NearestNeighbors

    if X.shape[0] <= 2:
        return np.nan
    k = max(1, min(k, X.shape[0] - 2))
    nn = NearestNeighbors(n_neighbors=k + 1).fit(X)
    knn = nn.kneighbors(return_distance=False)[:, 1:]
    ratios = []
    for i, nbrs in enumerate(knn):
        diff = np.linalg.norm(V[i] - V[nbrs], axis=1)
        denom = np.linalg.norm(V[i]) + np.linalg.norm(V[nbrs], axis=1) + eps
        ratios.extend(diff / denom)
    return 1 - 0.5 * float(np.mean(ratios))


def evaluate_embedding(X_gt: np.ndarray, X_emb: np.ndarray, V_gt: np.ndarray, V_emb: np.ndarray, k: int = 30) -> dict:
    from scipy.stats import pearsonr
    from sklearn.manifold import trustworthiness
    from sklearn.neighbors import NearestNeighbors

    k = max(1, min(k, X_gt.shape[0] - 2))
    k_trust = min(k, max(1, X_gt.shape[0] // 2 - 1))

    mags_gt = np.linalg.norm(V_gt, axis=1)
    mags_emb = np.linalg.norm(V_emb, axis=1)
    magnitude_correlation = pearsonr(mags_gt, mags_emb)[0]

    nbrs = NearestNeighbors(n_neighbors=k + 1).fit(X_gt)
    idx_mat = nbrs.kneighbors(return_distance=False)[:, 1:]

    def cos_sim(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))

    diffs = []
    for i in range(X_gt.shape[0]):
        for j in idx_mat[i]:
            diffs.append(cos_sim(V_gt[i], V_gt[j]) - cos_sim(V_emb[i], V_emb[j]))

    return {
        "jaccard_similarity": jaccard_knn_similarity(X_gt, X_emb, k=k),
        "trustworthiness": float(trustworthiness(X_gt, X_emb, n_neighbors=k_trust)),
        "magnitude_correlation": float(magnitude_correlation),
        "avg_cosine_similarity": 1 - float(np.mean(np.abs(diffs))),
        "smoothness": vector_field_local_smoothness(X_emb, V_emb, k=k),
    }


def plot_dataset(ax, adata: ad.AnnData, name: str) -> None:
    scv.pl.velocity_embedding_stream(
        adata,
        basis="veloviz",
        color="time",
        cmap="viridis",
        ax=ax,
        show=False,
        legend_loc=None,
        colorbar=False,
        density=0.3,
        arrow_size=2.5,
        linewidth=3.0,
        alpha=0.15,
        size=1000,
        title=name,
        frameon=False,
    )
    ax.set_aspect("equal")
    ax.axis("off")


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FIG_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, len(args.datasets), figsize=(4 * len(args.datasets), 4), constrained_layout=True)
    axes = np.atleast_1d(axes).ravel()
    records = []

    for ax, name in zip(axes, args.datasets):
        print(f"\n=== {name} ===")
        start = time.perf_counter()
        X_gt, V_gt, true_time = load_vector_field(DATASET_PATHS[name])
        X, V = make_noisy_input(X_gt, V_gt, args.noise, args.extra_dim, rng)

        emb, keep_idx = run_veloviz(X, V, args)
        X_conn, V_conn = X[keep_idx], V[keep_idx]
        X_gt_conn, V_gt_conn = X_gt[keep_idx], V_gt[keep_idx]
        time_conn = (true_time[keep_idx] - true_time.min()) / (true_time.max() - true_time.min() + 1e-12)

        print(f"veloViz retained {len(keep_idx)}/{X.shape[0]} points")
        adata, V_emb = project_velocity(X_conn, V_conn, emb, time_conn)
        plot_dataset(ax, adata, name)

        scores = evaluate_embedding_method(X_gt_conn, emb, V_gt_conn, V_emb, k=30)
        scores.update(
            {
                "dataset": name,
                "n_obs": len(keep_idx),
                "original_n_obs": X.shape[0],
                "retained_fraction": len(keep_idx) / X.shape[0],
                "runtime_seconds": time.perf_counter() - start,
                "veloviz_k": args.k,
                "veloviz_similarity_threshold": args.similarity_threshold,
                "veloviz_distance_threshold": args.distance_threshold,
            }
        )
        records.append(scores)
        print(pd.Series(scores).to_string())

    out_fig = OUT_FIG_DIR / "veloviz_embedding_streams.png"
    fig.savefig(out_fig, dpi=300, bbox_inches="tight")
    plt.close(fig)

    out_csv = OUT_DATA_DIR / "veloviz.csv"
    pd.DataFrame(records).to_csv(out_csv, index=False)
    print(f"\nSaved figure: {out_fig}")
    print(f"Saved metrics: {out_csv}")


if __name__ == "__main__":
    main()
