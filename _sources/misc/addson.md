# Other libraries of interest

```{figure} ../_static/NCI.png
---
figclass: margin
name: margin_launch
---
```

Part of the following librairies address an incresingly common problem: *what happens if the data we wish to analyze is “big data”?*

We learned how to use `Numpy`, `Pandas`, and `Xarray` to analyze various types of environmental data. There are obviously many others useful libraries, especially when it comes to **Big data**.

:::{note}
**Big data** is data sets that are so voluminous and complex that traditional data processing application software are inadequate to deal with them.
:::

By this definition, most of the dataset we are regularly confronted to in environmental science (actually *in Earth science more generally*) are big data.


## Faster array manipulation


```{figure} ../_static/daskzarr.png
:scale: 30%
```



````{panels}
:column: col-6
:card: border-2
**[DASK](https://dask.org)**
^^^
**Dask** provides advanced parallelism for analytics. It is developed in coordination with other community projects like NumPy, pandas, and scikit-learn.
---
**[Zarr](https://zarr.readthedocs.io/en/stable/)**
^^^
**Zarr** is a format for the storage of chunked, compressed, N-dimensional arrays that depends on Numpy.
````

## Data loading libraries


````{panels}
:column: col-6
:card: border-2
**[Intake](https://intake.readthedocs.io/en/latest/)**
^^^
**Intake** is a lightweight set of tools for loading and sharing data in data science projects.
---
**[Siphon](https://unidata.github.io/siphon/latest/index.html)**
^^^
Siphon allows efficient access to Unidata data hosted on a THREDDS Data Server.
````


## NCI examples

+ A useful overview of the National Computing Infrastructure data collection and services can be found [here](https://nci-data-training.readthedocs.io/en/latest/_notebook/tds/THREDDS_WMS.html?highlight=ereefs#In-this-notebook:). Series of Jupyter notebooks [examples](https://nci-data-training.readthedocs.io/en/latest/index.html) are provided.

+ [NCI Dask](https://opus.nci.org.au/display/Help/examples-dask) themed notebook tutorials demonstrate how to use Dask on data collections hosted at the NCI as well as data extracted from external databases (especially for eReefs models one can look at the following `Dask_13_intensive_calculation_eReef.ipynb` notebook).

+ [NCI THREDDS](https://opus.nci.org.au/display/Help/examples-thredds) demonstrate how to access data stored on NCI's THREDDS Data Server using Jupyter notebooks.
