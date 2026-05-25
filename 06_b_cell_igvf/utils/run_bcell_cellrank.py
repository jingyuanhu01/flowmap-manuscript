#!/usr/bin/env python
"""Run CellRank transition and fate probabilities for the B cell dataset."""

from __future__ import annotations

import argparse
from enum import Enum
import json
import os
import time
from collections.abc import Mapping
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", str(Path(".numba_cache").resolve()))
os.environ.setdefault("MPLCONFIGDIR", str(Path(".mpl_cache").resolve()))

import cellrank as cr
import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse
from scipy.stats import entropy as scipy_entropy


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    print(f"[{timestamp()}] {message}", flush=True)


def lineage_names(lineages) -> list[str]:
    names = getattr(lineages, "names", None)
    if names is not None:
        return [str(name) for name in names]
    names = getattr(lineages, "columns", None)
    if names is not None:
        return [str(name) for name in names]
    return [f"lineage_{idx}" for idx in range(np.asarray(lineages).shape[1])]


def lineages_to_frame(lineages, obs_names: pd.Index) -> pd.DataFrame:
    if hasattr(lineages, "to_df"):
        frame = lineages.to_df()
        frame.index = obs_names
        return frame
    return pd.DataFrame(
        np.asarray(lineages),
        index=obs_names,
        columns=lineage_names(lineages),
    )


def fate_entropy_frame(fate: pd.DataFrame) -> pd.DataFrame:
    probs = fate.clip(lower=0).to_numpy(dtype=float)
    row_sums = probs.sum(axis=1, keepdims=True)
    probs = np.divide(probs, row_sums, out=np.zeros_like(probs), where=row_sums != 0)
    raw_entropy = scipy_entropy(probs, axis=1)
    max_entropy = np.log(probs.shape[1]) if probs.shape[1] > 1 else 1.0
    return pd.DataFrame(
        {
            "fate_entropy": raw_entropy,
            "fate_entropy_normalized": raw_entropy / max_entropy,
        },
        index=fate.index,
    )


def series_to_csv(series_like, path: Path) -> None:
    if series_like is None:
        return
    if hasattr(series_like, "to_series"):
        series = series_like.to_series()
    elif isinstance(series_like, pd.Series):
        series = series_like
    else:
        series = pd.Series(series_like)
    series.to_csv(path, header=True)


