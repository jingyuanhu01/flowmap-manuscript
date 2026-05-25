#!/usr/bin/env python3

import numpy as np
import anndata as ad
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
DATA_PATH = "./data/larry/larry_processed.h5ad"
OUT_PATH = "./data/larry/d_raw_pairs.npz"

K_PER_POINT = 200
CHUNK_SIZE = 50_000
SEED = 0

# ----------------------------
# Load data
# ----------------------------
print("Loading AnnData...")
adata = ad.read_h5ad(DATA_PATH)

# ----------------------------
# Expression matrix (X)
# ----------------------------
print("Preprocessing X...")
X = adata.layers["spliced"]
hvg_mask = adata.var["highly_variable"].values
X = X[:, hvg_mask]

if hasattr(X, "toarray"):
    X = X.toarray()

X = np.log1p(X)

X = StandardScaler(
    with_mean=True,
    with_std=True
).fit_transform(X)

# IMPORTANT: reduce memory
X = X.astype(np.float32)

n, d = X.shape
print(f"X shape: {n} cells × {d} genes")

# ----------------------------
# Sample random pairs
# ----------------------------
rng = np.random.default_rng(SEED)

n = X.shape[0]
k = K_PER_POINT

i_idx = np.repeat(np.arange(n), k)
j_idx = np.empty(n * k, dtype=int)

all_idx = np.arange(n)

for i in range(n):
    start = i * k
    end = (i + 1) * k

    # sample without replacement, excluding i
    j_idx[start:end] = rng.choice(
        all_idx[all_idx != i],
        size=k,
        replace=False
    )

n_pairs = len(i_idx)
print(f"Number of pairs: {n_pairs}")  # exactly n * k

# ----------------------------
# Compute raw distances (chunked)
# ----------------------------
print("Computing raw distances (chunked)...")
d_raw = np.empty(n_pairs, dtype=np.float32)

for start in range(0, n_pairs, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, n_pairs)

    diff = X[i_idx[start:end]] - X[j_idx[start:end]]
    d_raw[start:end] = np.linalg.norm(diff, axis=1)

    if start % (10 * CHUNK_SIZE) == 0:
        print(f"  processed {end:,} / {n_pairs:,}")

# ----------------------------
# Save results
# ----------------------------
print("Saving results...")
np.savez_compressed(
    OUT_PATH,
    i_idx=i_idx,
    j_idx=j_idx,
    d_raw=d_raw,
)

print(f"Saved to {OUT_PATH}")
print("Done.")
