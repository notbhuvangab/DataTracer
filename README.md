
# DataTracer

Data Lineage Tracing Library

* License: [MIT](https://github.com/data-dev/DataTracer/blob/master/LICENSE)
## Overview

DataTracer is a Python library for solving Data Lineage problems using statistical
methods, machine learning techniques, and hand-crafted heuristics.

Currently the Data Tracer library implements discovery of the following properties:

* **Primary Key**: Identify which column is the primary key in each table.
* **Foreign Key**: Find which relationships exist between the tables.
* **Column Mapping**: Given a field in a table, deduce which other fields, from the same table
  or other tables, are more related or contributed the most in generating the given field.


**DataTracer** has been developed and tested on [Python 3.5 and 3.6, 3.7](https://www.python.org/downloads/)

## Install with pip

The easiest and recommended way to install **DataTracer** is using [pip](
https://pip.pypa.io/en/stable/):

```bash
pip install datatracer
```

# Data Format: Datasets and Metadata

The DataTracer library is prepared to work using datasets, which are a collection of tables
loaded as `pandas.DataFrames` and a MetaData JSON which provides information about the
dataset structure.


Then run app.py using 

```bash
python -m edifice app.py app 
```

It should show up visualization of posts dataset, identifying its primary,foreign keys and column mappings.
The UI wrapper used is pyedifice.

-Bhuvan Gabbita
-Lokesh Menga