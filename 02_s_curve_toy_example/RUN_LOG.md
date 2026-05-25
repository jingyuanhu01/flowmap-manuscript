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
import numpy as np
import pandas as pd
from scripts.plotting import *
from scripts.denoising import *
from scripts.TPS import *
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[2], line 4[0m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mpandas[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mpd[39;00m
[1;32m      3[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mplotting[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[0;32m----> 4[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mdenoising[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[1;32m      5[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mTPS[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m

[0;31mModuleNotFoundError[0m: No module named 'scripts.denoising'

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
import numpy as np
import pandas as pd
from scripts.plotting import *
from scripts.denoising import *
from scripts.TPS import *
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[2], line 4[0m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mpandas[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mpd[39;00m
[1;32m      3[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mplotting[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[0;32m----> 4[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mdenoising[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[1;32m      5[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mTPS[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m

[0;31mModuleNotFoundError[0m: No module named 'scripts.denoising'

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
import numpy as np
import pandas as pd
from scripts.plotting import *
from scripts.denoising import *
from scripts.TPS import *
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[2], line 4[0m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mpandas[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mpd[39;00m
[1;32m      3[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mplotting[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[0;32m----> 4[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mdenoising[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[1;32m      5[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mTPS[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m

[0;31mModuleNotFoundError[0m: No module named 'scripts.denoising'

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
from scripts.TPS import *

tps = ThinPlateSpline(X_2d, n_control_points=500)
tps.fit(X_noisy, dof_target=30)
X_smoothed = tps.predict(X_2d)
plot_3d(X_smoothed,t)
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mTypeError[0m                                 Traceback (most recent call last)
Cell [0;32mIn[6], line 4[0m
[1;32m      1[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mTPS[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[1;32m      3[0m tps [38;5;241m=[39m ThinPlateSpline(X_2d, n_control_points[38;5;241m=[39m[38;5;241m500[39m)
[0;32m----> 4[0m [43mtps[49m[38;5;241;43m.[39;49m[43mfit[49m[43m([49m[43mX_noisy[49m[43m,[49m[43m [49m[43mdof_target[49m[38;5;241;43m=[39;49m[38;5;241;43m30[39;49m[43m)[49m
[1;32m      5[0m X_smoothed [38;5;241m=[39m tps[38;5;241m.[39mpredict(X_2d)
[1;32m      6[0m plot_3d(X_smoothed,t)

[0;31mTypeError[0m: ThinPlateSpline.fit() got an unexpected keyword argument 'dof_target'

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
jacobians_f = tps.compute_tps_jacobians(X_scipy)
jacobians_f.shape
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mAttributeError[0m                            Traceback (most recent call last)
Cell [0;32mIn[9], line 1[0m
[0;32m----> 1[0m jacobians_f [38;5;241m=[39m [43mtps[49m[38;5;241;43m.[39;49m[43mcompute_tps_jacobians[49m(X_scipy)
[1;32m      2[0m jacobians_f[38;5;241m.[39mshape

[0;31mAttributeError[0m: 'ThinPlateSpline' object has no attribute 'compute_tps_jacobians'

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
import numpy as np
import pandas as pd
from scripts.plotting import *
from scripts.denoising import *
from sklearn.preprocessing import StandardScaler
from scipy.linalg import svd
from scipy.spatial.distance import pdist, squareform, jaccard
from scipy.linalg import norm
------------------


[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[2], line 4[0m
[1;32m      2[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mpandas[39;00m[38;5;250m [39m[38;5;28;01mas[39;00m[38;5;250m [39m[38;5;21;01mpd[39;00m
[1;32m      3[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mplotting[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[0;32m----> 4[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mdenoising[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m [38;5;241m*[39m
[1;32m      5[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01msklearn[39;00m[38;5;21;01m.[39;00m[38;5;21;01mpreprocessing[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m StandardScaler
[1;32m      6[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscipy[39;00m[38;5;21;01m.[39;00m[38;5;21;01mlinalg[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m svd

[0;31mModuleNotFoundError[0m: No module named 'scripts.denoising'

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
import matplotlib.pyplot as plt
import umap.umap_ as umap
from sklearn.manifold import MDS
from sklearn.manifold import trustworthiness
from scipy.spatial.distance import cdist

from scripts.perturbation_distance import PerturbDistanceSolver
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="umap.umap_")

# ------------------------------------------------------------------------------
# Set up the solver & time-l2 operation
# ------------------------------------------------------------------------------
X_noise_std = 1e-3
Y_noise_std = 1e-3

X = X_gt + np.random.normal(scale=X_noise_std, size=X_gt.shape)
Y = Y_gt + np.random.normal(scale=Y_noise_std, size=Y_gt.shape)

# Standardize to mean 0, std 1
X = (X - X.mean(axis=0)) / X.std(axis=0)
Y = (Y - Y.mean(axis=0)) / Y.std(axis=0)

solver = PerturbDistanceSolver(X, Y)
t_dist = solver.pairwise_time_constrained_L2_distance()
neighbors = 20

# ------------------------------------------------------------------------------
# Define the range of betas on a log scale
# ------------------------------------------------------------------------------
alphas = np.logspace(-1, 2, 3)  # [0.01, ... , 1.0]
alphas = np.concatenate(([0], alphas))
dist_mat_sq = cdist(X, X, metric='sqeuclidean')

fig, axes = plt.subplots(nrows=len(alphas), ncols=2, figsize=(12, 4 * len(alphas)))
for i, alpha in enumerate(alphas):
    dist_mat = np.sqrt(dist_mat_sq + alpha * t_dist ** 2)
    
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    coords_mds = mds.fit_transform(dist_mat)
    
    trust_mds = trustworthiness(X_gt, coords_mds, n_neighbors=neighbors)
    jaccard_mds = jaccard_knn_similarity(X_gt, coords_mds, k=neighbors)
    ax_mds = axes[i, 0]  # left column for MDS
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
        min_dist = 0.6,
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

----- stderr -----
/Users/jh/micromamba/envs/flowmap-manuscript/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
------------------

[0;31m---------------------------------------------------------------------------[0m
[0;31mModuleNotFoundError[0m                       Traceback (most recent call last)
Cell [0;32mIn[5], line 7[0m
[1;32m      4[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01msklearn[39;00m[38;5;21;01m.[39;00m[38;5;21;01mmanifold[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m trustworthiness
[1;32m      5[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscipy[39;00m[38;5;21;01m.[39;00m[38;5;21;01mspatial[39;00m[38;5;21;01m.[39;00m[38;5;21;01mdistance[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m cdist
[0;32m----> 7[0m [38;5;28;01mfrom[39;00m[38;5;250m [39m[38;5;21;01mscripts[39;00m[38;5;21;01m.[39;00m[38;5;21;01mperturbation_distance[39;00m[38;5;250m [39m[38;5;28;01mimport[39;00m PerturbDistanceSolver
[1;32m      8[0m [38;5;28;01mimport[39;00m[38;5;250m [39m[38;5;21;01mwarnings[39;00m
[1;32m      9[0m warnings[38;5;241m.[39mfilterwarnings([38;5;124m"[39m[38;5;124mignore[39m[38;5;124m"[39m, category[38;5;241m=[39m[38;5;167;01mUserWarning[39;00m, module[38;5;241m=[39m[38;5;124m"[39m[38;5;124mumap.umap_[39m[38;5;124m"[39m)

[0;31mModuleNotFoundError[0m: No module named 'scripts.perturbation_distance'

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

