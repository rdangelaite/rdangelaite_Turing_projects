import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.axes as axes
import matplotlib as plt
import unicodedata
from typing import Optional


def count_percentage(value: float, total: float, round_value: int = 2) -> float:
    """
    Function to count % of a value.
    """
    return round(value / total * 100, round_value)


def bar_plot_f(data: pd.Series, name: str, col: str, **kwargs) -> axes.Axes:
    """
    Function to draw Seaborn barplot easier.
    """
    ax = sns.barplot(x=data.index, y=data, color=col, **kwargs)
    ax.set_title(name)
    ax.set_xticklabels(labels=data.index, fontsize=9, alpha=0.8)
    labels_list = []
    for i in range(len(data)):
        labels_list.append(data[i])
    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    return ax


def bar_plot_f_perc(
    data: pd.Series, name: str, total: float, palet: str, **kwargs
) -> axes.Axes:
    """
    Function to draw Seaborn barplot easier.
    It has % on bar labels together with instances count.
    """
    ax = sns.barplot(x=data.index, y=data, palette=palet, **kwargs)
    ax.set_title(name)
    ax.set_xticklabels(labels=data.index, fontsize=9, alpha=0.8)
    labels_list = []
    for i in range(len(data)):
        labels_list.append(f"{data.iloc[i]} ({count_percentage(data.iloc[i], total)}%)")
    ax.bar_label(ax.containers[0], labels=labels_list, fontsize=9)
    ax.tick_params(left=False)
    ax.set(ylabel=None, xlabel=None, yticklabels=[])
    return ax


def rank_palette(data: pd.Series, pal_name: str) -> np.array:
    """
    Custom palette maker to rank palettes by values.
    Takes data and an existing colour palette.
    Sorts palette colours by rank based on data values.
    """
    pal = sns.color_palette(pal_name, len(data))
    rank = data.argsort().argsort()
    return np.array(pal[::-1])[rank]


def date_conv(unicode_arabic_date: str) -> str:
    """
    Function to convert date from arabic numerals format to typical western.
    """
    new_date = ""
    for d in unicode_arabic_date:
        if d in "T:0700":
            new_date += d
        elif d != "-":
            try:
                new_date += str(unicodedata.digit(d))
            except:
                print(new_date)
                continue
        else:
            new_date += "-"
    return new_date


def outlier_f(data: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """
    Detecting if there are any outliers within 1.5IQR.
    We will use Tukey's rule to detect outliers, also known as IQR rule.
    First, we will calculate the Interquartile Range of the data:

    IQR = Q3 - Q1

    Q1 and Q3 stand for 25th and 75th percentiles.
    Later we determine our outlier boundaries with IQR:

    IQR_lower = Q1 - 1.5 * IQR
    IQR_upper = Q3 + 1.5 * IQR

    The data entered is meant to be Pandas dataframe or series.
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    # Boundaries
    IQR_lower = Q1 - 1.5 * IQR
    IQR_upper = Q3 + 1.5 * IQR

    mask = (data < IQR_lower) | (data > IQR_upper)
    outliers = data[mask]
    return outliers
