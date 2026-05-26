# FlowMap Manuscript Reproduction Code

This repository is a minimal reproduction dump for the FlowMap manuscript. Code is grouped by analysis/dataset rather than by old figure-folder names.

The intended template is:

- root `flowmap_legacy/` for shared legacy FlowMap helper scripts
- root `scripts/` for shared non-legacy scripts
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
- `scripts/` - shared manuscript scripts that are not legacy FlowMap internals.
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
