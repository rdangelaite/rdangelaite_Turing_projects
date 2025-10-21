# Spaceship Titanic Dataset Project

## Project Overview

The Spaceship Titanic is an interstellar liner that mysteriously encountered a spacetime anomaly, transporting part of its passengers to an alternate dimension!

This project aims to predict which passengers were transported using machine learning models. The dataset is taken from the Kaggle Spaceship Titanic competition and contains passenger details such as age, home planet, spending habits, and cabin location.

The goal is to build an accurate predictive model that can outperform a baseline logistic regression model and achieve a Kaggle submission score of 0.79 or higher.

### Dataset Information

Source: Kaggle Spaceship Titanic (https://www.kaggle.com/competitions/spaceship-titanic/overview)
Size: ~13,000 passengers
Features:

- PassengerId - A unique Id for each passenger. Each Id takes the form gggg_pp where gggg indicates a group the passenger is traveling with and pp is their number within the group. People in a group are often family members, but not always.
- HomePlanet - The planet the passenger departed from, typically their planet of permanent residence.
- CryoSleep - Indicates whether the passenger elected to be put into suspended animation for the duration of the voyage. Passengers in cryo sleep are confined to their cabins.
- Cabin - The cabin number where the passenger is staying. Takes the form deck/num/side, where side can be either P for Port or S for Starboard.
- Destination - The planet the passenger will be debarking to.
- Age - The age of the passenger.
- VIP - Whether the passenger has paid for special VIP service during the voyage.
- RoomService, FoodCourt, ShoppingMall, Spa, VRDeck - Amount the passenger has billed at each of the Spaceship Titanic's many luxury amenities.
- Name - The first and last names of the passenger.
- Transported - Whether the passenger was transported to another dimension. This is the target.

### Project

Spaceship Titanic competition dataset is used for Unsupervised Learning & Hyperparameter Tuning project of Machine Learning module sprint 3. Data analysis is done using python and pandas library. Modeling is done using scikit-learn. For visualization matplotlib and seaborn libraries were used. The project is done using Jupyter notebooks (4.2.4).

The project is done using python (version 3.11.4), numpy (2.0.1), seaborn (0.13.2), matplotlib (3.9.1), missingno (0.5.2), pandas (2.2.3), scikit-learn (1.5.1), scipy (1.14.0) and statsmodels (0.14.2)libraries.

## Project Goals & Approach

1. Exploratory Data Analysis (EDA)

    Visualizing key features and trends
    Checking missing values and handling them appropriately
    Identifying correlations between features and the target variable

2. Statistical Hypothesis Testing

    T-tests & Mann-Whitney U Tests to check numerical feature significance
    Chi-square tests for binary feature importance

3. Machine Learning Modeling

    Baseline Model: Logistic Regression
    Advanced Models:
        Random Forest (Best Performing Model)
        Support Vector Machine (SVM)
   
4. Hyperparameter Tuning

    Randomized Search CV followed by Grid Search CV
    Feature selection and model evaluation based on accuracy

5. Kaggle Submission

    The final Random Forest model achieved an accuracy of 0.79822, meeting the competition goal.

## Key Findings & Insights

- 50.36% of passengers were transported by the anomaly.
- Passengers in Cryo Sleep (81.76%) had a much higher chance of being transported.
- Passengers from Europa (65.88%) and those traveling to 55 Cancri e (61%) were more likely to be transported.
- Children (under 18) were transported more frequently.
- Spending money on attractions reduced the chance of being transported:
  - Passengers who spent nothing had a higher transport rate (78.65%).
  - Those who spent money  were less likely to be transported (only 29.86%).
- Correlation Analysis:
  - Positive correlation: Cryo Sleep, Europa, Decks B & C, and Starboard side.
  - Negative correlation: Spending money, Home Planet Earth, Port side.

## Suggestions for improvement 

- Create a function which automatically picks correlation coeficient to calculate depending on the value of the variables.
- Use dimension reduction algorithm.
- Create new features by combining existing ones (for example, perhaps there is an interaction between deck and home planet).
- Try polynomial features for potential non-linear relationships.
- Try to use log scale for money since there are a lot of outliers.
- Use K-Means or DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to find hidden groups among passengers (e.g., spending behavior, travel habits). Add cluster labels as new features.
- Try different ways of handling missing values, instead of just imputing the most common value or 0. Tyr handling missing values with predictive models instead of imputing missing values with most common value, train models to predict missing values based on other features. 
- Try balancing techniques (like SMOTE), since some of the categories are rare and there's imbalance in the dataset (for example there are only around 200 VIP passengers compared to overall 8000). Downsample or upsample to balance the dataset and avoid model bias toward majority classes.
- Compare model performance on different subsets. Does the model perform better for certain groups (e.g., VIP vs. non-VIP, different decks, different spending levels)? Check if the model has bias toward specific demographics.
- Try more different modeling methods: K-Nearest Neighbors, boosting techniques like XGBoost, LightGBM.
- Do feature selection and identify, which features contribute most and remove redundant ones.
- Instead of grid search or Randomized Search, use Bayesian Optimization for smarter hyper parameter tuning.
