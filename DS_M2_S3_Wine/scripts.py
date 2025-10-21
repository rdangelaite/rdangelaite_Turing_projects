import seaborn as sns
import pandas as pd
import matplotlib.axes as axes


def outlier_f(data: pd.Series | pd.DataFrame, lower: bool = False, upper: bool = False) -> pd.Series | pd.DataFrame:
    '''
    Detecting if there are any outliers within 1.5IQR.
    We will use Tukey's rule to detect outliers, also known as IQR rule.
    First, we will calculate the Interquartile Range of the data:

    IQR = Q3 - Q1

    Q1 and Q3 stand for 25th and 75th percentiles.
    Later we determine our outlier boundaries with IQR:

    IQR_lower = Q1 - 1.5 * IQR
    IQR_upper = Q3 + 1.5 * IQR

    The data entered is meant to be Pandas dataframe or series.

    The function can also return only lowest or highest outliers if specified:
    - By default lower and upper are set to False, and the function returns
    both lower and upper outliers.
    - If lower is set to be true the function will return outliers below the
    lower boundary.
    - If upper is set to be true the function will return outliers above the
    upper boundary.
    - If both lower and upper are set to be true, the function will return
    both lower and upper outliers.
    '''

    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    # Boundaries
    IQR_lower = Q1 - 1.5 * IQR
    IQR_upper = Q3 + 1.5 * IQR

    if lower and not upper:
        mask = data < IQR_lower
        outliers = data[mask]

    elif upper and not lower:
        mask = data > IQR_upper
        outliers = data[mask]

    else:
        mask = (data < IQR_lower) | (data > IQR_upper)
        outliers = data[mask]

    return outliers


def histplot_f(
    data: pd.Series, color_mean: str = '#B8B3E9', color_median: str = '#7EDAF1', name: str = '', **kwargs
) -> axes.Axes:
    '''
    This is function to draw a histogram, with Seaborn library.
    It addition it also draws lines for mean and median.

    The function takes takes Pandas series as an argument.

    Optionally it is possible to choose colors for mean and median by entering
    color name or hexadecimal color code as a string,
    for example: color_mean = 'blue',  color_median = '#7EDAF1'.

    The name argument is the title for the graph and is also optional.

    The function returns axes
    '''
    ax = sns.histplot(data=data, **kwargs)
    if name:
        ax.set(title=name)
    ax.axvline(x=data.mean(), color=color_mean, label='Mean')
    ax.axvline(x=data.median(), color=color_median, label='Median')
    ax.legend(loc='upper right', edgecolor='none')
    ax.grid(axis='y', linestyle='--')
    return ax
