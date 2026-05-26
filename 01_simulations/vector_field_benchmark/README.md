# Vector-field simulation benchmark

Run the notebooks from this directory, in numeric order.

1. `01_simulate_1d_branching_vector_fields.ipynb`
2. `02_simulate_2d_vector_fields.ipynb`
3. `03_simulate_8_vector_field_collection.ipynb`
4. `04_benchmark_simulated_flowmap_embedding.ipynb`
5. `05_benchmark_simulated_scvelo_embedding.ipynb`
6. `06_benchmark_simulated_dynamo_embedding.ipynb`
7. `07_benchmark_simulated_veloviz_embedding.ipynb`
8. `08_benchmark_simulated_graphvelo_embedding.ipynb`
9. `09_benchmark_simulated_phase_distance_flowmap.ipynb`
10. `10_simulation_collection_main_panels.ipynb`
11. `11_simulation_collection_score_summary.ipynb`

`data` is a symlink to the repository-level simulation data directory. Generated
benchmark CSVs are written under `data/8_vf_collection`, and rendered benchmark
figures are written under `figures`.

After the per-method benchmark notebooks have generated their CSV files, run:

```bash
python combine_simulated_vf_benchmark_metrics.py
```
