# pydhi
Facilitate creating, reading and writing dfs0, dfs2, dfs1 and dfs3 files. Reading Res1D data.

## Install package from the dist directory:
	pythonnet - https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonnet
        pip install py_dhi_xxx.whl

	% Assumes MIKE installed already on the computer. Add install directory to PYTHONPATH from windows command line:
	% set PYTHONPATH=%PYTHONPATH%;"C:\Program Files (x86)\DHI\2019\bin\x64"

# Examples

## Reading dfs0 file into Pandas DataFrame
```python
from pydhi import dfs0 as dfs0
dfs = dfs0.dfs0()
ts = dfs.read_to_pandas(dfs0file)
```

## Create non-equidistant dfs0
```python
dfs0file = r'C:\test\randomEQC.dfs0'
data = np.random.random([1000, 2])
data[2, :] = np.nan
start_time = datetime.datetime(2017, 1, 1)
time_vector = []
for i in range(1000):
	time_vector.append( start_time + datetime.timedelta(hours=i*0.1) )
title = 'Hello Test'
names = ['VarFun01', 'NotFun']
variable_type = [100000, 100000]
unit = [1000, 1000]
data_value_type = [0, 1]

dfs = dfs0.dfs0()
dfs.create_non_equidistant_calendar(dfs0file=dfs0file, data=data, time_vector=time_vector,
				    names=names, title=title, variable_type=variable_type, unit=unit,
				    data_value_type=data_value_type)
```

## Create equidistant dfs0
```python
dfs0file = r'C:\test\randomEQC.dfs0'
data = np.random.random([1000, 2])
data[2, :] = np.nan
start_time = datetime.datetime(2017, 1, 1)
timeseries_unit = 1402
title = 'Hello Test'
names = ['VarFun01', 'NotFun']
variable_type = [100000, 100000]
unit = [1000, 1000]
data_value_type = [0, 1]
dt = 5
dfs = dfs0.dfs0()
dfs.create_equidistant_calendar(dfs0file=dfs0file, data=data, start_time=start_time,
				timeseries_unit=timeseries_unit, dt=dt, names=names,
				title=title, variable_type=variable_type, unit=unit,
				data_value_type=data_value_type)
```

## Read dfs2 data
```python
dfs2File = r"C:\test\random.dfs2"
dfs = dfs2.dfs2()
data = dfs.read(dfs2File, [0])[0]
data = data[0]
```

For a complete example of conversion from netcdf to dfs2 see this [notebook](notebooks/Sea surface temperature - dfs2.ipynb)

## DFS Utilities to query variable type, time series types (useful when creating a new dfs file)
```python
dfsUtil = dfs_util.dfs_util()
dfsUtil.type_list()
dfsUtil.timestep_list()
```

## Read Res1D file Return Pandas DataFrame
```python
import res1d as r1d
p1 = r1d.ExtractionPoint()
p1.BranchName  = 'branch1'
p1.Chainage = 10.11
p1.VariableType  = 'Discharge'
ts = r1d.read('res1dfile.res1d', [p1])
```

## Read dfsu files
```python
import matplotlib.pyplot as plt
import pydhi

dfs = pydhi.dfsu.dfsu()

filename = "HD.dfsu"
(d,t,n)= dfs.read(filename,[0])

idx = dfs.find_closest_element_index(x=608000, y=6907000)

plt.plot(t,d[0][idx,:])
```
![Timeseries](images/dfsu_ts.png)

# Created by Marc-Etienne Ridler (mer@dhigroup.com)
python setup.py sdist bdist_wheel

