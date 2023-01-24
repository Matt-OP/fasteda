# fasteda

A python module that provides a quick way to overview a DataFrame.


```python
!pip install fasteda

from fasteda import fast_eda

def fast_eda(df, target=None, correlation=True, pairplot=True, hist_box_plot=True, countplot=True):
```

### New in 1.0.1

- Added median, skewness and kurtosis to DataFrame Describe
- In Histplot(s) & Boxplot(s), when target variable is binary, boxplot(s) will now display 2 seperate boxes representing each class
- Improved visual presentation
- Fixed small visual issues when examining different types of datasets

Parameters:

- `df`: DataFrame | dataset for plotting.

- `target`: string, optional | target variable of (binary) classification dataset, works best with 2 classes (not recommended when there are > 3 classes). Enables hue of target variable in pairplot and hist_box_plot.

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