def sanitize_for_h5ad(value):
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, Mapping):
        return {str(k): sanitize_for_h5ad(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_for_h5ad(v) for v in value]
    if isinstance(value, tuple):
        return tuple(sanitize_for_h5ad(v) for v in value)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute a CellRank velocity transition matrix, GPCCA terminal states, "
            "and fate probabilities for the B cell velocity AnnData."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/flowmap_manuscript/b_cell/bcell_velocity_standard.h5ad"),
        help="Input AnnData with scVelo velocity results.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("data/flowmap_manuscript/b_cell_results/cellrank"),
        help="Output directory.",
    )
    parser.add_argument(
        "--cluster-key",
        default="celltype",
        help="Observation key used to name/interpret macrostates.",
    )
    parser.add_argument(
        "--n-states",
        type=int,
        default=None,
        help="Number of macrostates/terminal states for GPCCA. Defaults to number of cluster-key categories.",
    )
    parser.add_argument(
        "--estimator",
        default="cflare",
        choices=["cflare", "gpcca"],
        help="CellRank estimator. CFLARE is sparse-friendly for the 24k-cell full run.",
    )
    parser.add_argument(
        "--n-schur",
        type=int,
        default=20,
        help="Number of Schur vectors for GPCCA.",
    )
    parser.add_argument(
        "--n-jobs",
        type=int,
        default=8,
        help="Parallel jobs for fate probability solve.",
    )
    parser.add_argument(
        "--transition-n-jobs",
        type=int,
        default=1,
        help="Parallel jobs for transition matrix construction. Use 1 in sandboxed shells.",
    )
    parser.add_argument(
        "--softmax-scale",
        type=float,
        default=4.0,
        help=(
            "VelocityKernel softmax scale. Supplying a value avoids CellRank's "
            "parallel scale-estimation step, which may be blocked in sandboxed shells."
        ),
    )
    parser.add_argument(
        "--solver",
        default="gmres",
        choices=["direct", "gmres", "lgmres", "bicgstab", "gcrotmk"],
        help="Linear solver for fate probabilities.",
    )
    parser.add_argument(
        "--tol",
        type=float,
        default=1e-8,
        help="Tolerance for iterative fate probability solvers.",
    )
    parser.add_argument(
        "--priming-method",
        default="entropy",
        choices=["entropy", "kl_divergence"],
        help="CellRank native lineage priming method. Use 'entropy' for fate entropy.",
    )
    parser.add_argument(
        "--max-cells",
        type=int,
        default=None,
        help="Optional smoke-test subset size. Leave unset for all cells.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=0,
        help="Random seed for optional subsampling.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    timings: dict[str, float] = {}
    total_start = time.perf_counter()

    log(f"CellRank {cr.__version__}")
    log(f"Reading {args.input}")
    start = time.perf_counter()
    adata = sc.read_h5ad(args.input)
    timings["read_h5ad_sec"] = time.perf_counter() - start
    log(f"Loaded AnnData: {adata.n_obs:,} cells x {adata.n_vars:,} genes")

    if args.max_cells is not None and args.max_cells < adata.n_obs:
        log(f"Subsetting to {args.max_cells:,} cells for smoke test")
        rng = np.random.default_rng(args.random_state)
        idx = np.sort(rng.choice(adata.n_obs, size=args.max_cells, replace=False))
        adata = adata[idx].copy()
        rep = "X_pca" if "X_pca" in adata.obsm else None
        log(f"Recomputing neighbors for smoke-test subset using {rep or 'X'}")
        sc.pp.neighbors(adata, n_neighbors=30, use_rep=rep)

    if args.cluster_key not in adata.obs:
        raise KeyError(f"Missing adata.obs[{args.cluster_key!r}]")

    if args.n_states is None:
        args.n_states = int(adata.obs[args.cluster_key].nunique())

    log("Computing velocity transition matrix")
    start = time.perf_counter()
    vk = cr.kernels.VelocityKernel(adata)
    vk.compute_transition_matrix(
        n_jobs=args.transition_n_jobs,
        backend="threading",
        show_progress_bar=False,
        softmax_scale=args.softmax_scale,
    )
    timings["transition_matrix_sec"] = time.perf_counter() - start

    transition_path = args.outdir / "bcell_cellrank_transition_matrix.npz"
    sparse.save_npz(transition_path, vk.transition_matrix.tocsr())
    vk.write_to_adata("cellrank_velocity")
    log(f"Saved transition matrix to {transition_path}")

    if args.estimator == "gpcca":
        log(
            f"Running GPCCA with n_schur={args.n_schur}, "
            f"n_states={args.n_states}, cluster_key={args.cluster_key!r}"
        )
        estimator = cr.estimators.GPCCA(vk)

        start = time.perf_counter()
        estimator.compute_schur(n_components=args.n_schur)
        timings["schur_sec"] = time.perf_counter() - start

        start = time.perf_counter()
        estimator.compute_macrostates(n_states=args.n_states, cluster_key=args.cluster_key)
        timings["macrostates_sec"] = time.perf_counter() - start

        start = time.perf_counter()
        estimator.predict_terminal_states(n_states=args.n_states)
        timings["terminal_states_sec"] = time.perf_counter() - start
    else:
        log(
            f"Running CFLARE with k={args.n_schur}, "
            f"cluster_key={args.cluster_key!r}"
        )
        estimator = cr.estimators.CFLARE(vk)

        start = time.perf_counter()
        estimator.fit(k=args.n_schur)
        timings["eigendecomposition_sec"] = time.perf_counter() - start

        start = time.perf_counter()
        estimator.predict(cluster_key=args.cluster_key)
        timings["terminal_states_sec"] = time.perf_counter() - start

    series_to_csv(
        estimator.terminal_states,
        args.outdir / "bcell_cellrank_terminal_states.csv",
    )

    log(f"Computing fate probabilities with solver={args.solver}, n_jobs={args.n_jobs}")
    start = time.perf_counter()
    estimator.compute_fate_probabilities(
        solver=args.solver,
        n_jobs=args.n_jobs,
        backend="threading",
        show_progress_bar=False,
        use_petsc=False,
        tol=args.tol,
    )
    timings["fate_probabilities_sec"] = time.perf_counter() - start

    fate = lineages_to_frame(estimator.fate_probabilities, adata.obs_names)
    fate_path = args.outdir / "bcell_cellrank_fate_probabilities.csv"
    fate.to_csv(fate_path)
    log(f"Saved fate probabilities to {fate_path}")

    fate_by_cluster = fate.join(adata.obs[[args.cluster_key]]).groupby(args.cluster_key, observed=True).mean()
    fate_by_cluster_path = args.outdir / f"bcell_cellrank_fate_probabilities_by_{args.cluster_key}.csv"
    fate_by_cluster.to_csv(fate_by_cluster_path)
    log(f"Saved mean fate probabilities by {args.cluster_key} to {fate_by_cluster_path}")

    entropy = fate_entropy_frame(fate)
    entropy_path = args.outdir / "bcell_cellrank_fate_entropy.csv"
    entropy.to_csv(entropy_path)
    adata.obs = adata.obs.join(entropy)
    log(f"Saved true fate entropy to {entropy_path}")

    log(f"Computing CellRank lineage priming with method={args.priming_method!r}")
    start = time.perf_counter()
    priming = estimator.compute_lineage_priming(method=args.priming_method)
    timings["lineage_priming_sec"] = time.perf_counter() - start
    priming_name = f"lineage_priming_{args.priming_method}"
    priming = priming.rename(priming_name)
    priming_path = args.outdir / f"bcell_cellrank_{priming_name}.csv"
    priming.to_csv(priming_path, header=True)
    log(f"Saved CellRank native priming degree to {priming_path}")

    summary = {
        "input": str(args.input),
        "n_obs": int(adata.n_obs),
        "n_vars": int(adata.n_vars),
        "cluster_key": args.cluster_key,
        "estimator": args.estimator,
        "n_states": int(args.n_states),
        "n_schur": int(args.n_schur),
        "solver": args.solver,
        "tol": float(args.tol),
        "priming_method": args.priming_method,
        "n_jobs": int(args.n_jobs),
        "transition_n_jobs": int(args.transition_n_jobs),
        "softmax_scale": float(args.softmax_scale),
        "lineages": list(fate.columns),
        "celltype_counts": adata.obs[args.cluster_key].value_counts().to_dict(),
        "timings_sec": timings,
    }

    estimator_path = args.outdir / f"bcell_cellrank_{args.estimator}.pickle"
    estimator.write(estimator_path)
    log(f"Saved {args.estimator.upper()} estimator to {estimator_path}")

    adata_path = args.outdir / "bcell_cellrank_results.h5ad"
    result_adata = estimator.to_adata(keep="all", copy=True)
    result_adata.uns = sanitize_for_h5ad(result_adata.uns)
    result_adata.write_h5ad(adata_path)
    log(f"Saved annotated AnnData to {adata_path}")

    timings["total_sec"] = time.perf_counter() - total_start
    summary["timings_sec"] = timings
    summary_path = args.outdir / "bcell_cellrank_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    log(f"Saved summary to {summary_path}")
    log(f"Done in {timings['total_sec'] / 60:.1f} minutes")


if __name__ == "__main__":
    main()
