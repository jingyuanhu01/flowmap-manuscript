# Manuscript Figure Candidates

This file records likely manuscript figure ownership based on notebook contents, saved output paths, markdown headings, and loaded datasets. The main organization is by dataset/content; these figure links are intentionally secondary.

## Main Figure Candidates

- Figure 2 / simulated vector-field benchmark:
  - `01_simulation_benchmark/source_vector_field_visualization/simulation_collection_main_panels.ipynb`
  - `01_simulation_benchmark/source_vector_field_visualization/simulation_collection_score_summary.ipynb`
  - `01_simulation_benchmark/source_vector_field_visualization/benchmark_simulated_*_embedding.ipynb`

- Pancreas / endocrinogenesis figure:
  - `03_pancreas_endocrinogenesis/source_flowmap_manuscript/pancreas_main_embedding_concordance_gene_panels.ipynb`
  - `03_pancreas_endocrinogenesis/source_flowmap_manuscript/pancreas_flowmap_gene_evaluation_vs_deg.ipynb`
  - `03_pancreas_endocrinogenesis/source_flowmap_manuscript/pancreas_scvelo_kinetics_velocity_inference.ipynb`

- RPE1 / FUCCI cell-cycle figure:
  - `02_cell_cycle_rpe1/cell_cycle_main_phase_embedding_streams.ipynb`

- LARRY embedding / fixed-point / gradient figure:
  - `04_larry_gradient/source_flowmap_manuscript/larry_main_embedding_and_legend.ipynb`
  - `04_larry_gradient/source_flowmap_manuscript/larry_main_fp1_gradient_field_paths.ipynb`

- LARRY curvature / fate-bias figure:
  - `05_larry_curvature/source_flowmap_manuscript/larry_main_curvature_fate_bias.ipynb`
  - `05_larry_curvature/source_vector_field_visualization/larry_curvature_region*_*.ipynb`

- B-cell / IGVF figure:
  - `06_b_cell_igvf/source_flowmap_manuscript/b_cell_main_velocity_curvature_volcano_panels.ipynb`
  - `06_b_cell_igvf/source_flowmap_manuscript/b_cell_*curvature_panels.ipynb`

- Mouse organogenesis / spatial velocity figure:
  - `07_spatial_mouse_organogenesis/source_flowmap_manuscript/mouse_organogenesis_main_spatial_velocity_gene_gradients.ipynb`
  - `07_spatial_mouse_organogenesis/source_vector_field_visualization/mouse_organogenesis_embedding_spatial_velocity.ipynb`

## Supplement / Methods Candidates

- S-curve and TPS geometry:
  - `02_s_curve_toy_example/source_flowmap_manuscript/supplement_simulate_s_curve.ipynb`
  - `02_s_curve_toy_example/source_vector_field_visualization/s_curve_*.ipynb`

- Multi-dataset real-data benchmarks:
  - `03_real_data_benchmark/source_*/*.ipynb`

- Dentate gyrus:
  - `09_dentate_gyrus/source_vector_field_visualization/*.ipynb`

- Circle toy system and method exploration:
  - `11_circle_and_method_exploration/source_vector_field_visualization/*.ipynb`

## Notes

- The previous figure-number conflicts are no longer represented as directory names. They are now separate dataset folders.
- Some notebooks combine analysis and plotting for a dataset; those stayed with the dataset rather than being split by figure number.
- PDF text extraction tools were not available in this environment, so this map is based on notebook content and output paths rather than parsed manuscript captions.
