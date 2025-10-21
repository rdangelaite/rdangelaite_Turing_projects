# Analysis of the Mental Health in the Tech Industry

## Introduction

**Dataset information**

This data is from Open Source Mental Illness (OSMI) using survey data from years 2014, 2016, 2017, 2018 and 2019. Each survey measures and attitudes towards mental health and frequency of mental health disorders in the tech workplace. The dataset was taken from https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry.

**Project**

The Mental Health in the Tech Industry dataset is used for Understanding and Visualizing Data with Python project of Data Analysis module sprint 1. Data analysis is done using python and pandas library. For visualization matplotlib, plotly and seaborn libraries were used.

The project is done using python (version 3.11.4), seaborn (0.12.2), numpy (1.26.1), matplotlib (3.8.0), pandas (2.0.3), plotly (5.17.0) and scipy (1.11.2) libraries.

**Plan**

In the beginning all tables will be loaded and reviewed. Then basic data (age, gender, country) will be explored for survey participants. Lastly 3 questions will be selected to investigated further.

# Objectives for this Part

* Practice working with SQLite datasets.
* Practice performing EDA.
* Practice visualizing data with Matplotlib & Seaborn.
* Practice reading data, performing queries and filtering data using SQL and Pandas.

# Requirements

* Download the data from Mental Health in the Tech Industry.
* Load the data using SQLite and Pandas.
* Perform exploratory data analysis. This should include creating statistical summaries and charts, testing for anomalies, checking for correlations and other relations between variables, and other EDA elements.
* Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
* Provide suggestions about how your analysis can be improved.

# Summary

* There were total of 4218 participants in the survey. The survey started on 2014 and ended on 2019. Year 2015 was skipped for collecting data. Highest amount of participants was on year 2016 and since then participant amount decreased until year 2019 (the lowest amount of participants).
* Survey had diffrent amount of questions each year. The more questions the survey had, the less of them were answered. Overall, survey question answer rate is 75.88%. Only 12 questions were presented every year.
* Average age in the survey is 33.87 ± 0.13. The range is from 15 to 99 years old and outliers are present on the higher end.
* Most of participants are males (72.21%). Around a quarter of participants are female (24.32%).
* More than half of participants were from USA (61.76%). In second place by user amount is UK (11.43%) and in 3rd is Canada (4.72%).
* 3 questions which appeared every year were selected to be investigated.
* Around 44% of participants had family history of mental illness and 40% did not. 15% answered that they do not know if their family had mental illness or not. Around 57% of survey participants sought treatment for mental illness. Only 5.5% would bring up mental health issue in an interview. Majority of survey participants would prefer not bring it up (70%) and 24.5% answered that they might bring it up in an interview.
* The older generations have sought out mental health treatment more often.
* Compared to the rest of the world, more survey participants from USA have family history of mental illness and sought treatment for mental illness.
* There was less females in the survey, however they sought treatment for mental health disorder more often compared to males.
* Males are more likelly to bring up a mental health issue in an interview to a potential new employer, compared to females.

# Suggestions for improvements

* Calculate standart errors for correlation, as the sample is small to compare answered percent and question amount.
* Investigate more survey questions. Perhaps something changed over the years.
* Investigate survey answers for possible trolls.
* Compare tech industry with a different dataset. Figure out tech industry population statistics, proportions of males and females. Maybe, include weighted values, since there are much more males than females.
