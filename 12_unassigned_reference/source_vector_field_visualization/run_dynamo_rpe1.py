import warnings
warnings.filterwarnings("ignore")

import dynamo as dyn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Load preprocessed scEU-seq RPE1 dataset
    print("Loading RPE1 scEU-seq data...")
    adata = dyn.sample_data.scEU_seq_rpe1()

    # Subset: keep only 'Pulse' time points
    adata = adata[adata.obs.exp_type == 'Pulse'].copy()
    adata.obs['time'] = adata.obs['time'].astype(str)
    adata.obs.loc[adata.obs['time'] == 'dmso', 'time'] = -1
    adata.obs['time'] = adata.obs['time'].astype(float)
    adata = adata[adata.obs.time != -1, :].copy()

    # Convert time from minutes to hours
    adata.obs['time'] = adata.obs['time'] / 60

    # Collapse kinetic layers into new/total
    adata.layers['new'] = adata.layers['ul'] + adata.layers['sl']
    adata.layers['total'] = adata.layers['ul'] + adata.layers['sl'] + adata.layers['su'] + adata.layers['uu']
    for layer in ['ul', 'sl', 'su', 'uu']:
        del adata.layers[layer]

    # Run Dynamo kinetic pipeline
    print("Running Dynamo kinetic pipeline...")
    dyn.tl.recipe_kin_data(
        adata,
        keep_filtered_genes=True,
        keep_raw_layers=True,
        del_2nd_moments=False,
        tkey="time"
    )

    # Optional: project velocity into RFP/GFP space
    adata.obsm['X_RFP_GFP'] = adata.obs[["RFP_log10_corrected", "GFP_log10_corrected"]].to_numpy(dtype=float)

    dyn.tl.cell_velocities(adata, basis="RFP_GFP", vkey="velocity_T", ekey="M_t", enforce=True)

    # Save final result
    print("Saving output to: rpe1_kinetics_processed.h5ad")
    adata.write("rpe1_kinetics_processed.h5ad", compression="gzip")

if __name__ == "__main__":
    main()
