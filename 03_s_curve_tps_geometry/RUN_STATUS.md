# Run Status: 03_s_curve_tps_geometry

Executed with these kernels:

- `scvelo` for notebooks whose kernelspec explicitly named `scvelo`.
- `flowmap-manuscript` for generic `python3` / old base-style notebooks, because the `flowmap` dev kernel lacks legacy notebook dependencies such as `umap`.

## Passing

- `source_vector_field_visualization/simulate_s_curve_vector_field.ipynb`
- `source_vector_field_visualization/simulate_s_curve_high_dimensional_vf.ipynb`
- `source_vector_field_visualization/s_curve_embedding_tps_refinement.ipynb`
- `source_vector_field_visualization/s_curve_tps_parameter_tuning.ipynb`
- `source_vector_field_visualization/s_curve_mds_gradient_descent.ipynb`
- `source_vector_field_visualization/s_curve_perturbation_distance.ipynb`

## Still Failing / Legacy-Broken

- `source_vector_field_visualization/s_curve_tps_vector_field.ipynb`
  - Current blocker: missing optional `plotly`.
- `source_vector_field_visualization/s_curve_tps_iterative_refinement.ipynb`
  - Current blocker: stale variable `X_optimized`.
- `source_vector_field_visualization/s_curve_tps_iterative_refinement_copy1.ipynb`
  - Current blocker: missing optional `plotly`.
- `source_vector_field_visualization/s_curve_iterative_embedding_algorithm.ipynb`
  - Current blocker: missing optional `numdifftools`.
- `source_vector_field_visualization/s_curve_linear_denoising.ipynb`
  - Current blocker: dimensional mismatch between high-dimensional S-curve data and 3D denoising projection assumptions.
- `source_vector_field_visualization/s_curve_perturbation_distance_validation.ipynb`
  - Current blocker: missing optional `cvxpy`.

## Compatibility Patches Applied

- S-curve generator now writes the downstream `gt`, `noisy`, and `noisy_hd` CSV files.
- High-dimensional S-curve notebook imports `VectorFieldEmbedder` and `matplotlib` explicitly.
- Shared plotting handles missing `adjustText` / `seaborn` more gracefully.
- `TPS.py` accepts legacy `dof_target`.
- `TPS.py` exposes legacy aliases `compute_tps_jacobians` and `project_velocities`.
- Restored `denoising.py` and `perturbation_distance.py` into shared `scripts/`.
- Added a top-level `perturbation_distance.py` shim for notebooks that import it without `scripts.`.
- Patched stale `tps_viz_vf` usage to fall back to `tps_vf`.
- Guarded unavailable principal-curve/twist panels in `s_curve_embedding_tps_refinement.ipynb`.

Detailed raw logs:

- `RUN_LOG.md`
- `RUN_LOG_round2.md`
- `RUN_LOG_round3.md`
- `RUN_LOG_round4.md`
