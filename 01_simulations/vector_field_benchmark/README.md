# Vector-field simulation benchmark

Run the notebooks from this directory, in numeric order.

1. `01_simulate_1d_branching_vector_fields.ipynb`
2. `02_simulate_2d_vector_fields.ipynb`
3. `04_benchmark_simulated_flowmap_embedding.ipynb`
4. `05_benchmark_simulated_scvelo_embedding.ipynb`
5. `06_benchmark_simulated_dynamo_embedding.ipynb`
6. `07_benchmark_simulated_veloviz_embedding.ipynb`
7. `08_benchmark_simulated_graphvelo_embedding.ipynb`

`data` is a symlink to the repository-level simulation data directory. Generated
benchmark CSVs are written under `data/8_vf_collection`, and rendered benchmark
figures are written under `figures`.

`embedding_metrics.py` contains the shared embedding-quality metrics used by the
method benchmark notebooks.
