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
[0;31mValueError[0m                                Traceback (most recent call last)
Cell [0;32mIn[7], line 1[0m
[0;32m----> 1[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      2[0m metrics

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:465[0m, in [0;36mThinPlateSpline.evaluate_fit[0;34m(self, X, Y)[0m
[1;32m    463[0m         [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m"[39m[38;5;124mY must be provided when the TPS model has no stored training target.[39m[38;5;124m"[39m)
[1;32m    464[0m     Y [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mY_train
[0;32m--> 465[0m Y_pred [38;5;241m=[39m [38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mpredict[49m[43m([49m[43mX[49m[43m)[49m
[1;32m    466[0m N, D [38;5;241m=[39m Y[38;5;241m.[39mshape
[1;32m    468[0m RSS [38;5;241m=[39m np[38;5;241m.[39msum((Y [38;5;241m-[39m Y_pred) [38;5;241m*[39m[38;5;241m*[39m [38;5;241m2[39m, axis[38;5;241m=[39m[38;5;241m0[39m)

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:250[0m, in [0;36mThinPlateSpline.predict[0;34m(self, X_new)[0m
[1;32m    247[0m was_1d [38;5;241m=[39m (X_new[38;5;241m.[39mshape[[38;5;241m0[39m] [38;5;241m==[39m [38;5;241m1[39m [38;5;129;01mand[39;00m X_new[38;5;241m.[39mshape[[38;5;241m1[39m] [38;5;241m==[39m [38;5;28mself[39m[38;5;241m.[39mcontrol_points[38;5;241m.[39mshape[[38;5;241m1[39m])
[1;32m    249[0m [38;5;66;03m# Compute the kernel matrix between new inputs and the control points.[39;00m
[0;32m--> 250[0m pairwise_distances [38;5;241m=[39m [43mcdist[49m[43m([49m[43mX_new[49m[43m,[49m[43m [49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mcontrol_points[49m[43m,[49m[43m [49m[43mmetric[49m[38;5;241;43m=[39;49m[38;5;124;43m"[39;49m[38;5;124;43meuclidean[39;49m[38;5;124;43m"[39;49m[43m)[49m
[1;32m    251[0m K_new [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mtps_kernel(pairwise_distances)
[1;32m    253[0m [38;5;66;03m# Build the affine term for the new inputs.[39;00m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/scipy/spatial/distance.py:3108[0m, in [0;36mcdist[0;34m(XA, XB, metric, out, **kwargs)[0m
[1;32m   3106[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXB must be a 2-dimensional array.[39m[38;5;124m'[39m)
[1;32m   3107[0m [38;5;28;01mif[39;00m s[[38;5;241m1[39m] [38;5;241m!=[39m sB[[38;5;241m1[39m]:
[0;32m-> 3108[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXA and XB must have the same number of columns [39m[38;5;124m'[39m
[1;32m   3109[0m                      [38;5;124m'[39m[38;5;124m(i.e. feature dimension.)[39m[38;5;124m'[39m)
[1;32m   3111[0m mA [38;5;241m=[39m s[[38;5;241m0[39m]
[1;32m   3112[0m mB [38;5;241m=[39m sB[[38;5;241m0[39m]

[0;31mValueError[0m: XA and XB must have the same number of columns (i.e. feature dimension.)

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
[0;31mValueError[0m                                Traceback (most recent call last)
Cell [0;32mIn[6], line 3[0m
[1;32m      1[0m tps [38;5;241m=[39m ThinPlateSpline(X_2d, n_control_points[38;5;241m=[39m[38;5;241m1000[39m)
[1;32m      2[0m tps[38;5;241m.[39mfit(X, dof_target[38;5;241m=[39m[38;5;241m50[39m)
[0;32m----> 3[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      4[0m metrics

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:465[0m, in [0;36mThinPlateSpline.evaluate_fit[0;34m(self, X, Y)[0m
[1;32m    463[0m         [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m"[39m[38;5;124mY must be provided when the TPS model has no stored training target.[39m[38;5;124m"[39m)
[1;32m    464[0m     Y [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mY_train
[0;32m--> 465[0m Y_pred [38;5;241m=[39m [38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mpredict[49m[43m([49m[43mX[49m[43m)[49m
[1;32m    466[0m N, D [38;5;241m=[39m Y[38;5;241m.[39mshape
[1;32m    468[0m RSS [38;5;241m=[39m np[38;5;241m.[39msum((Y [38;5;241m-[39m Y_pred) [38;5;241m*[39m[38;5;241m*[39m [38;5;241m2[39m, axis[38;5;241m=[39m[38;5;241m0[39m)

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:250[0m, in [0;36mThinPlateSpline.predict[0;34m(self, X_new)[0m
[1;32m    247[0m was_1d [38;5;241m=[39m (X_new[38;5;241m.[39mshape[[38;5;241m0[39m] [38;5;241m==[39m [38;5;241m1[39m [38;5;129;01mand[39;00m X_new[38;5;241m.[39mshape[[38;5;241m1[39m] [38;5;241m==[39m [38;5;28mself[39m[38;5;241m.[39mcontrol_points[38;5;241m.[39mshape[[38;5;241m1[39m])
[1;32m    249[0m [38;5;66;03m# Compute the kernel matrix between new inputs and the control points.[39;00m
[0;32m--> 250[0m pairwise_distances [38;5;241m=[39m [43mcdist[49m[43m([49m[43mX_new[49m[43m,[49m[43m [49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mcontrol_points[49m[43m,[49m[43m [49m[43mmetric[49m[38;5;241;43m=[39;49m[38;5;124;43m"[39;49m[38;5;124;43meuclidean[39;49m[38;5;124;43m"[39;49m[43m)[49m
[1;32m    251[0m K_new [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mtps_kernel(pairwise_distances)
[1;32m    253[0m [38;5;66;03m# Build the affine term for the new inputs.[39;00m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/scipy/spatial/distance.py:3108[0m, in [0;36mcdist[0;34m(XA, XB, metric, out, **kwargs)[0m
[1;32m   3106[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXB must be a 2-dimensional array.[39m[38;5;124m'[39m)
[1;32m   3107[0m [38;5;28;01mif[39;00m s[[38;5;241m1[39m] [38;5;241m!=[39m sB[[38;5;241m1[39m]:
[0;32m-> 3108[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXA and XB must have the same number of columns [39m[38;5;124m'[39m
[1;32m   3109[0m                      [38;5;124m'[39m[38;5;124m(i.e. feature dimension.)[39m[38;5;124m'[39m)
[1;32m   3111[0m mA [38;5;241m=[39m s[[38;5;241m0[39m]
[1;32m   3112[0m mB [38;5;241m=[39m sB[[38;5;241m0[39m]

[0;31mValueError[0m: XA and XB must have the same number of columns (i.e. feature dimension.)

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
[0;31mValueError[0m                                Traceback (most recent call last)
Cell [0;32mIn[6], line 3[0m
[1;32m      1[0m tps [38;5;241m=[39m ThinPlateSpline(X_2d, n_control_points[38;5;241m=[39m[38;5;241m1000[39m)
[1;32m      2[0m tps[38;5;241m.[39mfit(X, dof_target[38;5;241m=[39m[38;5;241m50[39m)
[0;32m----> 3[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX[49m[43m)[49m
[1;32m      4[0m metrics

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:465[0m, in [0;36mThinPlateSpline.evaluate_fit[0;34m(self, X, Y)[0m
[1;32m    463[0m         [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m"[39m[38;5;124mY must be provided when the TPS model has no stored training target.[39m[38;5;124m"[39m)
[1;32m    464[0m     Y [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mY_train
[0;32m--> 465[0m Y_pred [38;5;241m=[39m [38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mpredict[49m[43m([49m[43mX[49m[43m)[49m
[1;32m    466[0m N, D [38;5;241m=[39m Y[38;5;241m.[39mshape
[1;32m    468[0m RSS [38;5;241m=[39m np[38;5;241m.[39msum((Y [38;5;241m-[39m Y_pred) [38;5;241m*[39m[38;5;241m*[39m [38;5;241m2[39m, axis[38;5;241m=[39m[38;5;241m0[39m)

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:250[0m, in [0;36mThinPlateSpline.predict[0;34m(self, X_new)[0m
[1;32m    247[0m was_1d [38;5;241m=[39m (X_new[38;5;241m.[39mshape[[38;5;241m0[39m] [38;5;241m==[39m [38;5;241m1[39m [38;5;129;01mand[39;00m X_new[38;5;241m.[39mshape[[38;5;241m1[39m] [38;5;241m==[39m [38;5;28mself[39m[38;5;241m.[39mcontrol_points[38;5;241m.[39mshape[[38;5;241m1[39m])
[1;32m    249[0m [38;5;66;03m# Compute the kernel matrix between new inputs and the control points.[39;00m
[0;32m--> 250[0m pairwise_distances [38;5;241m=[39m [43mcdist[49m[43m([49m[43mX_new[49m[43m,[49m[43m [49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mcontrol_points[49m[43m,[49m[43m [49m[43mmetric[49m[38;5;241;43m=[39;49m[38;5;124;43m"[39;49m[38;5;124;43meuclidean[39;49m[38;5;124;43m"[39;49m[43m)[49m
[1;32m    251[0m K_new [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mtps_kernel(pairwise_distances)
[1;32m    253[0m [38;5;66;03m# Build the affine term for the new inputs.[39;00m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/scipy/spatial/distance.py:3108[0m, in [0;36mcdist[0;34m(XA, XB, metric, out, **kwargs)[0m
[1;32m   3106[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXB must be a 2-dimensional array.[39m[38;5;124m'[39m)
[1;32m   3107[0m [38;5;28;01mif[39;00m s[[38;5;241m1[39m] [38;5;241m!=[39m sB[[38;5;241m1[39m]:
[0;32m-> 3108[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXA and XB must have the same number of columns [39m[38;5;124m'[39m
[1;32m   3109[0m                      [38;5;124m'[39m[38;5;124m(i.e. feature dimension.)[39m[38;5;124m'[39m)
[1;32m   3111[0m mA [38;5;241m=[39m s[[38;5;241m0[39m]
[1;32m   3112[0m mB [38;5;241m=[39m sB[[38;5;241m0[39m]

[0;31mValueError[0m: XA and XB must have the same number of columns (i.e. feature dimension.)

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
[0;31mValueError[0m                                Traceback (most recent call last)
Cell [0;32mIn[14], line 22[0m
[1;32m     20[0m [38;5;28mprint[39m([38;5;124mf[39m[38;5;124m"[39m[38;5;124mRunning with dof: [39m[38;5;132;01m{[39;00mdof_target[38;5;132;01m:[39;00m[38;5;124m.2f[39m[38;5;132;01m}[39;00m[38;5;124m"[39m)
[1;32m     21[0m tps[38;5;241m.[39mfit(X_noisy, dof_target[38;5;241m=[39mdof_target)
[0;32m---> 22[0m metrics [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mevaluate_fit[49m[43m([49m[43mX_noisy[49m[43m)[49m
[1;32m     24[0m [38;5;66;03m# Compute RMSE with ground truth[39;00m
[1;32m     25[0m X_smoothed [38;5;241m=[39m tps[38;5;241m.[39mpredict(X_2d)

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:465[0m, in [0;36mThinPlateSpline.evaluate_fit[0;34m(self, X, Y)[0m
[1;32m    463[0m         [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m"[39m[38;5;124mY must be provided when the TPS model has no stored training target.[39m[38;5;124m"[39m)
[1;32m    464[0m     Y [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mY_train
[0;32m--> 465[0m Y_pred [38;5;241m=[39m [38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mpredict[49m[43m([49m[43mX[49m[43m)[49m
[1;32m    466[0m N, D [38;5;241m=[39m Y[38;5;241m.[39mshape
[1;32m    468[0m RSS [38;5;241m=[39m np[38;5;241m.[39msum((Y [38;5;241m-[39m Y_pred) [38;5;241m*[39m[38;5;241m*[39m [38;5;241m2[39m, axis[38;5;241m=[39m[38;5;241m0[39m)

File [0;32m~/Projects/flowmap_code_by_dataset/03_s_curve_tps_geometry/source_vector_field_visualization/scripts/TPS.py:250[0m, in [0;36mThinPlateSpline.predict[0;34m(self, X_new)[0m
[1;32m    247[0m was_1d [38;5;241m=[39m (X_new[38;5;241m.[39mshape[[38;5;241m0[39m] [38;5;241m==[39m [38;5;241m1[39m [38;5;129;01mand[39;00m X_new[38;5;241m.[39mshape[[38;5;241m1[39m] [38;5;241m==[39m [38;5;28mself[39m[38;5;241m.[39mcontrol_points[38;5;241m.[39mshape[[38;5;241m1[39m])
[1;32m    249[0m [38;5;66;03m# Compute the kernel matrix between new inputs and the control points.[39;00m
[0;32m--> 250[0m pairwise_distances [38;5;241m=[39m [43mcdist[49m[43m([49m[43mX_new[49m[43m,[49m[43m [49m[38;5;28;43mself[39;49m[38;5;241;43m.[39;49m[43mcontrol_points[49m[43m,[49m[43m [49m[43mmetric[49m[38;5;241;43m=[39;49m[38;5;124;43m"[39;49m[38;5;124;43meuclidean[39;49m[38;5;124;43m"[39;49m[43m)[49m
[1;32m    251[0m K_new [38;5;241m=[39m [38;5;28mself[39m[38;5;241m.[39mtps_kernel(pairwise_distances)
[1;32m    253[0m [38;5;66;03m# Build the affine term for the new inputs.[39;00m

File [0;32m~/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/scipy/spatial/distance.py:3108[0m, in [0;36mcdist[0;34m(XA, XB, metric, out, **kwargs)[0m
[1;32m   3106[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXB must be a 2-dimensional array.[39m[38;5;124m'[39m)
[1;32m   3107[0m [38;5;28;01mif[39;00m s[[38;5;241m1[39m] [38;5;241m!=[39m sB[[38;5;241m1[39m]:
[0;32m-> 3108[0m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m([38;5;124m'[39m[38;5;124mXA and XB must have the same number of columns [39m[38;5;124m'[39m
[1;32m   3109[0m                      [38;5;124m'[39m[38;5;124m(i.e. feature dimension.)[39m[38;5;124m'[39m)
[1;32m   3111[0m mA [38;5;241m=[39m s[[38;5;241m0[39m]
[1;32m   3112[0m mB [38;5;241m=[39m sB[[38;5;241m0[39m]

[0;31mValueError[0m: XA and XB must have the same number of columns (i.e. feature dimension.)

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

## s_curve_perturbation_distance.ipynb
[NbConvertApp] Converting notebook s_curve_perturbation_distance.ipynb to notebook
[NbConvertApp] Writing 4525057 bytes to s_curve_perturbation_distance.ipynb
PASS s_curve_perturbation_distance.ipynb

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
import cvxpy as cp

# Dummy vectors (change to your actual data)
i = 0
j = 1
x1 = X[i,:]
x2 = X[j,:]
v1 = Y[i,:]
v2 = Y[j,:]
c = 0.5  # L2 constraint on [t1, t2]

# Variables
t1 = cp.Variable()
t2 = cp.Variable()

# Objective: minimize norm squared
residual = x1 + t1 * v1 - x2 - t2 * v2
objective = cp.Minimize(cp.sum_squares(residual))

# Constraint: L2 norm of (t1, t2) ≤ c
constraints = [cp.norm(cp.hstack([t1, t2]), 2) <= c]

# Problem
prob = cp.Problem(objective, constraints)
prob.solve()

# Output
print("Optimal t1:", t1.value)
print("Optimal t2:", t2.value)
print("Objective value:", prob.value)
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[2], line 1[0m
[0;32m----> 1[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mcvxpy[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mcp[39;00m
[1;32m      3[0m [38;5;66;03m# Dummy vectors (change to your actual data)[39;00m
[1;32m      4[0m i [38;5;241m=[39m [38;5;241m0[39m

[0;31mModuleNotFoundError[0m: No module named 'cvxpy'

FAIL s_curve_perturbation_distance_validation.ipynb

