import seaborn as sns
import pandas as pd
import matplotlib.axes as axes
from scipy import stats


def count_percentage(value: float, total: float, round_value: int = 2) -> float:
    """
    Function to count % of a value.

    The first value entered is number of part total we are interested.
    The second is the total or the whole.

    By default rounds values up to hundredths.

    The function then divides the part by the whole and multiplies by 100.
    Returns the result.
    """
    return round(value / total * 100, round_value)


def bar_plot_f_perc(data: pd.Series, name: str = '', **kwargs) -> axes.Axes:
    """
    Function to draw Seaborn barplot easier.
    It has % on bar labels together with instances count.
    The % is calculated by taking a value for a category and dividing it by
    total number of instances.

    The function takes Pandas series as an argument.

    The name argument is the title for the graph and is optional.

    The function returns axes.
    """
    ax = sns.barplot(x=data.index, y=data, **kwargs)
    ax.set_title(name)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(labels=data.index, fontsize=9, alpha=0.8)
    labels_list = []
    total = data.sum()
    for i in range(len(data)):
        labels_list.append(f"{data.iloc[i]} ({count_percentage(data.iloc[i], total)}%)")
    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    sns.despine(left=True, bottom=True)
    return ax


def df_from_multiindex(s_multi: pd.Series, new_index: str, filling: int = 0) -> pd.DataFrame:
    '''
    Takes a multi index series made by grouping targets data on multiple
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
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=9, alpha=0.8)

    indexes = df.index.unique()
    labels_list = []
    # iterating through bars with different indexes
    for j in range(len(indexes)):
        # selecting only values for that group according to index
        temporary = df.loc[indexes[j]].iloc[:, 1]
        # calculating sum of different populations according to index
        total = sum(temporary)
        # creation of bar labels only for columns with selected index
        for i in range(len(temporary)):
            labels_list.append(f'{temporary.iloc[i]} ({count_percentage(temporary.iloc[i], total)}%)')

    # adding correct labels for groups
    for j in range(len(ax.containers)):
        mylist = [j + i * 2 for i in range(int(len(labels_list) / 2))]
        labels = [labels_list[i] for i in mylist]
        ax.bar_label(ax.containers[j], labels=labels, fontsize=9)

    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    sns.despine(left=True, bottom=True)
    return ax


def simple_histplot(data: pd.DataFrame, x: str, xlabel: str = '', **kwargs) -> axes.Axes:
    '''
    This is function to draw a histogram, with Seaborn library.
    The function takes Pandas data frame and x as a string as arguments.

    Optionally it is possible to choose name for x axis.

    The function returns axes.
    '''
    ax = sns.histplot(data=data, x=x, **kwargs)
    if xlabel:
        ax.set(xlabel=xlabel)
    ax.grid(axis='y', linestyle='--')
    return ax


def histplot_f(
    data: pd.Series, color_mean: str = '#B8B3E9', color_median: str = '#7EDAF1', name: str = '', **kwargs
) -> axes.Axes:
    '''
    This is function to draw a histogram, with Seaborn library.
    It addition it also draws lines for mean and median.

    The function takes Pandas series as an argument.

    Optionally it is possible to choose colors for mean and median by entering
    color name or hexadecimal color code as a string,
    for example: color_mean = 'blue',  color_median = '#7EDAF1'.

    The name argument is the title for the graph and is also optional.

    The function returns axes.
    '''
    ax = sns.histplot(data=data, **kwargs)
    if name:
        ax.set(title=name)
    ax.axvline(x=data.mean(), color=color_mean, label='Mean')
    ax.axvline(x=data.median(), color=color_median, label='Median')
    ax.legend(loc='upper right', edgecolor='none')
    ax.grid(axis='y', linestyle='--')
    return ax


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


def hyphotesis_tests_f(x: pd.Series, y: pd.Series, p: float = 0.05, name_x: str = '', name_y: str = '') -> None:
    '''
    This function takes two populations for statistical comparison and prints
    95% confidence intervals and if they overlap,
    t test, Mann–Whitney U test and Median test and their results.

    It needs two panda series as argument.
    Significance value by default is set to 0.05, but can be changed.
    Confidence intervals can be named according to taken datasets for clarity.
    '''

    print('95% confidence intervals:')
    print()
    print(name_x)
    conf_int_x = stats.t.interval(0.95, df=len(x) - 1, loc=x.mean(), scale=x.sem())
    print(conf_int_x)

    print(name_y)
    conf_int_y = stats.t.interval(0.95, df=len(y) - 1, loc=y.mean(), scale=y.sem())
    print(conf_int_y)
    conf_int_x = pd.Interval(conf_int_x[0], conf_int_x[1])
    conf_int_y = pd.Interval(conf_int_y[0], conf_int_y[1])
    overlap = conf_int_x.overlaps(conf_int_y)
    if overlap:
        print('Intervals overlap.')
    else:
        print('Invervals do not overlap.')
    print()

    print(f'Set p value is {p}.')
    print()

    ttest = stats.ttest_ind(x, y)
    print(ttest)
    if ttest[1] < p:
        print('t test results are statistically significant')
    else:
        print('t test results are not statistically significant')
    print()

    mwtest = stats.mannwhitneyu(x, y)
    print(mwtest)
    if mwtest[1] < p:
        print('Mann–Whitney U test results are statistically significant')
    else:
        print('Mann–Whitney U test results are not statistically significant')
    print()

    mtest = stats.median_test(x, y)
    print(mtest)
    if mtest[1] < p:
        print('Median test results are statistically significant')
    else:
        print('Median test results are not statistically significant')

    return None
