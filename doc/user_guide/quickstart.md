# PyMultiFracs quickstart

## The ``xarray`` structure

The output of multifractal analysis in pymultifracs are instances of the {class}`xarray.DataArray` class.

The ``DataArray`` structure is a wrapper around numpy's ndarrays, that labels the dimensions, and may additionally provide coordinates for those dimensions. Internally, this is done to make sure that dimensions are properly aligned when applying operations.
This also means that the output arrays are immediatly interpretable, since the meaning of each dimension, and where relevant, the coordinates of the dimensions are provided along with the input.

``xarray`` can be thought of as extending the pandas dataframe approach, which is limited to 2D arrays, to a N-dimensional setting.

### Indexing data arrays

DataArrays provide a simple interface to select a particular entry by specifying the dimension by name. For instance, if ``pwt`` is the output of {func}`~pymultifracs.mfa`, the value of $C_2(3)$ can be obtained with the {meth}`~xarray.DataArray.sel` method:

```python
pwt.cumulants.values.sel(j=3, m=2)
```

To instead take $C_2(j)$ for j between $2$ and $8$, slicing with `np.s_` may be used:

```python
pwt.cumulants.values.sel(j=np.s_[2:8], m=2)
```

On dimensions where there are no coordinates, the {meth}`~xarra.DataArray.isel` method may be used to select by position.
For instance, if a 2D array was provided as input to {func}`~pymultifracs.wavelet_analysis`, then the $c_2$ estimate for the second entry can be obtained by:

```python
pwt.cumulants.c2.isel(channel=1)
```

For further details, please refer to the [xarray documentation](https://docs.xarray.dev/en/latest/user-guide/indexing.html)

### Quick plotting

On top of the more detailed plotting functions provided by the pymultifracs package, the contents of xarrays may be plotted using their {meth}`~xarray.DataArray.plot` method.

As an example, plotting the average structure function $S_2(j)$ across all channels and $j$ in the range $[2, 8]$ is as simple as:

```python
pwt.structure.values.sel(q=2, j=np.s_[2:8]).mean(dim='channel').plot()
```
