# Analysis of Podcast Reviews dataset

## Introduction

A podcast is a digital program consisting of a series of episodes that you can download or stream from the internet. They are primarily an audio medium, with some of podcasts also offering a video component as well. 

In 2022 it was estimated that 62% of Americans will have listened to a podcast in their lifetime. This percentage has increased from 57% in 2021 (source: https://riverside.fm/blog/podcast-statistics). It is obvious that podcasts are becoming more and more popular. Therefore, it makes sence to analyse data from them to see if there are any tendencies.

**Dataset information**

2 million podcast reviews for 100k podcasts, updated monthly. This dataset is intended to aid in analysis of text feedback and review data. The dataset was taken from https://www.kaggle.com/datasets/thoughtvector/podcastreviews/versions/28.

**Project**

Podcast Reviews dataset is used for Inferential Statistical Analysis project of Data Analysis module sprint 2. Data analysis is done using python and pandas library. For visualization matplotlib, plotly and seaborn libraries were used.

The project is done using python (version 3.11.4), seaborn (0.12.2), numpy (1.26.1) (used in scripts.py file), matplotlib (3.8.0), pandas (2.0.3), duckdb (0.9.1) and scipy (1.11.2) libraries.

**Plan**

Explore date presented in the tables. Test three hypotheses.

**Dashboard**

This is a link to my created dashboard for this project:
https://lookerstudio.google.com/reporting/48ed55c4-1398-4f91-80fe-a86d25e3e891

## Objectives for this Part

* Practice working with SQLite datasets.
* Practice performing EDA.
* Practice applying statistical inference procedures.
* Practice visualizing data with Matplotlib & Seaborn.
* Practice creating dashboards.
* Practice reading data, performing queries, and filtering data using SQL and Pandas.

## Requirements

* Download the data from Podcast Reviews Dataset.
* Load the data using SQLite and Pandas.
* Perform exploratory data analysis. This should include creating statistical summaries and charts, testing for anomalies, checking for correlations and other relations between variables, and other EDA elements.
* Perform statistical inference. This should include defining the target population, forming multiple statistical hypotheses and constructing confidence intervals, setting the significance levels, and conducting z or t-tests for these hypotheses.
* Create a dashboard using Looker Studio or another BI tool, e.g. Tableau with at least three different types of charts.
* Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
* Provide suggestions about how your analysis can be improved.

## Summary of findings

* There seems to be a lot of podcasts with chruch in it's title. Close second most common word is life. The 3rd most popular word is real.
* On average one podcast will have two categories. At most the podcast will have 8 categories and there are 3 podcasts like that: Beyond Retirement, FrazerRice.Com and Pursue Execellence.
* Most common podcast category is society-culture. Rarest is sports-volleyball, which seems to be specific sub-category of sports.
* There are 2,066,874 reviews in the dataset.
* Majority of ratings are 5 stars (86.58%). There are 5.64% of ratings for 1 star. Ratings of 2 to 4 stars aren't as likely to be given.
* Majority of reviewers wrote just one review. There are two reviewers who wrote 615.
* There is weak negative correlation between left review amount and podcasts ratings.

Three hypotheses were tested to answer these questions I am interested in:

    Do people who do not like the podcast leave longer reviews?
    Are average ratings left during the winter lower compared to summer?
    Are more reviews left on podcasts about news-politics compared to science podcasts?

Confidence intervals were built, and t-test and Mann-Whitney U test were used for all hypothesies. For the 1st and 3rd were also tested with Mood's median test.

Results:
* There is statisticaly significant result that people, who listened itunes podcasts, leave longer reviews for the podcasts they do not like. This is indicated by weak negative correlation between rating and review length.
* There is statistical difference between ratings left on winter compared to summer (listeners tended to leave higher ratings during winter, compared to summer). However, the difference is small (confidence interval for winter is: 4.62491, 4.63064; for summer: (4.61842, 4.62413), and practicaly there is no difference.
* There is statistical difference between amount of reviews left on news-politics compared to science podcasts. However, they did fail one test, that is Mood's Median test, when the outliers are removed. Therefore, we cannot confidentaly say that we reject null hyphotesis.

## Suggestions for improvements

* Include permutation tests.
* More comparisons between categories and more investigations into categories.
* Investigate content of the reviews.
* Find a way to separate troll reviews (if it is clearly troll review).
* Create fancier dashboard.
* Separate more popular, higher reviewed podcasts from not so popular podcasts with few reviews.
* Do more timeline investigations, like weekday comparisons etc.
