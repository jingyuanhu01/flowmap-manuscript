## s_curve_tps_vector_field.ipynb
[NbConvertApp] Converting notebook s_curve_tps_vector_field.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
metrics = tps.evaluate_fit(X)
metrics
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[7], line 1[0m
[0;32m----> 1[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      2[0m metrics

[0;31mTypeError[0m: ThinPlateSpline.evaluate_fit() missing 1 required positional argument: 'Y'

FAIL s_curve_tps_vector_field.ipynb

## s_curve_tps_iterative_refinement.ipynb
[NbConvertApp] Converting notebook s_curve_tps_iterative_refinement.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
tps = ThinPlateSpline(X_2d, n_control_points=1000)
tps.fit(X, dof_target=50)
metrics = tps.evaluate_fit(X)
metrics
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[6], line 3[0m
[1;32m      1[0m tps [38;5;241m=[39m ThinPlateSpline(X_2d, n_control_points[38;5;241m=[39m[38;5;241m1000[39m)
[1;32m      2[0m tps[38;5;241m.[39mfit(X, dof_target[38;5;241m=[39m[38;5;241m50[39m)
[0;32m----> 3[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      4[0m metrics

[0;31mTypeError[0m: ThinPlateSpline.evaluate_fit() missing 1 required positional argument: 'Y'

FAIL s_curve_tps_iterative_refinement.ipynb

## s_curve_tps_iterative_refinement_copy1.ipynb
[NbConvertApp] Converting notebook s_curve_tps_iterative_refinement_copy1.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
tps = ThinPlateSpline(X_2d, n_control_points=1000)
tps.fit(X, dof_target=50)
metrics = tps.evaluate_fit(X)
metrics
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[6], line 3[0m
[1;32m      1[0m tps [38;5;241m=[39m ThinPlateSpline(X_2d, n_control_points[38;5;241m=[39m[38;5;241m1000[39m)
[1;32m      2[0m tps[38;5;241m.[39mfit(X, dof_target[38;5;241m=[39m[38;5;241m50[39m)
[0;32m----> 3[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      4[0m metrics

[0;31mTypeError[0m: ThinPlateSpline.evaluate_fit() missing 1 required positional argument: 'Y'

FAIL s_curve_tps_iterative_refinement_copy1.ipynb

## s_curve_tps_parameter_tuning.ipynb
[NbConvertApp] Converting notebook s_curve_tps_parameter_tuning.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
import numpy as np
import matplotlib.pyplot as plt
from scripts.TPS import ThinPlateSpline

# Define the range of degrees of freedom to test in log space
dof_targets = np.logspace(np.log10(20), np.log10(410), 11)  # Logarithmically spaced values

# Store the computed metrics
rmse_values = []
r2_values = []
gcv_values = []
rmse_gt_values = []

# Create TPS model
n_control_points = 1000  # Adjust as needed
tps = ThinPlateSpline(X_2d, n_control_points=n_control_points)

# Iterate over different degrees of freedom
for dof_target in dof_targets:
    print(f"Running with dof: {dof_target:.2f}")
    tps.fit(X_noisy, dof_target=dof_target)
    metrics = tps.evaluate_fit(X_noisy)
    
    # Compute RMSE with ground truth
    X_smoothed = tps.predict(X_2d)
    RSS_gt = np.sum((X - X_smoothed) ** 2)
    RMSE_gt = np.sqrt(RSS_gt / (X.shape[0] * X.shape[1]))

    # Store metrics
    rmse_values.append(metrics["RMSE"])
    r2_values.append(metrics["R2"])
    gcv_values.append(metrics["GCV"])
    rmse_gt_values.append(RMSE_gt)
------------------

----- stdout -----
Running with dof: 20.00
------------------

[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[14], line 22[0m
[1;32m     20[0m [38;5;28mprint[39m([38;5;124mf[39m[38;5;124m"[39m[38;5;124mRunning with dof: [39m[38;5;132;01m{[39;00mdof_target[38;5;132;01m:[39;00m[38;5;124m.2f[39m[38;5;132;01m}[39;00m[38;5;124m"[39m)
[1;32m     21[0m tps[38;5;241m.[39mfit(X_noisy, dof_target[38;5;241m=[39mdof_target)
[0;32m---> 22[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX_noisy[49m[43m)[49m
[1;32m     24[0m [38;5;66;03m# Compute RMSE with ground truth[39;00m
[1;32m     25[0m X_smoothed [38;5;241m=[39m tps[38;5;241m.[39mpredict(X_2d)

[0;31mTypeError[0m: ThinPlateSpline.evaluate_fit() missing 1 required positional argument: 'Y'

FAIL s_curve_tps_parameter_tuning.ipynb

## s_curve_mds_gradient_descent.ipynb
[NbConvertApp] Converting notebook s_curve_mds_gradient_descent.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
from sklearn.manifold import Isomap

# isomap = Isomap(n_components=2, n_neighbors=20)
# X_2d = isomap.fit_transform(X)
X_2d = np.random.uniform(0, 1, size=(1000, 2))
plot_2d(X_2d, t)
geodesic_distances = isomap.dist_matrix_

lam = 0.01
num_iterations = 20
for i in range(num_iterations):
    print(f"Iteration {i+1}")

    # Step 2: Fit the thin-plate spline (TPS)
    tps = ThinPlateSpline(X_2d, n_control_points=1000)
    tps.fit(X, lambda_reg=100)
    X_2d, optimization_result = optimize_total(tps, X_2d, X, geodesic_distances, lam, disp=False)

    # Final visualization
    plot_2d(X_2d, t, "Iterative TPS Optimization")
    plot_3d(tps.predict(X_2d), t, "Iterative TPS Optimization")
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mNameError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[12], line 7[0m
[1;32m      5[0m X_2d [38;5;241m=[39m np[38;5;241m.[39mrandom[38;5;241m.[39muniform([38;5;241m0[39m, [38;5;241m1[39m, size[38;5;241m=[39m([38;5;241m1000[39m, [38;5;241m2[39m))
[1;32m      6[0m plot_2d(X_2d, t)
[0;32m----> 7[0m geodesic_distances [38;5;241m=[39m [43misomap[49m[38;5;241m.[39mdist_matrix_
[1;32m      9[0m lam [38;5;241m=[39m [38;5;241m0.01[39m
[1;32m     10[0m num_iterations [38;5;241m=[39m [38;5;241m20[39m

[0;31mNameError[0m: name 'isomap' is not defined

FAIL s_curve_mds_gradient_descent.ipynb

## s_curve_iterative_embedding_algorithm.ipynb
[NbConvertApp] Converting notebook s_curve_iterative_embedding_algorithm.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
smoothed_values = smooth_values(X_grid, X_2d)
smoothed_values
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mNameError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[6], line 1[0m
[0;32m----> 1[0m smoothed_values [38;5;241m=[39m smooth_values([43mX_grid[49m, X_2d)
[1;32m      2[0m smoothed_values

[0;31mNameError[0m: name 'X_grid' is not defined

FAIL s_curve_iterative_embedding_algorithm.ipynb

## s_curve_linear_denoising.ipynb
[NbConvertApp] Converting notebook s_curve_linear_denoising.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
X = pd.read_csv("./data/s_curve/s_curve_noisy_hd_position_matrix.csv")
Y = pd.read_csv("./data/s_curve/s_curve_noisy_hd_velocity_matrix.csv")
t = pd.read_csv("./data/s_curve/s_curve_gt_latent_time_vector.csv")
t = list(t["t"])

X_gt = pd.read_csv("./data/s_curve/s_curve_gt_position_matrix.csv")
Y_gt = pd.read_csv("./data/s_curve/s_curve_gt_velocity_matrix.csv")

X.shape, Y.shape
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mFileNotFoundError[0m                         Traceback (most recent call last)
Cell [0;32mIn[3], line 1[0m
[0;32m----> 1[0m X [38;5;241m=[39m [43mpd[49m[38;5;241;43m.[39;49m[43mread_csv[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43m./data/s_curve/s_curve_noisy_hd_position_matrix.csv[39;49m[38;5;124;43m"[39;49m[43m)[49m
[1;32m      2[0m Y [38;5;241m=[39m pd[38;5;241m.[39mread_csv([38;5;124m"[39m[38;5;124m./data/s_curve/s_curve_noisy_hd_velocity_matrix.csv[39m[38;5;124m"[39m)
[1;32m      3[0m t [38;5;241m=[39m pd[38;5;241m.[39mread_csv([38;5;124m"[39m[38;5;124m./data/s_curve/s_curve_gt_latent_time_vector.csv[39m[38;5;124m"[39m)

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1026[0m, in [0;36mread_csv[0;34m(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)[0m
[1;32m   1013[0m kwds_defaults [38;5;241m=[39m _refine_defaults_read(
[1;32m   1014[0m     dialect,
[1;32m   1015[0m     delimiter,
[0;32m   (...)[0m
[1;32m   1022[0m     dtype_backend[38;5;241m=[39mdtype_backend,
[1;32m   1023[0m )
[1;32m   1024[0m kwds[38;5;241m.[39mupdate(kwds_defaults)
[0;32m-> 1026[0m [38;5;28;01mreturn[39;00m [43m_read[49m[43m([49m[43mfilepath_or_buffer[49m[43m,[49m[43m [49m[43mkwds[49m[43m)[49m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/pandas/io/parsers/readers.py:620[0m, in [0;36m_read[0;34m(filepath_or_buffer, kwds)[0m
[1;32m    617[0m _validate_names(kwds[38;5;241m.[39mget([38;5;124m"[39m[38;5;124mnames[39m[38;5;124m"[39m, [38;5;28;01mNone[39;00m))
[1;32m    619[0m [38;5;66;03m# Create the parser.[39;00m
[0;32m--> 620[0m parser [38;5;241m=[39m [43mTextFileReader[49m[43m([49m[43mfilepath_or_buffer[49m[43m,[49m[43m [49m[38;5;241;43m*[39;49m[38;5;241;43m*[39;49m[43mkwds[49m[43m)[49m
[1;32m    622[0m [38;5;28;01mif[39;00m chunksize [38;5;129;01mor[39;00m iterator:
[1;32m    623[0m     [38;5;28;01mreturn[39;00m parser

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1620[0m, in [0;36mTextFileReader.__init__[0;34m(self, f, engine, **kwds)[0m
[1;32m   1617[0m     [38;5;28mself[39m[38;5;241m.[39moptions[[38;5;124m"[39m[38;5;124mhas_index_names[39m[38;5;124m"[39m] [38;5;241m=[39m kwds[[38;5;124m"[39m[38;5;124mhas_index_names[39m[38;5;124m"[39m]
[1;32m   1619[0m [38;5;28mself[39m[38;5;241m.[39mhandles: IOHandles [38;5;241m|[39m [38;5;28;01mNone[39;00m [38;5;241m=[39m [38;5;28;01mNone[39;00m
[0;32m-> 1620[0m [38;5;28mself[39m[38;5;241m.[39m_engine [38;5;241m=[39m [38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43m_make_engine[49m[43m([49m[43mf[49m[43m,[49m[43m [49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mengine[49m[43m)[49m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1880[0m, in [0;36mTextFileReader._make_engine[0;34m(self, f, engine)[0m
[1;32m   1878[0m     [38;5;28;01mif[39;00m [38;5;124m"[39m[38;5;124mb[39m[38;5;124m"[39m [38;5;129;01mnot[39;00m [38;5;129;01min[39;00m mode:
[1;32m   1879[0m         mode [38;5;241m+[39m[38;5;241m=[39m [38;5;124m"[39m[38;5;124mb[39m[38;5;124m"[39m
[0;32m-> 1880[0m [38;5;28mself[39m[38;5;241m.[39mhandles [38;5;241m=[39m [43mget_handle[49m[43m([49m
[1;32m   1881[0m [43m    [49m[43mf[49m[43m,[49m
[1;32m   1882[0m [43m    [49m[43mmode[49m[43m,[49m
[1;32m   1883[0m [43m    [49m[43mencoding[49m[38;5;241;43m=[39;49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43moptions[49m[38;5;241;43m.[39;49m[43mget[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43mencoding[39;49m[38;5;124;43m"[39;49m[43m,[49m[43m [49m[38;5;28;43;01mNone[39;49;00m[43m)[49m[43m,[49m
[1;32m   1884[0m [43m    [49m[43mcompression[49m[38;5;241;43m=[39;49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43moptions[49m[38;5;241;43m.[39;49m[43mget[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43mcompression[39;49m[38;5;124;43m"[39;49m[43m,[49m[43m [49m[38;5;28;43;01mNone[39;49;00m[43m)[49m[43m,[49m
[1;32m   1885[0m [43m    [49m[43mmemory_map[49m[38;5;241;43m=[39;49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43moptions[49m[38;5;241;43m.[39;49m[43mget[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43mmemory_map[39;49m[38;5;124;43m"[39;49m[43m,[49m[43m [49m[38;5;28;43;01mFalse[39;49;00m[43m)[49m[43m,[49m
[1;32m   1886[0m [43m    [49m[43mis_text[49m[38;5;241;43m=[39;49m[43mis_text[49m[43m,[49m
[1;32m   1887[0m [43m    [49m[43merrors[49m[38;5;241;43m=[39;49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43moptions[49m[38;5;241;43m.[39;49m[43mget[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43mencoding_errors[39;49m[38;5;124;43m"[39;49m[43m,[49m[43m [49m[38;5;124;43m"[39;49m[38;5;124;43mstrict[39;49m[38;5;124;43m"[39;49m[43m)[49m[43m,[49m
[1;32m   1888[0m [43m    [49m[43mstorage_options[49m[38;5;241;43m=[39;49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43moptions[49m[38;5;241;43m.[39;49m[43mget[49m[43m([49m[38;5;124;43m"[39;49m[38;5;124;43mstorage_options[39;49m[38;5;124;43m"[39;49m[43m,[49m[43m [49m[38;5;28;43;01mNone[39;49;00m[43m)[49m[43m,[49m
[1;32m   1889[0m [43m[49m[43m)[49m
[1;32m   1890[0m [38;5;28;01massert[39;00m [38;5;28mself[39m[38;5;241m.[39mhandles [38;5;129;01mis[39;00m [38;5;129;01mnot[39;00m [38;5;28;01mNone[39;00m
[1;32m   1891[0m f [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mhandles[38;5;241m.[39mhandle

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/pandas/io/common.py:873[0m, in [0;36mget_handle[0;34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)[0m
[1;32m    868[0m [38;5;28;01melif[39;00m [38;5;28misinstance[39m(handle, [38;5;28mstr[39m):
[1;32m    869[0m     [38;5;66;03m# Check whether the filename is to be opened in binary mode.[39;00m
[1;32m    870[0m     [38;5;66;03m# Binary mode does not support 'encoding' and 'newline'.[39;00m
[1;32m    871[0m     [38;5;28;01mif[39;00m ioargs[38;5;241m.[39mencoding [38;5;129;01mand[39;00m [38;5;124m"[39m[38;5;124mb[39m[38;5;124m"[39m [38;5;129;01mnot[39;00m [38;5;129;01min[39;00m ioargs[38;5;241m.[39mmode:
[1;32m    872[0m         [38;5;66;03m# Encoding[39;00m
[0;32m--> 873[0m         handle [38;5;241m=[39m [38;5;28;43mopen[39;49m[43m([49m
[1;32m    874[0m [43m            [49m[43mhandle[49m[43m,[49m
[1;32m    875[0m [43m            [49m[43mioargs[49m[38;5;241;43m.[39;49m[43mmode[49m[43m,[49m
[1;32m    876[0m [43m            [49m[43mencoding[49m[38;5;241;43m=[39;49m[43mioargs[49m[38;5;241;43m.[39;49m[43mencoding[49m[43m,[49m
[1;32m    877[0m [43m            [49m[43merrors[49m[38;5;241;43m=[39;49m[43merrors[49m[43m,[49m
[1;32m    878[0m [43m            [49m[43mnewline[49m[38;5;241;43m=[39;49m[38;5;124;43m"[39;49m[38;5;124;43m"[39;49m[43m,[49m
[1;32m    879[0m [43m        [49m[43m)[49m
[1;32m    880[0m     [38;5;28;01melse[39;00m:
[1;32m    881[0m         [38;5;66;03m# Binary mode[39;00m
[1;32m    882[0m         handle [38;5;241m=[39m [38;5;28mopen[39m(handle, ioargs[38;5;241m.[39mmode)

[0;31mFileNotFoundError[0m: [Errno 2] No such file or directory: './data/s_curve/s_curve_noisy_hd_position_matrix.csv'

FAIL s_curve_linear_denoising.ipynb

## s_curve_perturbation_distance.ipynb
[NbConvertApp] Converting notebook s_curve_perturbation_distance.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
X_noise_std = 0.3
Y_noise_std = 0.3
neighbors = 20
# Get shape
n_samples = X_gt.shape[0]

# Add Gaussian noise to original 3D data
X = X_gt + np.random.normal(scale=X_noise_std, size=X_gt.shape)
Y = Y_gt + np.random.normal(scale=Y_noise_std, size=Y_gt.shape)

# Standardize to mean 0, std 1
X = (X - X.mean(axis=0)) / X.std(axis=0)
Y = (Y - Y.mean(axis=0)) / Y.std(axis=0)

solver = PerturbDistanceSolver(X, Y, quantile=0.5)
t_dist = solver.pairwise_time_constrained_L2_distance()

# ------------------------------------------------------------------------------
# Define the range of betas on a log scale
# ------------------------------------------------------------------------------
alphas = np.logspace(-1, 2, 3)
alphas = np.concatenate(([0], alphas))
dist_mat_sq = cdist(X, X, metric='sqeuclidean')

fig, axes = plt.subplots(nrows=len(alphas), ncols=2, figsize=(12, 4 * len(alphas)))
for i, alpha in enumerate(alphas):
    dist_mat = np.sqrt(dist_mat_sq + alpha * t_dist ** 2)
    
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    coords_mds = mds.fit_transform(dist_mat)
    
    trust_mds = trustworthiness(X_gt, coords_mds, n_neighbors=neighbors)
    jaccard_mds = jaccard_knn_similarity(X_gt, coords_mds, k=neighbors)
    ax_mds = axes[i, 0] 
    sc_mds = ax_mds.scatter(coords_mds[:, 0], coords_mds[:, 1],
                            c=col, s=30, alpha=0.8, cmap='viridis')
    ax_mds.set_title(f"MDS | alpha={alpha:.3f} | Trust={trust_mds:.2f} | Jaccard={jaccard_mds:.2f}")
    ax_mds.set_xticks([])
    ax_mds.set_yticks([])
    ax_mds.grid(True)
    
    # -----------------------------------------------------
    # 3. UMAP with precomputed distances
    # -----------------------------------------------------
    reducer = umap.UMAP(
        n_neighbors=neighbors,
        n_components=2,
        metric="precomputed",
#         min_dist = 0.4,
        random_state=1
    )
    coords_umap = reducer.fit_transform(dist_mat)
    
    trust_umap = trustworthiness(X_gt, coords_umap, n_neighbors=neighbors)
    jaccard_umap = jaccard_knn_similarity(X_gt, coords_umap, k=neighbors)
    
    ax_umap = axes[i, 1]  # right column for UMAP
    sc_umap = ax_umap.scatter(coords_umap[:, 0], coords_umap[:, 1],
                              c=col, s=30, alpha=0.8, cmap='viridis')
    ax_umap.set_title(f"UMAP | alpha={alpha:.3f} | Trust={trust_umap:.2f} | Jaccard={jaccard_umap:.2f}")
    ax_umap.set_xticks([])
    ax_umap.set_yticks([])
    ax_umap.grid(True)

plt.tight_layout()
plt.show()
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[7], line 15[0m
[1;32m     12[0m X [38;5;241m=[39m (X [38;5;241m-[39m X[38;5;241m.[39mmean(axis[38;5;241m=[39m[38;5;241m0[39m)) [38;5;241m/[39m X[38;5;241m.[39mstd(axis[38;5;241m=[39m[38;5;241m0[39m)
[1;32m     13[0m Y [38;5;241m=[39m (Y [38;5;241m-[39m Y[38;5;241m.[39mmean(axis[38;5;241m=[39m[38;5;241m0[39m)) [38;5;241m/[39m Y[38;5;241m.[39mstd(axis[38;5;241m=[39m[38;5;241m0[39m)
[0;32m---> 15[0m solver [38;5;241m=[39m [43mPerturbDistanceSolver[49m[43m([49m[43mX[49m[43m,[49m[43m [49m[43mY[49m[43m,[49m[43m [49m[43mquantile[49m[38;5;241;43m=[39;49m[38;5;241;43m0.5[39;49m[43m)[49m
[1;32m     16[0m t_dist [38;5;241m=[39m solver[38;5;241m.[39mpairwise_time_constrained_L2_distance()
[1;32m     18[0m [38;5;66;03m# ------------------------------------------------------------------------------[39;00m
[1;32m     19[0m [38;5;66;03m# Define the range of betas on a log scale[39;00m
[1;32m     20[0m [38;5;66;03m# ------------------------------------------------------------------------------[39;00m

[0;31mTypeError[0m: PerturbDistanceSolver.__init__() got an unexpected keyword argument 'quantile'

FAIL s_curve_perturbation_distance.ipynb

## s_curve_perturbation_distance_validation.ipynb
[NbConvertApp] Converting notebook s_curve_perturbation_distance_validation.ipynb to notebook
Traceback (most recent call last):
  File "/opt/homebrew/bin/jupyter-nbconvert", line 6, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/application.py", line 284, in launch_instance
    super().launch_instance(argv=argv, **kwargs)
  File "/opt/homebrew/lib/python3.11/site-packages/traitlets/config/application.py", line 1075, in launch_instance
    app.start()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 420, in start
    self.convert_notebooks()
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 597, in convert_notebooks
    self.convert_single_notebook(notebook_filename)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 563, in convert_single_notebook
    output, resources = self.export_single_notebook(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/nbconvertapp.py", line 487, in export_single_notebook
    output, resources = self.exporter.from_filename(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 201, in from_filename
    return self.from_file(f, resources=resources, **kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 220, in from_file
    return self.from_notebook_node(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/notebook.py", line 36, in from_notebook_node
    nb_copy, resources = super().from_notebook_node(nb, resources, **kw)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 154, in from_notebook_node
    nb_copy, resources = self._preprocess(nb_copy, resources)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/exporters/exporter.py", line 353, in _preprocess
    nbc, resc = preprocessor(nbc, resc)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/base.py", line 48, in __call__
    return self.preprocess(nb, resources)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 103, in preprocess
    self.preprocess_cell(cell, resources, index)
  File "/opt/homebrew/lib/python3.11/site-packages/nbconvert/preprocessors/execute.py", line 124, in preprocess_cell
    cell = self.execute_cell(cell, index, store_history=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jupyter_core/utils/__init__.py", line 165, in wrapped
    return loop.run_until_complete(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 1062, in async_execute_cell
    await self._check_raise_for_error(cell, cell_index, exec_reply)
  File "/opt/homebrew/lib/python3.11/site-packages/nbclient/client.py", line 918, in _check_raise_for_error
    raise CellExecutionError.from_cell_and_msg(cell, exec_reply_content)
nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
------------------
from perturbation_distance import PerturbDistanceSolver
import numpy as np
import pandas as pd

X_gt = np.array(pd.read_csv("./data/s_curve/uniform/s_curve_gt_position_matrix.csv"))
Y_gt = np.array(pd.read_csv("./data/s_curve/uniform/s_curve_gt_velocity_matrix.csv"))

X = X_gt
Y = Y_gt
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[1], line 1[0m
[0;32m----> 1[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mperturbation_distance[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m PerturbDistanceSolver
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mnumpy[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mnp[39;00m
[1;32m      3[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mpandas[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mpd[39;00m

[0;31mModuleNotFoundError[0m: No module named 'perturbation_distance'

FAIL s_curve_perturbation_distance_validation.ipynb

