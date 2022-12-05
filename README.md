# fasteda

A python module that provides a quick way to overview a DataFrame.

#### `!pip install fasteda`

#### `from fasteda import fast_eda`

#### `def fast_eda(df, target=None, correlation=True, pairplot=True, hist_box_plot=True, countplot=True):`

Parameters:

- `df`: DataFrame | dataset for plotting.

- `target`: string, optional | target variable of multi-class classification dataset, works best with < 4 classes. Enables hue of target variable in pairplot and hist_box_plot.

- `correlation`: bool, optional | Enable/disable correlation plot

- `pairplot`: bool, optional | Enable/disable pairplot

- `hist_box_plot`: bool, optional | Enable/disable hist_box_plot

- `countplot`: bool, optional | Enable/disable countplot

#### Outputs:

- Head
- Tail
- Missing values count
- MSNO Matrix
- Shape
- Info
- Describe
- Correlation
- Pairplot
- Histplot(s) & Boxplot(s) subplot
- Countplot(s)

#### Example output on the Titanic dataset: https://www.kaggle.com/code/mattop/example-output-of-fasteda-on-titanic-dataset
