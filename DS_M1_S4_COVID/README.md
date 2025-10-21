# Data Science for COVID-19

Analysis was done in Jupyter notebooks (JupyterLab Version 4.0.6). Python version 3.11.4. Requirements for used packages is saved in requirements.txt.

## Introduction

**Context**

This is a structured dataset based on the report materials of KCDC and local governments. The data is obtained from Kaggle website: https://www.kaggle.com/datasets/kimjihoo/coronavirusdataset?select=Region.csv.
COVID-19 has infected more than 10,000 people in South Korea. KCDC (Korea Centers for Disease Control & Prevention) announces the information of COVID-19 quickly and transparently. 

**Project**

The COVID-19 dataset is used for Capstone project of Data Wrangling. Data analysis is done using python and primarily pandas library. For visualization matplotlib, geopandas, windrose and seaborn libraries were used. 

## Objectives for this Part

* Practice identifying opportunities for data analysis.
* Practice performing EDA.
* Practice working with data from Kaggle.
* Practice visualizing data with Matplotlib & Seaborn.
* Practice reading data, performing queries, and filtering data using Pandas.

## Requirements

* Perform data cleaning and feature engineering. Work with features - handle missing data if needed, use Pandas date APIs, create other additional features.
* Perform exploratory data analysis. Describe the data with basic statistical parameters - mean, median, quantiles, etc. Use parameters that give you the most important statistical insights of the data. Grouping the data and analyzing the groups - using Pandas aggregate methods. Visualize the data - you can use line, scatter, histogram plots, density plots, regplots, etc.
* Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
* Present the project - the data, methods, and results.
* Provide suggestions about how your analysis can be improved.

# Summary of findings

* Majority of COVID cases started as part of a group – places where people gather for events or other reasons. As such, we see churches, hospitals, clubs and gyms among places with highest case COVID case counts. There are a lot of outbreaks resulting from religious group activities. Case with highest infection count comes from Daegu province, Shincheonji Church.
* Although the virus spreads among all age groups, it spreads among elderly and sick easier, since hospitals and nursing homes appear often in infection causes. Places often visited by younger people, such as clubs or gyms, have much less cases.
* Although, majority of cases did come from group activities, there is still a considerable percent of them originating from individual to individual transfers, such as overseas travel, patient to patient contact and individual cases.
* Majority of COVID cases originated from city. Least amount of cases originated from country. Therefore, people density is likely to play a part in spread of COVID, most likely due to low density of people. 8.33% of cases originated from abroad.
* Confirmed count rises in waves. The second wave was smaller than the first one and maximums for waves are separated around by 3 months.
* There were more females than males in the dataset, but males had more contacts with others. Also, the virus was more deadly to males compared to females.
*  Most of people had to wait up to ten days to get confirmation that they got covid. Sometimes symptoms only appeared after confirmation of COVID.
*  Active policy amount negatively correlates with contacts and deceased patients, which indicates that policies did achieve what they were suposed to do – reduce contacts and deaths.
*  Amount of confirmed covid cases correlate strongly with nursing home count.
*  There is correlation between how many patients there are and population. Therefore, the more people are in the district, the more COVID patients as well. However, correlation between percent of confirmed infected population and population itself is low.
*  Coronavirus search looks like it is moved in time few days before the rise of amount confirmed.
*  Most confirmed COVID cases were in 20s age group. Highest mortality is in 80s age group. It had the highest amount of deceased and the highest pecent of deceased patients. No infected people aged up to 30 died during this period.
*  COVID does not seem to be related to weather much, however, timeframe for COVID data might be too short to have any concrete results.

## Suggestions for improvements

Deeper investigation of policies and Seoul data. Also investigation for outliers for symptom - confirmation days. Grouping patient data by two categories: for example age and gender. Draw some more interactive graphs for weather data, and other datasets where it is fitting. Create different versions for Git and presentation, since interactive graphs do not work there. Fix accumulated datasets so that following value would not be lower than previous one. Compare Korean data with other countries data. Also, obtain data for longer time period and do analysis on that. 
