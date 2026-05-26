"""Prepare the SIRV/scVelo spatial velocity input used by the notebook.

This records the processing step used for the mouse organogenesis spatial
transcriptomics analysis. The repository notebook expects the processed output:

    data/flowmap_manuscript/mouse_organogenesis/SeqFISH_Embryo2_adata_SIRV_velocity.h5ad

The raw SeqFISH and RNA reference inputs are not committed to this repository.
For the manuscript cleanup, place the processed h5ad in the data folder and run
the analysis notebook directly.
"""

from pathlib import Path
import sys

import scanpy as sc
import scvelo as scv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "flowmap_manuscript" / "mouse_organogenesis"
SIRV_DIR = PROJECT_ROOT / "07_spatial_mouse_organogenesis" / "scripts" / "SIRV"

sys.path.insert(0, str(SIRV_DIR))
from main import SIRV  # noqa: E402


def process_embryo(embryo_name: str = "SeqFISH_Embryo2_adata.h5ad") -> Path:
    """Run the default SIRV transfer and scVelo velocity workflow."""
    rna = sc.read_h5ad(DATA_DIR / "RNA_adata.h5ad")
    seqfish = sc.read_h5ad(DATA_DIR / embryo_name)

    seqfish_imputed = SIRV(
        seqfish,
        rna,
        n_pv=50,
        metadata_to_transfer=["celltype"],
    )

    scv.pp.normalize_per_cell(seqfish_imputed, enforce=True)
    seqfish_imputed.X = seqfish.to_df()[seqfish_imputed.var_names]

    if hasattr(seqfish, "uns"):
        seqfish_imputed.uns.update(seqfish.uns)

    scv.pp.moments(seqfish_imputed, n_pcs=50, n_neighbors=30)
    scv.tl.velocity(seqfish_imputed, mode="stochastic")
    scv.tl.velocity_graph(seqfish_imputed)

    out_path = DATA_DIR / embryo_name.replace(".h5ad", "_SIRV_velocity.h5ad")
    seqfish_imputed.write_h5ad(out_path)
    return out_path


if __name__ == "__main__":
    output = process_embryo()
    print(f"Saved {output}")
