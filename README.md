# FlowMap Code by Dataset and Content

This is the second-pass organization. It does not trust old figure filenames. Code is grouped by dataset/content first, with manuscript role noted in filenames where it is evident from notebook contents and saved outputs.

Data and generated figures are routed through repo-local placeholder folders. The notebooks should be run from their own `source_*` directory, where `./data`, `./figures`, and helper-code symlinks point back into this repo.

## Top-Level Layout

- `00_manuscript/` - optional place for the manuscript PDF.
- `00_shared_helpers/` - shared Python helpers, SIRV scripts, and B-cell preprocessing utilities.
- `01_method_overview/` - method overview / schematic-like notebooks.
- `02_simulated_vector_fields/` - synthetic 1D/2D/swiss-roll/vector-field collection benchmarks.
- `03_s_curve_tps_geometry/` - S-curve, TPS, perturbation-distance, and geometry notebooks.
- `04_cell_cycle_rpe1/` - RPE1/FUCCI cell-cycle analysis.
- `05_pancreas_endocrinogenesis/` - pancreas/endocrinogenesis analysis and scVelo kinetics.
- `06_larry_hematopoiesis/` - LARRY hematopoiesis embedding, gradients, fixed points, curvature, pseudotime.
- `07_b_cell_igvf/` - IGVF/B-cell embedding and curvature analysis.
- `08_spatial_mouse_organogenesis/` - SeqFISH/SIRV mouse organogenesis and spatial velocity analysis.
- `09_dentate_gyrus/` - dentate gyrus velocity/fixed-point notebooks.
- `10_multi_dataset_benchmarks/` - cross-dataset real-data and velocity-estimation benchmarks.
- `11_circle_and_method_exploration/` - circle toy system and method-development scratch work.
- `12_unassigned_reference/` - anything left over after the content-based pass.
- `data/` - place source data here for GitHub reproduction.
- `generated_figures/` - generated figure outputs land here through symlinks.
- `source_data/` - stable symlink layer used by notebook folders.
- `source_figures/` - stable symlink layer used by notebook folders.

## Merged Code View

Each dataset/content folder now has a `code/` folder that merges notebooks and helper scripts from both old sources:

- `source_flowmap_manuscript/`
- `source_vector_field_visualization/`

The original `source_*` folders are still present for traceability and for old relative-path behavior. The merged `code/` folders are the cleaner place to inspect and run notebooks going forward.

Inside each `code/` folder, source-specific adapters are named explicitly:

- `data_flowmap_manuscript`
- `data_vector_field_visualization`
- `data_vector_field_simulation`
- `figures_flowmap_manuscript`
- `figures_vector_field_visualization`
- `utils`
- `scripts`
- `SIRV`

See `MERGED_CODE_MANIFEST.csv` for the exact source-to-merged mapping.

## Traceability

See `MANIFEST.csv` for every move/rename from the first-pass folder into this dataset/content layout.

## Conflict Handling

The old figure-number conflicts were folded into content folders:

- Pancreas and cell-cycle notebooks both formerly claimed figure 3; they now live in separate dataset folders.
- B-cell and mouse organogenesis/spatial notebooks both formerly claimed figure 7; they now live in separate dataset folders.
- `fig3_pancreas.ipynb` from `flowmap_manuscript/other` was renamed with `.from_other`.

## Running Notebooks

Each `source_vector_field_visualization` folder has symlinks to `data`, `figures`, `simulation_data`, `scripts`, and `SIRV` where applicable. Each `source_flowmap_manuscript` folder has symlinks to `data`, `figures`, and `utils`.

Run notebooks from their own source folder. The notebooks now use repo-local relative paths such as `./data/...` and `./figures/...`.

## Data Layout

Put reproducibility data under:

- `data/flowmap_manuscript/`
- `data/vector_field_visualization/`
- `data/vector_field_simulation/`

The source folders point to those locations through relative symlinks. This avoids committing machine-specific absolute paths while still letting old notebook code use simple `./data/...` paths.

See `DATA_REQUIREMENTS.csv` for the notebook-by-notebook list of referenced data files. It is intentionally mechanical: it is a practical checklist, not a polished data dictionary.

## Public Notebook Cleanup

Notebook outputs and execution counts were cleared so the public dump does not contain local environment paths or stale warnings. This is a reproducibility dump, not a museum exhibit.
