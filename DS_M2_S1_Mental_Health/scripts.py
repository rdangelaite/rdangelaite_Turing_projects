import seaborn as sns
import pandas as pd
import matplotlib.axes as axes
import matplotlib as plt
from typing import Optional


def count_percentage(value: float, total: float, round_value: int = 2) -> float:
    '''
    Function to count % of a value.
    '''
    return round(value / total * 100, round_value)


def bar_plot_f(data: pd.Series, name: str, total: float, palet: str, **kwargs) -> axes.Axes:
    '''
    Function to draw Seaborn barplot easier.
    It has % on bar labels together with instances count.
    '''
    ax = sns.barplot(x=data.index, y=data, palette=palet, **kwargs)
    ax.set_title(name)
    ax.set_xticklabels(labels=data.index, fontsize=9, alpha=0.8)
    labels_list = []
    for i in range(len(data)):
        labels_list.append(f'{data.iloc[i]} ({count_percentage(data.iloc[i], total)}%)')
    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    return ax


def outlier_f(data: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
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
    '''
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    # Boundaries
    IQR_lower = Q1 - 1.5 * IQR
    IQR_upper = Q3 + 1.5 * IQR

    mask = (data < IQR_lower) | (data > IQR_upper)
    outliers = data[mask]
    return outliers


def df_from_multiindex(s_multi: pd.Series, new_index: str, filling: int = 0) -> pd.DataFrame:
    '''
    Takes a multi index series made by grouping patients data on multiple
    value counts. Returns a df used to draw a graph.

    By default fills nan values with 0

    This was created as a helper function to draw bar plot using a multiindex
    pandas series.
    '''
    df = s_multi.unstack().fillna(filling).stack().reset_index().set_index(new_index)
    return df


def bar_plot_multi_index_f(data: pd.Series, x: str, hue: str, name: str, palet: str, **kwargs) -> axes.Axes:
    '''
    This is a function made to draw a graph from pandas multi series
    index. It takes one of the indexes as x and another one as hue.
    '''
    df = df_from_multiindex(data, x)
    ax = sns.barplot(df, x=df.index, y=df.iloc[:, 1], palette=palet, hue=hue, **kwargs)
    ax.set_title(name)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=9, alpha=0.8)

    things = df[hue].unique()
    # iterating through bars with different hue
    for j in range(len(ax.containers)):
        labels_list = []
        # selecting only values for that group of bars according to hue
        mask = df[hue] == things[j]
        temporary = df[mask].iloc[:, 1]
        # calculating sum of different populations according to hue
        total = sum(temporary)
        # creation of bar labels only for columns with selected hue
        for i in range(len(temporary)):
            labels_list.append(f'{temporary.iloc[i]} ({count_percentage(temporary.iloc[i], total)}%)')
        ax.bar_label(ax.containers[j], labels=labels_list, fontsize=9)

    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    plt.pyplot.legend(loc='upper left', bbox_to_anchor=(1, 1), title='', frameon=False)
    return ax
