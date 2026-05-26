import argparse
from pathlib import Path

import pandas as pd


DEFAULT_DATASET_ORDER = [
    "straight_line",
    "sine_curve",
    "branch_2",
    "branch_4",
    "rotation",
    "spiral",
    "saddle",
    "quadratic_source_sink",
]

DEFAULT_METHOD_ORDER = [
    "flowmap",
    "graphvelo",
    "scvelo",
    "dynamo",
    "veloviz",
]

METRIC_COLUMNS = [
    "jaccard_similarity",
    "trustworthiness",
    "magnitude_correlation",
    "avg_cosine_similarity",
    "smoothness",
]


def load_metric_tables(input_dir: Path) -> pd.DataFrame:
    frames = []
    for csv_path in sorted(input_dir.glob("*.csv")):
        method = csv_path.stem
        df = pd.read_csv(csv_path)
        if "dataset" not in df.columns:
            df = df.rename(columns={df.columns[0]: "dataset"})
        df["method"] = method
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No CSV files found in {input_dir}")

    combined = pd.concat(frames, ignore_index=True, sort=False)
    available_metrics = [col for col in METRIC_COLUMNS if col in combined.columns]
    return combined[["dataset", "method", *available_metrics]]


def sort_table(df: pd.DataFrame, dataset_order, method_order) -> pd.DataFrame:
    df = df.copy()
    df["dataset"] = pd.Categorical(df["dataset"], dataset_order, ordered=True)
    df["method"] = pd.Categorical(df["method"], method_order, ordered=True)
    return df.sort_values(["dataset", "method"]).reset_index(drop=True)


def mean_summary(df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [col for col in METRIC_COLUMNS if col in df.columns]
    return (
        df.groupby("method", observed=True)[metric_cols]
        .mean(numeric_only=True)
        .sort_index()
    )


def best_by_dataset(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metric_cols = [col for col in METRIC_COLUMNS if col in df.columns]
    for dataset, sub in df.groupby("dataset", observed=True):
        row = {"dataset": dataset}
        for metric in metric_cols:
            values = sub[["method", metric]].dropna()
            if values.empty:
                row[metric] = pd.NA
            else:
                best = values.loc[values[metric].idxmax()]
                row[metric] = f"{best['method']} ({best[metric]:.3f})"
        rows.append(row)
    return pd.DataFrame(rows)


def write_markdown_table(df: pd.DataFrame, path: Path) -> None:
    rounded = df.round(3)
    table = rounded.reset_index()
    headers = [str(col) for col in table.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in table.iterrows():
        values = []
        for value in row:
            if pd.isna(value):
                values.append("")
            elif isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Combine simulated vector-field benchmark metrics into tables."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/8_vf_collection"),
        help="Directory containing one benchmark CSV per method.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("figures/simulation_metrics"),
        help="Directory for combined benchmark tables.",
    )
    parser.add_argument(
        "--methods",
        nargs="*",
        default=DEFAULT_METHOD_ORDER,
        help="Method ordering. Methods not listed are appended alphabetically.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    df = load_metric_tables(args.input_dir)
    extra_methods = sorted(set(df["method"]) - set(args.methods))
    method_order = [m for m in args.methods if m in set(df["method"])] + extra_methods
    df = sort_table(df, DEFAULT_DATASET_ORDER, method_order)

    combined_wide = df.set_index(["dataset", "method"])
    summary = mean_summary(df)
    best = best_by_dataset(df)

    combined_csv = args.output_dir / "simulated_vf_metrics_by_dataset_method.csv"
    summary_csv = args.output_dir / "simulated_vf_metrics_mean_by_method.csv"
    best_csv = args.output_dir / "simulated_vf_best_method_by_dataset.csv"
    summary_md = args.output_dir / "simulated_vf_metrics_mean_by_method.md"
    summary_tex = args.output_dir / "simulated_vf_metrics_mean_by_method.tex"

    combined_wide.to_csv(combined_csv)
    summary.to_csv(summary_csv)
    best.to_csv(best_csv, index=False)
    write_markdown_table(summary, summary_md)
    summary.round(3).to_latex(summary_tex, float_format="%.3f")

    print(f"Saved combined table: {combined_csv}")
    print(f"Saved method means:   {summary_csv}")
    print(f"Saved best table:     {best_csv}")
    print(f"Saved Markdown:       {summary_md}")
    print(f"Saved LaTeX:          {summary_tex}")
    print()
    print(summary.round(4).to_string())


if __name__ == "__main__":
    main()
