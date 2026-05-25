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
import plotly.graph_objects as go
import numpy as np

grid_3d = tps.predict(grid_points)
# Stack grid points and data points together
combined_3d = np.vstack([grid_3d, X_smoothed])
combined_colors = [0] * len(grid_3d) + list(t)  # Grey for grid, t for data

# Create an interactive scatter plot
fig = go.Figure()

# Add grid points (grey)
fig.add_trace(go.Scatter3d(
    x=grid_3d[:, 0], y=grid_3d[:, 1], z=grid_3d[:, 2],
    mode='markers',
    marker=dict(size=3, color='grey'),
    name='Grid Points'
))

# Add data points (colored by t)
fig.add_trace(go.Scatter3d(
    x=X_smoothed[:, 0], y=X_smoothed[:, 1], z=X_smoothed[:, 2],
    mode='markers',
    marker=dict(size=3, color=t, colorscale='Viridis', opacity=0.8),
    name='Data Points'
))

# Layout settings
fig.update_layout(
    title="Interactive 3D Plot of Grid and Data Points",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z"
    )
)

# Show interactive plot
fig.show()

------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[12], line 1[0m
[0;32m----> 1[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mplotly[39;00m[38;5;21;01m.[39;00m[38;5;21;01mgraph_objects[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mgo[39;00m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mnumpy[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mnp[39;00m
[1;32m      4[0m grid_3d [38;5;241m=[39m tps[38;5;241m.[39mpredict(grid_points)

[0;31mModuleNotFoundError[0m: No module named 'plotly'

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
projected_velocities = tps.project_velocities(X_2d, Y)
tps_vf = ThinPlateSpline(X_2d)
tps_vf.fit(projected_velocities, dof_target=30)
smoothed_velocities = tps_vf.predict(X_2d) 

plot_2d_quiver(X_2d, smoothed_velocities, t, scale=5, cmap='coolwarm', arrow_color='black')
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mAttributeError[0m                            Traceback (most recent call last)
Cell [0;32mIn[10], line 1[0m
[0;32m----> 1[0m projected_velocities [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mproject_velocities[49m(X_2d, Y)
[1;32m      2[0m tps_vf [38;5;241m=[39m ThinPlateSpline(X_2d)
[1;32m      3[0m tps_vf[38;5;241m.[39mfit(projected_velocities, dof_target[38;5;241m=[39m[38;5;241m30[39m)

[0;31mAttributeError[0m: 'ThinPlateSpline' object has no attribute 'project_velocities'

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
import plotly.graph_objects as go
import numpy as np

grid_3d = tps.predict(grid_points)
# Stack grid points and data points together
combined_3d = np.vstack([grid_3d, X_smoothed])
combined_colors = [0] * len(grid_3d) + list(t)  # Grey for grid, t for data

# Create an interactive scatter plot
fig = go.Figure()

# Add grid points (grey)
fig.add_trace(go.Scatter3d(
    x=grid_3d[:, 0], y=grid_3d[:, 1], z=grid_3d[:, 2],
    mode='markers',
    marker=dict(size=3, color='grey'),
    name='Grid Points'
))

# Add data points (colored by t)
fig.add_trace(go.Scatter3d(
    x=X_smoothed[:, 0], y=X_smoothed[:, 1], z=X_smoothed[:, 2],
    mode='markers',
    marker=dict(size=3, color=t, colorscale='Viridis', opacity=0.8),
    name='Data Points'
))

# Layout settings
fig.update_layout(
    title="Interactive 3D Plot of Grid and Data Points",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z"
    )
)

# Show interactive plot
fig.show()

------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[11], line 1[0m
[0;32m----> 1[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mplotly[39;00m[38;5;21;01m.[39;00m[38;5;21;01mgraph_objects[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mgo[39;00m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mnumpy[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mnp[39;00m
[1;32m      4[0m grid_3d [38;5;241m=[39m tps[38;5;241m.[39mpredict(grid_points)

[0;31mModuleNotFoundError[0m: No module named 'plotly'

FAIL s_curve_tps_iterative_refinement_copy1.ipynb

## s_curve_tps_parameter_tuning.ipynb
[NbConvertApp] Converting notebook s_curve_tps_parameter_tuning.ipynb to notebook
[NbConvertApp] Writing 1498511 bytes to s_curve_tps_parameter_tuning.ipynb
PASS s_curve_tps_parameter_tuning.ipynb

## s_curve_mds_gradient_descent.ipynb
[NbConvertApp] Converting notebook s_curve_mds_gradient_descent.ipynb to notebook
[NbConvertApp] Writing 5314870 bytes to s_curve_mds_gradient_descent.ipynb
PASS s_curve_mds_gradient_descent.ipynb

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
import numdifftools as nd

X_flat = X_2d[:10,:].flatten()
D = squareform(pdist(X[:10,:], metric='euclidean')) ** 2
loss_func = lambda X_flat: loss(X_flat, D, tps, X[:10,:])
numerical_grad = nd.Gradient(loss_func)(X_flat)
numerical_grad
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[17], line 1[0m
[0;32m----> 1[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mnumdifftools[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mnd[39;00m
[1;32m      3[0m X_flat [38;5;241m=[39m X_2d[:[38;5;241m10[39m,:][38;5;241m.[39mflatten()
[1;32m      4[0m D [38;5;241m=[39m squareform(pdist(X[:[38;5;241m10[39m,:], metric[38;5;241m=[39m[38;5;124m'[39m[38;5;124meuclidean[39m[38;5;124m'[39m)) [38;5;241m*[39m[38;5;241m*[39m [38;5;241m2[39m

[0;31mModuleNotFoundError[0m: No module named 'numdifftools'

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
rotation = np.array([[0,0,1],
                  [1,0,0],
                  [0,1,0]])
# Visualize using the provided function
plot_3d_with_quiver(
    X_std @ V_hat.T[:X_hat.shape[1],:r] @ rotation,
    Y_std @ V_hat.T[:X_hat.shape[1],:r] @ rotation,
    t,
    arrow_size=1,
    title="3D S-Curve with General Derivatives (PCA Projection)",
)
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mValueError[0m                                Traceback (most recent call last)
Cell [0;32mIn[8], line 6[0m
[1;32m      1[0m rotation [38;5;241m=[39m np[38;5;241m.[39marray([[[38;5;241m0[39m,[38;5;241m0[39m,[38;5;241m1[39m],
[1;32m      2[0m                   [[38;5;241m1[39m,[38;5;241m0[39m,[38;5;241m0[39m],
[1;32m      3[0m                   [[38;5;241m0[39m,[38;5;241m1[39m,[38;5;241m0[39m]])
[1;32m      4[0m [38;5;66;03m# Visualize using the provided function[39;00m
[1;32m      5[0m plot_3d_with_quiver(
[0;32m----> 6[0m     [43mX_std[49m[43m [49m[38;5;241;43m@[39;49m[43m [49m[43mV_hat[49m[38;5;241;43m.[39;49m[43mT[49m[43m[[49m[43m:[49m[43mX_hat[49m[38;5;241;43m.[39;49m[43mshape[49m[43m[[49m[38;5;241;43m1[39;49m[43m][49m[43m,[49m[43m:[49m[43mr[49m[43m][49m [38;5;241m@[39m rotation,
[1;32m      7[0m     Y_std [38;5;241m@[39m V_hat[38;5;241m.[39mT[:X_hat[38;5;241m.[39mshape[[38;5;241m1[39m],:r] [38;5;241m@[39m rotation,
[1;32m      8[0m     t,
[1;32m      9[0m     arrow_size[38;5;241m=[39m[38;5;241m1[39m,
[1;32m     10[0m     title[38;5;241m=[39m[38;5;124m"[39m[38;5;124m3D S-Curve with General Derivatives (PCA Projection)[39m[38;5;124m"[39m,
[1;32m     11[0m )

[0;31mValueError[0m: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 3 is different from 100)

FAIL s_curve_linear_denoising.ipynb

