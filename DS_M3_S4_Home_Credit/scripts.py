import seaborn as sns
import pandas as pd
import numpy as np
import duckdb as db
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import scipy.stats as stats
from typing import Dict, Any, List
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_predict
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_curve, auc
from scipy import stats
from typing import List, Literal


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


def kendalltau_f(x: List[str], y: List[str], dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    The function computes the Kendall rank correlation coefficient between
    pairs of columns in a given DataFrame.

    The Kendall tau coefficient is a statistic used to measure the ordinal
    association between two measured quantities. It can be used when both
    values are binary.

    Parameters:
    - x: a list of column names to be used as row indices in the output
    DataFrame.
    - y: a list of column names to be used as column indices in the output
    DataFrame.
    - dataframe: the DataFrame containing the data for correlation computation.

    Returns: DataFrame where each cell (i, j) contains the Kendall tau
    correlation coefficient between column i from "x" and column j from "y".
    """
    df = pd.DataFrame(index=x, columns=y, dtype=float)

    for i in x:
        for j in y:
            kendalltau = stats.kendalltau(dataframe[i], dataframe[j])
            df.loc[i, j] = kendalltau[0]

    return df.astype(float)


def correlation_f(dataframe: pd.DataFrame, flag: bool = False) -> pd.DataFrame:
    """
    Calculates a pairwise correlation matrix for a DataFrame, automatically selecting
    an appropriate correlation method based on variable types and handling missing data.

    Correlation method selection:
    - If both variables are binary: uses Kendall's tau
    - If both variables are continuous or ordinal: uses Spearman's rank correlation
    - If one variable is binary and the other continuous: uses Point-Biserial correlation

    NaN handling:
    - Correlations are computed only on rows where both variables are non-missing.
    - If either variable has only one unique non-missing value, correlation is set to NaN.

    Parameters:
    ----------
    dataframe : pd.DataFrame
        A DataFrame containing the variables for which to compute pairwise correlations.
    flag : bool, optional
        If True, prints diagnostic messages for skipped or problematic variable pairs.

    Returns:
    -------
    pd.DataFrame
        A symmetric correlation matrix with variables as both rows and columns.
        Diagonal values are set to 1.0.
    """
    x = dataframe.columns
    df = pd.DataFrame(index=x, columns=x, dtype=float)

    for i in x:
        for j in x:
            if i == j:
                df.loc[i, j] = 1
                break

            else:
                valid_data = dataframe[[i, j]].copy().dropna()
                leni = len(valid_data[i].unique())
                lenj = len(valid_data[j].unique())

                if leni == 1 or lenj == 1:
                    df.loc[i, j] = float('nan')
                    df.loc[j, i] = float('nan')
                    if flag:
                        print(f"Skipped ({i}, {j}): constant input,")
                        print(f"respective unique value counts: {leni}, {lenj}.")
                    continue

                elif leni == 2 and lenj == 2:
                    corr = stats.kendalltau(valid_data[i], valid_data[j])

                elif leni != 2 and lenj != 2:
                    corr = stats.spearmanr(valid_data[i], valid_data[j])

                else:
                    corr = stats.pointbiserialr(valid_data[i], valid_data[j])

                df.loc[i, j] = corr[0]
                df.loc[j, i] = corr[0]

    return df.astype(float)


def get_correlations(df: pd.DataFrame, threshold: float = 0.9, higher: bool = True) -> pd.DataFrame:
    """
    Return pairs of features with correlation above a threshold.

    Parameters:
    df: Correlation matrix.
    threshold: Correlation threshold (default is 0.9).
    higher: if true takes values higher than the treshold. If false - lower
    values (default is true).

    Returns:
    DataFrame with pairs of correlated features and their correlation values.
    """
    corr_matrix = df.copy()
    corr_matrix = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))  # Keep upper triangle
    corr = corr_matrix.stack().reset_index()
    corr.columns = ['Feature_1', 'Feature_2', 'Correlation']

    if higher:
        mask = corr['Correlation'] > threshold
        ascending = False
    else:
        mask = corr['Correlation'] < threshold
        ascending = True

    result = corr[mask].sort_values(by='Correlation', ascending=ascending)
    return result


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


def remove_outliers_iqr(df: pd.DataFrame, cols: list[str] | None = None, factor: float = 3.0) -> pd.DataFrame:
    """
    Removes extreme outliers based on IQR.
    Only removes values outside Q1 - factor * IQR or Q3 + factor * IQR.
    Skips columns with binary data

    Parameters:
    - df: The input DataFrame.
    - cols: List of columns to check for outliers. If None, all numeric columns are used.
    - factor: The IQR multiplier threshold (default is 3.0).

    Returns:
    - A DataFrame with outliers replaced by NaN
    """
    df_cleaned = df.copy()
    if cols is None:
        cols = df_cleaned.select_dtypes(include='number').columns

    for col in cols:
        if df[col].nunique(dropna=True) <= 2:
            continue
        else:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - factor * iqr
            upper = q3 + factor * iqr
            mask = (df_cleaned[col] < lower) | (df_cleaned[col] > upper), col
            df_cleaned.loc[mask] = np.nan

    return df_cleaned


def bar_plot_f_perc(data: pd.Series, name: str = '', order: List[Any] | None = None, **kwargs) -> axes.Axes:
    """
    Function to draw Seaborn barplot easier.
    It has % on bar labels together with instances count.
    The % is calculated by taking a value for a category and dividing it by
    total number of instances.

    The function takes Pandas series as an argument.

    The name argument is the title for the graph and is optional.
    Order (list) is optional custom category order to enforce correct label alignment.

    The function returns axes.
    """
    if order is None:
        order = list(data.index)

    ax = sns.barplot(x=data.index, y=data, order=order, **kwargs)
    ax.set_title(name)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(labels=data.index, fontsize=9, alpha=0.8)

    total = data.sum()
    labels_list = [f"{data.loc[val]} ({count_percentage(data.loc[val], total)}%)" for val in order]
    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    sns.despine(left=True, bottom=True)
    return ax


def bar_plot_f_perc_horizontal(data: pd.Series, name: str = '', **kwargs) -> axes.Axes:
    """
    Function to draw Seaborn barplot easier.
    This function draws the bar plot horizontally.
    It has % on bar labels together with instances count.
    The % is calculated by taking a value for a category and dividing it by
    total number of instances.

    The function takes Pandas series as an argument.

    The name argument is the title for the graph and is optional.

    The function returns axes.
    """

    ax = sns.barplot(x=data, y=data.index, **kwargs)
    ax.set_title(name)

    labels_list = []
    total = data.sum()
    for i in range(len(data)):
        labels_list.append(f"{data.iloc[i]} ({count_percentage(data.iloc[i], total)}%)")

    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False, bottom=False)
    ax.set(ylabel=None, xlabel=None, xticklabels=[])
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


def bar_plot_multi_index_f_horizontal(data: pd.Series, x: str, hue: str, name: str, palet: str, **kwargs) -> axes.Axes:
    '''
    This is a function made to draw a graph from pandas multi series
    index. It takes one of the indexes as x and another one as hue.
    '''
    df = df_from_multiindex(data, x)
    ax = sns.barplot(df, x=df.iloc[:, 1], y=df.index, palette=palet, hue=hue, **kwargs)
    ax.set_title(name)
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=9, alpha=0.8)

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

    ax.tick_params(left=False, bottom=False)
    ax.set(ylabel=None, xlabel=None, xticklabels=[])
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
    data: pd.Series,
    color_mean: str = '#B8B3E9',
    color_median: str = '#7EDAF1',
    name: str = '',
    xlabel: str = '',
    mean_meadian: bool = True,
    **kwargs,
) -> axes.Axes:
    '''
    This is function to draw a histogram, with Seaborn library.
    It addition it also draws lines for mean and median.
    Drawing mean and median can be turned off if needed, by setting it to false.

    The function takes Pandas series as an argument.

    Optionally it is possible to choose colors for mean and median by entering
    color name or hexadecimal color code as a string,
    for example: color_mean = 'blue',  color_median = '#7EDAF1'.

    The name argument is the title for the graph and is optional.
    The xlabel argument is also optional.

    The function returns axes.
    '''
    ax = sns.histplot(data=data, **kwargs)
    if name:
        ax.set(title=name)
    if xlabel:
        ax.set(xlabel=xlabel)
    if mean_meadian:
        ax.axvline(x=data.mean(), color=color_mean, label='Mean')
        ax.axvline(x=data.median(), color=color_median, label='Median')
        ax.legend(loc='upper right', edgecolor='none')
    return ax


def simple_kdeplot(data: pd.DataFrame, x: str, xlabel: str = '', fill: bool = True, **kwargs) -> axes.Axes:
    '''
    This is function to draw a kde plot, with Seaborn library.
    The function takes Pandas data frame and x as a string as arguments.

    By default it the plot is filled.

    Optionally it is possible to choose name for x axis.

    The function returns axes.
    '''
    ax = sns.kdeplot(data=data, x=x, fill=fill, **kwargs)
    if xlabel:
        ax.set(xlabel=xlabel)
    return ax


def plot_roc_curve(
    y: pd.Series, y_probs: pd.Series, model_name: str = "Model", color: str = "#036264", alpha: float = 1
) -> float:
    """
    Plots the ROC curve and computes AUC for a given model and dataset.

    Parameters
    ----------
    y : pd.Series
        True binary labels.
    y_probs : pd.Series
        Predicted probabilities for the positive class.
    model_name : str, optional
        Name of the model (for labeling the plot). Default is 'Model'.
    color : str, optional
        Color for the ROC line. Default is '#036264'.
    alpha: float, optional
        The parameter that controls the transparency level of a plot.

    Returns
    -------
    roc_auc : float
        Area under the ROC curve (AUC score).
    """

    # Compute ROC curve and AUC
    fpr, tpr, _ = roc_curve(y, y_probs)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color=color, lw=2, label=f'{model_name} (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='#11302a', linestyle='--', lw=2, alpha=alpha)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()

    return roc_auc


def plot_feature_importance(
    model,
    feature_names: List[str],
    n: int = 10,
    order: Literal["top", "bottom"] = "top",
    palette: str = "crest",
    model_name: str = "the Model",
) -> List[str]:
    """
    Plots the top or bottom N most important features from a model with feature_importances_.

    Parameters
    ----------
    model : fitted model
        Any trained model that exposes the `feature_importances_` attribute (e.g., XGBoost, LightGBM, RandomForest).
    feature_names : list of str
        Names of features used in model training.
    n : int, optional
        Number of features to display. Default is 10.
    order : {'top', 'bottom'}, optional
        Whether to show the most ('top') or least ('bottom') important features. Default is 'top'.
    palette : str, optional
        Seaborn color palette to use for bars. Default is 'crest'.
    model_name : str, optional
        Tittle of the model. Default is 'the Model'.

    Returns
    -------
    selected_features : list of str
        The feature names that were plotted.
    """

    importances = model.named_steps["clf"].feature_importances_

    # Sort importances
    indices = np.argsort(importances)
    if order == "top":
        indices = indices[::-1]

    # Select top or bottom n
    selected_indices = indices[:n]
    selected_features = [feature_names[i] for i in selected_indices]
    selected_importances = importances[selected_indices]

    # Plot
    plt.figure(figsize=(10, n * 0.15 + 2))
    ax = sns.barplot(
        x=selected_importances, y=selected_features, hue=selected_importances, palette=palette, dodge=False
    )
    ax.set(
        xlabel="Feature Importance",
        ylabel="Feature Name",
        title=f"{n} {'Most' if order=='top' else 'Least'} Important Features of {model_name}",
    )
    ax.get_legend().set_visible(False)
    plt.tight_layout()
    plt.show()

    return selected_features


def thousands_formatter(x: float, pos: int) -> str:
    """
    Formats a number by converting absolute values >= 1000 to a 'k' format
    (e.g., 10000 -> '10k').

    Args: x (float): The tick value.
    pos (int): The tick position (required by FuncFormatter, but not used here).

    Returns: str: Formatted tick label.
    """
    if abs(x) >= 1000:
        return f'{int(x/1000)}k'
    return f'{int(x)}'


def chi2_test_f(df: pd.DataFrame, group_by: str, feature: str, p: float = 0.05) -> float:
    '''
    This function uses chi squared test to compare contingency tables.
    The tables are made from pandas' dataframe and selecting features which we
    want to group and compare.

    It needs pandas' dataframe, feature we want to group by and feature which
    statistical significance will be tested as an arguments. Group by and tested
    feature must be entered as strings.

    Significance value by default is set to 0.05, but can be changed.

    The function returns calculated p value.
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
    return pvalue


def analyze_distribution(data: pd.DataFrame, column: str, sample_size: int = 100000, random_state: int = 42) -> bool:
    """
    Analyzes the distribution of a numerical column in a DataFrame using:
        - Skewness and kurtosis
        - Kolmogorov-Smirnov test

    Args:
        data (pd.DataFrame): The input DataFrame containing the column.
        column (str): The name of the numerical column to analyze.
        sample_size (int, optional): Max number of data points to sample.
            Defaults to 100 000.
        random_state (int, optional): Random seed for reproducibility.
            Defaults to 42.

    Returns:
        bool: The function outputs boolean value - True for normal distributions,
        False for other, based on Kolmogorov-Smirnov test.
    """

    col_data = data[column].dropna()
    if len(col_data) > sample_size:
        col_sample = col_data.sample(sample_size, random_state=random_state)
    else:
        col_sample = col_data

    print(f"Skewness: {stats.skew(col_sample):.3f}")
    print(f"Kurtosis: {stats.kurtosis(col_sample):.3f}")

    # Kolmogorov-Smirnov Test
    ks_result = stats.kstest(col_sample, 'norm', args=(col_sample.mean(), col_sample.std()))
    print("\n📈 Kolmogorov-Smirnov Test:")
    print(f"Statistic: {ks_result.statistic:.3f}, p-value: {ks_result.pvalue:.3f}")

    if ks_result.pvalue < 0.05:
        print("→ Likely not normal")
        return False
    else:
        print("→ Possibly normal")
        return True


def hypothesis_tests_f(
    x: pd.Series, y: pd.Series, p: float = 0.05, name_x: str = '', name_y: str = '', test: list = ['t']
) -> None | float:
    '''
    This function takes two populations for statistical comparison and prints
    95% confidence intervals and if they overlap and a statistical test.

    By default the function returns t test, however it can be set to return
    Mann–Whitney U test and Median test and their results, by entering a list
    with desired tests as an argument to the function:
    - to get t test (the default) the list is set to ['t']
    - to get Mann–Whitney U, the list should be set to ['mw']
    - to get Median test - ['m']
    - to get all of the tests set the list to ['t', 'mw', 'm']

    It needs two panda series as argument.
    Significance value by default is set to 0.05, but can be changed.
    Confidence intervals can be named according to taken datasets for clarity.

    If there is only one test done the function returns p value.
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
        result = stats.ttest_ind(x, y)
        print(result)
        if result[1] < p:
            print('t test results are statistically significant')
        else:
            print('t test results are not statistically significant')
        print()

    if 'mw' in test:
        result = stats.mannwhitneyu(x, y)
        print(result)
        if result[1] < p:
            print('Mann–Whitney U test results are statistically significant')
        else:
            print('Mann–Whitney U test results are not statistically significant')
        print()

    if 'm' in test:
        result = stats.median_test(x, y)
        print(result)
        if result[1] < p:
            print('Median test results are statistically significant')
        else:
            print('Median test results are not statistically significant')

    if len(test) == 1:
        return result[1]
    else:
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


def choosing_params(params: str) -> list:
    '''
     Helper function for model building that selects which building parameters to keep.

    Given a parameter name (e.g., 'mean', 'median', or 'mode'), it returns a list of
    features that should be dropped based on the chosen parameter.

    Args:
        params (str): The name of the parameter selection strategy ('mean', 'median',
        or 'mode').

    Returns:
        list: A list of feature names to drop.
    '''
    building_avg = [
        'APARTMENTS_AVG',
        'BASEMENTAREA_AVG',
        'YEARS_BEGINEXPLUATATION_AVG',
        'YEARS_BUILD_AVG',
        'COMMONAREA_AVG',
        'ELEVATORS_AVG',
        'ENTRANCES_AVG',
        'FLOORSMAX_AVG',
        'FLOORSMIN_AVG',
        'LANDAREA_AVG',
        'LIVINGAPARTMENTS_AVG',
        'LIVINGAREA_AVG',
        'NONLIVINGAREA_AVG',
    ]

    building_mod = [
        'APARTMENTS_MODE',
        'BASEMENTAREA_MODE',
        'YEARS_BEGINEXPLUATATION_MODE',
        'YEARS_BUILD_MODE',
        'COMMONAREA_MODE',
        'ELEVATORS_MODE',
        'ENTRANCES_MODE',
        'FLOORSMAX_MODE',
        'FLOORSMIN_MODE',
        'LANDAREA_MODE',
        'LIVINGAPARTMENTS_MODE',
        'LIVINGAREA_MODE',
        'NONLIVINGAREA_MODE',
    ]

    building_med = [
        'APARTMENTS_MEDI',
        'BASEMENTAREA_MEDI',
        'YEARS_BEGINEXPLUATATION_MEDI',
        'YEARS_BUILD_MEDI',
        'COMMONAREA_MEDI',
        'ELEVATORS_MEDI',
        'ENTRANCES_MEDI',
        'FLOORSMAX_MEDI',
        'FLOORSMIN_MEDI',
        'LANDAREA_MEDI',
        'LIVINGAPARTMENTS_MEDI',
        'LIVINGAREA_MEDI',
        'NONLIVINGAREA_MEDI',
    ]

    drop_list = []
    if params == 'mean':
        drop_list.extend(building_med)
        drop_list.extend(building_mod)
    elif params == 'median':
        drop_list.extend(building_avg)
        drop_list.extend(building_mod)
    else:
        drop_list.extend(building_avg)
        drop_list.extend(building_med)
    return drop_list
