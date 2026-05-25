#!/usr/bin/env python
"""Annotate B cell Leiden clusters using marker-score evidence."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("NUMBA_CACHE_DIR", str(Path(".numba_cache").resolve()))
os.environ.setdefault("MPLCONFIGDIR", str(Path(".mpl_cache").resolve()))

import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse


CANONICAL_MARKERS = {
    "Naive": [
        "IGHM",
        "IGHD",
        "TCL1A",
        "IL4R",
        "SELL",
        "FCER2",
        "BACH2",
        "BANK1",
    ],
    "Activated_B": [
        "CD69",
        "FOS",
        "NFKBIA",
        "NR4A2",
        "DUSP1",
        "FOSB",
        "JUN",
        "JUNB",
    ],
    "GC_B": [
        "AICDA",
        "BCL6",
        "RGS13",
        "MEF2B",
        "LMO2",
        "CD38",
        "KIAA1549L",
        "PALLD",
    ],
    "Pre_Plasmablast": [
        "IRF4",
        "CD27",
        "IL2RA",
        "IL2RB",
        "CD226",
        "DUSP4",
        "IL12RB2",
        "ACSL4",
    ],
    "Plasmablast": [
        "PRDM1",
        "XBP1",
        "MZB1",
        "JCHAIN",
        "TNFRSF17",
        "DERL3",
        "SDC1",
        "IRF4",
    ],
}


SUPPORTING_MARKERS = {
    "Naive": ["GRASP", "ZNF331", "IRS2", "LIX1-AS1", "NR4A2", "KCNH8", "DUSP1", "RASGEF1B", "FOSB", "ZBTB10"],
    "Activated_B": ["ITGA1", "JAZF1", "SMIM14", "AC083837.1", "ST6GALNAC3", "IL7", "NIBAN3"],
    "GC_B": ["KIAA1549L", "CFI", "HOMER2", "EEPD1", "PALLD", "SLC37A3", "FCER2"],
    "Pre_Plasmablast": ["IL2RB", "IL2RA", "CD226", "DUSP4", "ACSL4", "CLIC5", "IL12RB2"],
    "Plasmablast": ["CFAP54", "AL591518.1", "ACOXL", "FNDC3B", "AC016074.2", "NUGGC", "RASSF6", "ZNF215"],
}


CLASSIFIER_MODULES = {
    "naive": ["IGHD", "TCL1A", "IL4R", "SELL", "FCER2", "BACH2", "BANK1"],
    "activated": ["CD69", "FOS", "NFKBIA", "NR4A2"],
    "activated_support": ["ITGA1", "JAZF1", "SMIM14", "ST6GALNAC3", "IL7", "NIBAN3"],
    "gc": ["AICDA", "LMO2", "CD38", "KIAA1549L", "PALLD", "FCER2"],
    "prepb": ["IRF4", "CD27", "IL2RA", "CD226", "DUSP4", "IL12RB2", "ACSL4"],
    "pb_core": ["PRDM1", "XBP1", "MZB1", "JCHAIN", "TNFRSF17", "DERL3"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify B cell Leiden clusters using canonical marker scoring and cluster DE."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/flowmap_manuscript/b_cell/bcell_velocity_standard.h5ad"),
        help="Input AnnData.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("data/flowmap_manuscript/b_cell_results/annotation"),
        help="Output directory.",
    )
    parser.add_argument(
        "--cluster-key",
        default="leiden",
        help="Cluster key in adata.obs.",
    )
    parser.add_argument(
        "--existing-label-key",
        default="celltype",
        help="Existing label key to compare against if present.",
    )
    parser.add_argument(
        "--write-h5ad",
        action="store_true",
        help="Write an annotated h5ad copy to the output directory.",
    )
    return parser.parse_args()


def present_markers(adata: sc.AnnData, marker_dict: dict[str, list[str]]) -> dict[str, list[str]]:
    var_names = set(adata.var_names)
    return {label: [gene for gene in genes if gene in var_names] for label, genes in marker_dict.items()}


def expression_frame(adata: sc.AnnData, genes: list[str]) -> pd.DataFrame:
    x = adata[:, genes].X
    if sparse.issparse(x):
        x = x.toarray()
    return pd.DataFrame(np.asarray(x), index=adata.obs_names, columns=genes)


def add_marker_scores(adata: sc.AnnData, marker_dict: dict[str, list[str]], prefix: str) -> list[str]:
    score_keys: list[str] = []
    for label, genes in marker_dict.items():
        if not genes:
            continue
        key = f"{prefix}_{label}"
        score_keys.append(key)
        sc.tl.score_genes(
            adata,
            genes,
            score_name=key,
            ctrl_size=min(50, max(1, adata.n_vars - len(genes))),
            use_raw=False,
        )
    return score_keys


def cluster_marker_summary(adata: sc.AnnData, cluster_key: str, marker_dict: dict[str, list[str]]) -> pd.DataFrame:
    rows = []
    all_genes = sorted({gene for genes in marker_dict.values() for gene in genes})
    expr = expression_frame(adata, all_genes) if all_genes else pd.DataFrame(index=adata.obs_names)
    clusters = adata.obs[cluster_key].astype(str)
    for cluster in sorted(clusters.unique(), key=lambda x: int(x) if x.isdigit() else x):
        mask = clusters == cluster
        row = {"cluster": cluster, "n_cells": int(mask.sum())}
        for label, genes in marker_dict.items():
            if genes:
                row[f"{label}_mean_expression"] = float(expr.loc[mask, genes].mean(axis=1).mean())
                row[f"{label}_pct_any_marker"] = float((expr.loc[mask, genes] > 0).any(axis=1).mean())
            else:
                row[f"{label}_mean_expression"] = np.nan
                row[f"{label}_pct_any_marker"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows).set_index("cluster")


def module_scores_by_cluster(
    adata: sc.AnnData, cluster_key: str, marker_dict: dict[str, list[str]]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    present = present_markers(adata, marker_dict)
    all_genes = sorted({gene for genes in present.values() for gene in genes})
    expr = expression_frame(adata, all_genes)
    clusters = adata.obs[cluster_key].astype(str)
    raw = pd.DataFrame(index=sorted(clusters.unique(), key=lambda x: int(x) if x.isdigit() else x))
    raw.index.name = "cluster"
    for module, genes in present.items():
        raw[module] = expr[genes].mean(axis=1).groupby(clusters, observed=True).mean()
    z = (raw - raw.mean(axis=0)) / raw.std(axis=0, ddof=0).replace(0, np.nan)
    return raw, z.fillna(0)


def classify_clusters(module_z: pd.DataFrame) -> pd.DataFrame:
    z = module_z.copy()
    z["plasma_signal"] = z["pb_core"]
    z["activated_signal"] = z[["activated", "activated_support"]].max(axis=1)
    z["gc_signal"] = z["gc"]
    z["prepb_signal"] = z["prepb"]
    z["naive_signal"] = z["naive"]

    calls = []
    for cluster, row in z.iterrows():
        state_scores = pd.Series(
            {
                "Naive_B": row["naive_signal"],
                "Activated_B": row["activated_signal"],
                "GC_B": row["gc_signal"],
                "Pre_Plasmablast": row["prepb_signal"],
                "Plasmablast": row["plasma_signal"],
            }
        )

        if row["plasma_signal"] >= 0.45 and row["plasma_signal"] >= row["prepb_signal"] - 0.25:
            best = "Plasmablast"
        elif row["gc_signal"] >= 1.0:
            best = "GC_B"
        elif row["activated_signal"] >= 0.75:
            best = "Activated_B"
        elif row["prepb_signal"] >= 0.75:
            best = "Pre_Plasmablast"
        elif row["naive_signal"] >= -0.1:
            best = "Naive_B"
        else:
            best = str(state_scores.sort_values(ascending=False).index[0])

        broad = best
        refined = best
        if best == "Activated_B" and row["naive_signal"] >= 1.0 and row["activated_signal"] >= 1.0:
            refined = "Activated_Naive_B"
        elif best == "Activated_B" and row["activated_signal"] < 0.25:
            refined = "Ambiguous_Activated_B"
        elif best == "Plasmablast" and row["plasma_signal"] < 0.75:
            refined = "Plasmablast_like"
        elif best == "Plasmablast" and row["prepb_signal"] > row["plasma_signal"]:
            refined = "Plasmablast_prePB_transition"

        ranked = state_scores.sort_values(ascending=False)
        runner_up = next(label for label in ranked.index if label != best)
        margin = float(state_scores[best] - state_scores[runner_up])
        confidence = "high" if margin >= 0.75 else "medium" if margin >= 0.25 else "low"
        calls.append(
            {
                "cluster": cluster,
                "bcell_annotation": refined,
                "bcell_annotation_broad": broad,
                "runner_up": runner_up,
                "score_margin": margin,
                "confidence": confidence,
                "naive_z": float(row["naive_signal"]),
                "activated_z": float(row["activated_signal"]),
                "gc_z": float(row["gc_signal"]),
                "prepb_z": float(row["prepb_signal"]),
                "plasmablast_z": float(row["plasma_signal"]),
            }
        )
    return pd.DataFrame(calls).set_index("cluster")


def top_de_genes(adata: sc.AnnData, cluster_key: str, n_genes: int = 12) -> pd.DataFrame:
    sc.tl.rank_genes_groups(adata, groupby=cluster_key, method="wilcoxon", pts=True)
    names = adata.uns["rank_genes_groups"]["names"]
    scores = adata.uns["rank_genes_groups"]["scores"]
    rows = []
    for cluster in names.dtype.names:
        rows.append(
            {
                "cluster": str(cluster),
                "top_de_genes": ";".join(map(str, names[cluster][:n_genes])),
                "top_de_scores": ";".join(f"{float(x):.3f}" for x in scores[cluster][:n_genes]),
            }
        )
    return pd.DataFrame(rows).set_index("cluster")


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    adata = sc.read_h5ad(args.input)
    if args.cluster_key not in adata.obs:
        raise KeyError(f"Missing adata.obs[{args.cluster_key!r}]")

    canonical = present_markers(adata, CANONICAL_MARKERS)
    supporting = present_markers(adata, SUPPORTING_MARKERS)
    marker_manifest = {
        "canonical": canonical,
        "supporting": supporting,
        "missing_canonical": {
            label: [gene for gene in genes if gene not in canonical[label]]
            for label, genes in CANONICAL_MARKERS.items()
        },
        "missing_supporting": {
            label: [gene for gene in genes if gene not in supporting[label]]
            for label, genes in SUPPORTING_MARKERS.items()
        },
    }
    (args.outdir / "bcell_annotation_marker_manifest.json").write_text(json.dumps(marker_manifest, indent=2))

    canonical_score_keys = add_marker_scores(adata, canonical, "canonical_score")
    supporting_score_keys = add_marker_scores(adata, supporting, "supporting_score")

    clusters = adata.obs[args.cluster_key].astype(str)
    score_means = adata.obs[[*canonical_score_keys, *supporting_score_keys]].groupby(clusters, observed=True).mean()
    score_means.index.name = "cluster"

    module_raw, module_z = module_scores_by_cluster(adata, args.cluster_key, CLASSIFIER_MODULES)
    module_raw.to_csv(args.outdir / "bcell_classifier_module_means_by_cluster.csv")
    module_z.to_csv(args.outdir / "bcell_classifier_module_zscores_by_cluster.csv")

    calls = classify_clusters(module_z)
    de = top_de_genes(adata, args.cluster_key)
    marker_summary = cluster_marker_summary(
        adata,
        args.cluster_key,
        {f"canonical_{k}": v for k, v in canonical.items()} | {f"supporting_{k}": v for k, v in supporting.items()},
    )

    existing = pd.DataFrame(index=score_means.index)
    if args.existing_label_key in adata.obs:
        existing = (
            adata.obs[[args.cluster_key, args.existing_label_key]]
            .assign(**{args.cluster_key: lambda df: df[args.cluster_key].astype(str)})
            .groupby(args.cluster_key)[args.existing_label_key]
            .agg(lambda x: x.value_counts().index[0])
            .rename("previous_label")
            .to_frame()
        )

    cluster_table = calls.join(existing).join(score_means).join(marker_summary).join(de)
    cluster_table.to_csv(args.outdir / "bcell_cluster_annotation_evidence.csv")

    cluster_map = calls["bcell_annotation"].to_dict()
    broad_cluster_map = calls["bcell_annotation_broad"].to_dict()
    adata.obs["bcell_annotation"] = clusters.map(cluster_map).astype("category")
    adata.obs["bcell_annotation_broad"] = clusters.map(broad_cluster_map).astype("category")
    adata.obs["bcell_annotation_confidence"] = clusters.map(calls["confidence"].to_dict()).astype("category")
    adata.obs["bcell_annotation_cluster"] = clusters

    cell_annotations = adata.obs[
        [
            args.cluster_key,
            "bcell_annotation",
            "bcell_annotation_broad",
            "bcell_annotation_confidence",
            *([args.existing_label_key] if args.existing_label_key in adata.obs else []),
        ]
    ].copy()
    cell_annotations.to_csv(args.outdir / "bcell_celltype_annotations.csv")

    if args.write_h5ad:
        adata.write_h5ad(args.outdir / "bcell_velocity_standard_annotated.h5ad")

    print(cluster_table[["bcell_annotation", "runner_up", "score_margin", "confidence", "previous_label", "top_de_genes"]])
    print(f"Wrote outputs to {args.outdir}")


if __name__ == "__main__":
    main()
