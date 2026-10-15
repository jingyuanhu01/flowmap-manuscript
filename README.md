# FlowMap Manuscript Reproduction Code

This repository contains analysis code and saved local figure results for the FlowMap manuscript. Code is grouped by analysis/dataset rather than by old figure-folder names.

The intended template is:

- root `flowmap_legacy/` for shared legacy FlowMap helper scripts
- root `data/` for uploaded source data
- one folder per analysis, with a notebook, a `figures/` output folder/link, and a local `utils/` folder only when that analysis needs extra Python files

## Top-Level Layout

- `01_simulations/` - all simulation code.
  - `vector_field_benchmark/` - simulated 8-vector-field collection benchmark across FlowMap, scVelo, dynamo, and veloViz.
  - `s_curve_toy_example/` - S-curve toy-example code, including simulation, TPS, perturbation-distance, and geometry notebooks.
- `08_real_data_benchmarks/` - cross-dataset real-data and velocity-estimation benchmarks.
- `02_cell_cycle_rpe1/` - RPE1/FUCCI cell-cycle manuscript notebook.
- `03_pancreas_endocrinogenesis/` - pancreas/endocrinogenesis analysis and scVelo kinetics.
- `04_larry_gradient/` - LARRY hematopoiesis embedding, gradients, fixed points, and pseudotime.
- `05_larry_curvature/` - LARRY curvature and fate-bias notebooks.
- `06_b_cell_igvf/` - IGVF/B-cell embedding, curvature analysis, and B-cell preprocessing helpers.
- `07_spatial_mouse_organogenesis/` - SeqFISH/SIRV mouse organogenesis, spatial velocity analysis, and SIRV helper scripts.
- `flowmap_legacy/` - shared legacy FlowMap/vector-field helper scripts used across notebooks.
- `data/` - place source data here for GitHub reproduction.

## Traceability

See `MANIFEST.csv` for the rough source-to-cleaned-location mapping from the first-pass folder into this dataset/content layout.

## Conflict Handling

The old figure-number conflicts were folded into content folders:

- Pancreas and cell-cycle notebooks both formerly claimed figure 3; they now live in separate dataset folders.
- B-cell and mouse organogenesis/spatial notebooks both formerly claimed figure 7; they now live in separate dataset folders.
- `fig3_pancreas.ipynb` from `flowmap_manuscript/other` was renamed with `.from_other`.

## Running Notebooks

Run notebooks from the analysis folder when possible. The cleaned notebook template writes to `./figures/` and reads source data from root `data/`.

Some older folders still contain `source_*` or `code/` compatibility layouts; those will be removed as each analysis is reduced to the few notebooks worth keeping.

## Data Layout

Put reproducibility data under:

- `data/flowmap_manuscript/`
- `data/vector_field_simulation/`

Analysis folders point to those locations through relative symlinks where needed. This avoids committing machine-specific absolute paths while still letting old notebook code use simple `./data/...` paths.

See `DATA_REQUIREMENTS.csv` for the notebook-by-notebook list of referenced data files. It is intentionally mechanical: it is a practical checklist, not a polished data dictionary.

## Saved Results and Reproduction Status

Saved figures and result tables are committed under each analysis's `figures/`
directory and the root `figures/` directory. These are existing local outputs;
most were collected from existing local outputs. The LARRY notebooks in sections 04 and 05 were subsequently executed locally to retain inline plots; see their folder READMEs for results. Other analyses were not rerun by this update.

| Analysis | Saved results |
| --- | --- |
| Simulated vector fields | [Embedding stream plots](01_simulations/vector_field_benchmark/figures/simulation/) |
| Pancreas | [Expression, concordance, pseudotime, and velocity figures](03_pancreas_endocrinogenesis/figures/) |
| LARRY gradients | [Executed notebooks and plot previews](04_larry_gradient/) |
| LARRY curvature | [Executed notebooks and plot previews](05_larry_curvature/) |
| B-cell IGVF | [Curvature, entropy, heterogeneity, and velocity figures](06_b_cell_igvf/figures/) |
| Spatial mouse organogenesis | [Spatial embedding and gene-gradient figures](07_spatial_mouse_organogenesis/figures/) |
| Cross-dataset Ricci curvature | [Figures and LARRY stage summary table](figures/ricci_cross_dataset/) |

A clone is **not yet a self-contained reproduction bundle**. Source data and
large derived arrays (`.h5ad`, `.npy`, and related formats) are excluded from Git,
as are `intermediate_data/` directories. Some local input locations are symlinks
to files outside this repository; their targets are not uploaded. No public data
archive is provided by this update. Use `DATA_REQUIREMENTS.csv` as the input
checklist and populate `data/` before running the notebooks.

Several LARRY notebooks also contain an optional local FlowMap source path
(`/Users/jh/Projects/flowmap/src`). Check their import/setup cells and configure
the FlowMap installation for your own environment. A pinned environment and a
clean-machine execution check remain necessary for full reproducibility.
