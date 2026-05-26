# Vector-field simulation benchmark

Run the code from this directory, in numeric order.

1. `01_simulate_1d_branching_vector_fields.ipynb`
2. `02_simulate_2d_vector_fields.ipynb`
3. `03_benchmark_simulated_flowmap_embedding.ipynb`
4. `04_benchmark_simulated_scvelo_embedding.ipynb`
5. `05_benchmark_simulated_dynamo_embedding.ipynb`
6. `06_benchmark_simulated_veloviz_embedding.py`
7. `07_benchmark_simulated_graphvelo_embedding.ipynb`

`data` is a symlink to the repository-level simulation data directory. Generated
benchmark CSVs are written under `data/8_vf_collection`, and rendered benchmark
figures are written under `figures`.

The benchmark code imports shared metric and legacy embedding code from
`flowmap_legacy` at the repository root.
