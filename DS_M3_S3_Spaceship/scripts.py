import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.axes as axes
from typing import Dict, Any
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_predict
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
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


def bar_plot_multi_index_f(
    data: pd.Series, x: str, hue: str, name: str, palet: str, rotation: int = 0, **kwargs
) -> axes.Axes:
    '''
    This is a function made to draw a graph from pandas multi series
    index. It takes one of the indexes as x and another one as hue.

    It also has option to rotate bar annotations.
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
        ax.bar_label(ax.containers[j], labels=labels, fontsize=9, rotation=rotation)

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


def hypothesis_tests_f(
    x: pd.Series, y: pd.Series, p: float = 0.05, name_x: str = '', name_y: str = '', test: list = ['t']
) -> None:
    '''
    This function takes two populations for statistical comparison and prints
    95% confidence intervals and if they overlap and a statistical test.

    By default the function returns t test, however it can be set to return
    Mann–Whitney U test and Median test and their results, by entering a list
    with desired tests as an argument to the function:
    - to get t test the default the list is set to ['t']
    - to get Mann–Whitney U, the list should be set to ['mw']
    - to get Median test - ['m']
    - to get all of the tests set the list to ['t', 'mw', 'm']

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
        print('Intervals do not overlap.')
    print()

    print(f'Set p value is {p}.')
    print()

    if 't' in test:
        ttest = stats.ttest_ind(x, y)
        print(ttest)
        if ttest[1] < p:
            print('t test results are statistically significant')
        else:
            print('t test results are not statistically significant')
        print()

    if 'mw' in test:
        mwtest = stats.mannwhitneyu(x, y)
        print(mwtest)
        if mwtest[1] < p:
            print('Mann–Whitney U test results are statistically significant')
        else:
            print('Mann–Whitney U test results are not statistically significant')
        print()

    if 'm' in test:
        mtest = stats.median_test(x, y)
        print(mtest)
        if mtest[1] < p:
            print('Median test results are statistically significant')
        else:
            print('Median test results are not statistically significant')

    return None


def chi2_test_f(df: pd.DataFrame, group_by: str, feature: str, p: float = 0.05) -> None:
    '''
    This function uses chi squared test to compare contingency tables.
    The tables are made from pandas' dataframe and selecting features which we
    want to group and compare.

    It needs pandas' dataframe, feature we want to group by and feature which
    statistical significance will be tested as an arguments. Group by and tested
    feature must be entered as strings.

    Significance value by default is set to 0.05, but can be changed.
    '''
    contingency_table = df.groupby(group_by)[feature].value_counts()
    contingency_table = contingency_table.unstack().rename(columns={0: 'No', 1: 'Yes'}, index={0: 'No', 1: 'Yes'})
    print(contingency_table)

    results = stats.chi2_contingency(contingency_table)
    print(results)
    print()
    print(f'Set p value is {p}.')

    pvalue = results[1]
    if p > pvalue:
        print('Results are statistically significant')
    else:
        print('Results are not statistically significant')
    print()
    return None


def grid_search_f(
    model: BaseEstimator,
    param_grid: Dict[str, Any],
    x: pd.DataFrame,
    y: pd.Series,
    scoring: str = 'accuracy',
    showall: bool = False,
    cv: int = 5,
) -> Dict[str, Any]:
    """
    Performs a Grid Search with cross-validation and prints the top three results,
    including Precision, Recall, F1-score, and Accuracy.

    Parameters:
        model: The estimator to tune.
        param_grid: Dictionary with parameters to test.
        x, y: Features and target.
        scoring: Metric to optimize (default: 'accuracy').
        showall: If True, prints all results.
        cv: Number of cross-validation folds (default: 5).

    Returns:
        Best parameters from the search.
    """

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, scoring=scoring, cv=cv, error_score=0)
    with np.errstate(invalid='ignore'):  # to ignore a bugged error message
        grid_result = grid_search.fit(x, y)

    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']

    sorted_results = sorted(zip(means, stds, params), key=lambda x: x[0], reverse=True)

    print(f'Scoring: {scoring}')

    print("🔹 Top 3 Results with Evaluation Metrics::")
    for rank, (mean, stdev, param) in enumerate(sorted_results[:3], start=1):
        print(f"{rank}. Mean: {mean:.6f} ± {stdev:.6f} | Params: {param}")

        best_model = model.set_params(**param)
        with np.errstate(invalid='ignore'):
            y_pred = cross_val_predict(best_model, x, y, cv=cv)

        precision = precision_score(y, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y, y_pred, average='weighted')
        f1 = f1_score(y, y_pred, average='weighted')
        accuracy = accuracy_score(y, y_pred)

        print(f"   - Precision: {precision:.4f} | Recall: {recall:.4f} | F1-score: {f1:.4f} | Accuracy: {accuracy:.4f}")
        print(" ")

    if showall:
        print("\n🔹 **All Results:**")
        for mean, stdev, param in zip(means, stds, params):
            print("%f (%f) with: %r" % (mean, stdev, param))

    return grid_search.best_params_


def randomized_search_f(
    model: BaseEstimator,
    param_dist: Dict[str, Any],
    x: pd.DataFrame,
    y: pd.Series,
    scoring: str = 'accuracy',
    showall: bool = False,
    cv: int = 5,
    random_state: int = 0,
) -> Dict[str, Any]:
    """
    Performs a Randomized Search with cross-validation and prints the top
    three results, including Precision, Recall, F1-score, and Accuracy.

    Parameters:
        model: The estimator to tune.
        param_dist: Dictionary with parameters to test.
        x, y: Features and target.
        scoring: Metric to optimize (default: 'accuracy').
        showall: If True, prints all results.
        cv: Number of cross-validation folds (default: 5).
        random_state: same randomization each time code is ran (default: 0).

    Returns:
        Best parameters from the search.
    """

    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_dist,
        n_jobs=-1,
        scoring=scoring,
        cv=cv,
        random_state=random_state,
        error_score=0,
    )
    with np.errstate(invalid='ignore'):  # to ignore a bugged error message
        random_result = random_search.fit(x, y)

    means = random_result.cv_results_['mean_test_score']
    stds = random_result.cv_results_['std_test_score']
    params = random_result.cv_results_['params']

    sorted_results = sorted(zip(means, stds, params), key=lambda x: x[0], reverse=True)

    print(f'Scoring: {scoring}')

    print("🔸 Top 3 Results with Evaluation Metrics::")
    for rank, (mean, stdev, param) in enumerate(sorted_results[:3], start=1):
        print(f"{rank}. Mean: {mean:.6f} ± {stdev:.6f} | Params: {param}")

        best_model = model.set_params(**param)
        with np.errstate(invalid='ignore'):
            y_pred = cross_val_predict(best_model, x, y, cv=cv)

        precision = precision_score(y, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y, y_pred, average='weighted')
        f1 = f1_score(y, y_pred, average='weighted')
        accuracy = accuracy_score(y, y_pred)

        print(f"   - Precision: {precision:.4f} | Recall: {recall:.4f} | F1-score: {f1:.4f} | Accuracy: {accuracy:.4f}")
        print(" ")

    if showall:
        print("\n🔸 **All Results:**")
        for mean, stdev, param in zip(means, stds, params):
            print("%f (%f) with: %r" % (mean, stdev, param))

    return random_search.best_params_
