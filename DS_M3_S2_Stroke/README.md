# Stroke Prediction Project

## Introduction

Stroke is a life-threatening condition that occurs when blood supply to the brain is blocked or a blood vessel in the brain bursts, leading to potential brain damage, disability, or death. Quick and accurate stroke prediction can significantly improve patient outcomes by enabling timely preventive measures. This project aims to develop a machine learning model to predict the likelihood of a stroke based on patient data. The dataset used for this project is publicly available on Kaggle (https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset/data), and predictions from the model can be used to assess stroke risk in future patients.

**Dataset information**

The dataset contains 5,110 patient records with 12 features, including demographic information (e.g., gender, age), medical conditions (e.g., hypertension, heart disease), lifestyle factors (e.g., smoking status), and health metrics (e.g., BMI, glucose levels). The dataset has some missing values, especially in the BMI feature.

**Project**

Stroke Prediction Dataset is used for Gradient Boosted Trees & Feature Engineering project of Machine Learning module sprint 2. Data analysis is done using python and pandas library. Modeling is done using scikit-learn, lightgbm and xgboost. For visualization matplotlib and seaborn libraries were used. The project is done using Jupyter notebooks (4.2.4).

The project is done using python (version 3.11.4), numpy (2.0.1), seaborn (0.13.2), matplotlib (3.9.1), missingno (0.5.2), pandas (2.2.2), imbalanced-learn (0.12.3), lightgbm (4.5.0), scikit-learn (1.5.1), statsmodels (0.14.2), scipy (1.14.0), xgboost (2.1.1), Flask (3.0.3), joblib (1.4.2) and requests (2.32.3) libraries. 

**Project Objectives**

The goal of this project is to develop a machine learning model that predicts whether a patient is at risk of having a stroke. The project follows the steps below:

- Exploratory Data Analysis (EDA) – To gain insights into the data and explore relationships between features and stroke.
- Feature Engineering & Hypothesis Testing – To investigate the impact of specific features (age, BMI, gender) on stroke occurrence using statistical methods.
- Modeling & Hyperparameter Tuning – To build and evaluate machine learning models with a focus on recall as the primary performance metric.
- Model Evaluation – To compare model performance against a baseline and select the best model for deployment.
- The best model was deployed using your own computer as a server.

# Results of exploratory data analysis

We observed that stroke incidence increases significantly with age. There are also tendencies for higher average glucose to be causing higher chances for strokes. Patients with hypertension, heart disease, and those who are self-employed showed a higher likelihood of stroke. Additionally, formerly smoked and married patients tend to be at higher risk, likely due to their older age.

There is high correlation between marriage and age, and moderate correlation between age and self-employment work type and formerly smoked status. There is correlation between having a stroke and age. There is also weak correlation between stroke hypertention, heart disease and being married. Rest of features have very weak correlation to having a stroke stroke.

# Results of hypothesis testing

BMI and Age: A t-test revealed significant differences in BMI and age between stroke and non-stroke patients (p < 0.0167). Patients with higher BMI and older age are at a greater risk.
Gender: A Chi-square test indicated no statistically significant difference between males and females in stroke incidence, suggesting that both genders are equally susceptible.

# Modeling

Majority of the patients did not suffer from stroke in this dataset (95.13%). The goal of the model is to have as high as possible recall, as we prioritize identifying as many high-risk stroke patients as possible.

We trained several machine learning models: Random Forest, XGBoost, LightGBM, and K-Nearest Neighbors.

Baseline Performance: A dummy model yielded a recall of 0.52.

Best Model: XGBoost was chosen as the best model with a recall of 0.80, significantly outperforming the baseline.

# Suggestions for improvement

- Provide visualizations for the model logic.
- Extend the Flask app by deploying it on a web platform where patient data could be entered and receive stroke risk predictions.
- Perform feature selection to remove redundant or irrelevant features.
- Implement binning for continuous features.
- Experiment with removing outliers, to check their impact on model robustness.
- Develop more sophisticated imputation techniques for missing BMI values by using age, gender, and glucose levels as predictors.
- Separate models for age groups as there is strong correlation between age and stroke.
