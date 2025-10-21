# Travel Insurance Dataset Project

## Introduction

Travel insurance is coverage designed to protect against risks and financial losses that could happen while traveling. The risks range from minor inconveniences such as missed airline connections and delayed luggage all the way to more serious issues including injuries or major illness (https://www.nationwide.com/lc/resources/home/articles/what-is-travel-insurance).  

Roughly 38% of travelers take travel insurances according to survey done in 2023 by businessinsider (https://www.businessinsider.com/personal-finance/travel-insurance-statistics-winter-2023-1). Main reasons for buying a travel insurance were delayed flights or moved reservations (35%). About 29% were worried about a health emergency. The majority of insured travelers (55%) purchased their policy through a travel provider.

The goal of this project is to make a model which would predict if the person is going to buy travel insurance or not, based on available data. Predictions from model can be used for targeted advertisements. Data is taken from Kaggle (https://www.kaggle.com/datasets/tejashvi14/travel-insurance-prediction-data)

**Dataset information**

A Tour & Travels Company is offering travel insurance package to their customers. The new insurance package also includes covid cover.

The company requires to know the which customers would be interested to buy it based on its database history.
The insurance was offered to some of the customers in 2019 and the given data has been extracted from the performance/sales of the package during that period. The data is provided for almost 2000 of its previous customers and you are required to build an intelligent model that can predict if the customer will be interested to buy the travel insurance package based on certain parameters given. The solution offered by you may be used for customer specific advertising of the package.

**Project**

Travel Insurance Prediction Data is used for Supervised Machine Learning Fundamentals project of Machine Learning module sprint 1. Data analysis is done using python and pandas library. Modeling is done using scikit-learn. For visualization matplotlib and seaborn libraries were used. The project is done using Jupyter notebooks (4.1.2).

The project is done using python (version 3.11.4), numpy (1.26.1), seaborn (0.12.2), matplotlib (3.7.3), pandas (2.0.3), scikit-learn (1.3.0), statsmodels (0.14.1) and scipy (1.11.2) libraries.

**Plan**

First, I will do exploratory data analysis.

Second, I will look into three questions, regarding the features: 
* Do people who buy travel insurance have higher income?
* Is there an age difference between people who bought travel insurance and ones who did not?
* Do frequent fliers buy travel insurance more often?
And I will try to answer them using hypothesis testing and use results for modeling.

Third, I will create few models and tune their hyper-parameters:
* Logistic regression, k-nearest neighbors, support vector machine and random forest.
* After tuning the best model will be chosen, based on accuracy.

## Summary

The dataset consist of 1987 entries and it has 9 features. Information about features:
- Age - age of the customer
- Employment Type - the sector in which customer is employed
- GraduateOrNot - whether the customer is college graduate or not
- AnnualIncome - the yearly income of the customer in Indian rupees, rounded to nearest 50 thousand rupees.
- FamilyMembers - number of members in customer's family
- ChronicDisease - whether the customer suffers from any major disease or conditions like diabetes/high BP or asthma, etc.
- FrequentFlyer - derived data based on customer's history of booking air tickets on at least 4 different instances in the last 2 years (2017 – 2019).
- EverTravelledAbroad - has the customer ever traveled to a foreign country, not necessarily using the company's services.
- TravelInsurance - did the customer buy travel insurance package during introductory offering held in the year 2019.

The dataset is not balanced, because as some categories are not as frequent as others (for example, there are 19% of frequent fliers compared to 81% non frequent ones). However, there should be enough data to represent all of the categories.

We can see that having higher annual income correlates with buying travel insurance, traveling abroad and being a frequent flier. It makes sense as people with higher income have more money available for more expensive leisure activities. Being a frequent flier and ever traveling abroad also correlates with buying the insurance.

After exploring the data some hypothesis testing has been done. Here are the findings:
- There is a statistical difference in income between ones who bought the insurance and ones who didn't. People who tend to buy travel insurance tend to have higher income.
- We cannot say with confidence that there is a statistical difference between ages in both groups, as it did fail the Mann-Whitney U test and p value (0.03) is higher than our set limit (0.0167). Also practically the average age difference looks insignificant (29.89 for ones who bought the insurance vs 29.52 ones who didn't). However, the age feature is going to be kept for modeling, because it did pass t test and median test (as they show statistical significance), and it might be somewhat significant in determining if the customer is going to buy the insurance or not.
- Frequent flyers do tend to buy travel insurance more often than ones who do not.

For modeling Logistic regression, K-Nearest Neighbors (KNN), Support Vector Machine (SVM) and Random Forest models were trained and their hyper-parameters tuned using grid search. The goal was to have higher accuracy than 64.27%, which is the percentage of people who do not buy the travel insurance. 

All of the models perform well, and their accuracy is higher than set target (64.27%) and is about 80%. 3 best performing models were be ensembled. They accuracy on training set was 81.44%. The model performs well and has high accuracy and high precision, for both who bought (87%) and who didn't buy travel insurance (81%). It has high recall for people who didn't buy the insurance (95%). Recall for guessing who bought it is only 60%, however it is more important to have higher accuracy and precision in this case.

The model should perform well for selecting customers for whom to advertise the travel insurance.

# Suggestions for improvement 

- Better visualization for confusion matrix.
- Tuning models for precision instead of accuracy. 
- Picking more hyper-parameter combinations.
- Use other method for picking hyper-parameters: random search or Bayesian optimization.
- Do feature selection.
