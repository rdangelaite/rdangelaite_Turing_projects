# Home Credit Default Risk Dataset Project

Many people struggle to get loans due to insufficient or non-existent credit histories. They are often excluded from traditional lending systems and are especially vulnerable to exploitation by unregulated, untrustworthy or predatory lenders.

Home Credit strives to broaden financial inclusion for the unbanked population by providing a positive and safe borrowing experience. By leveraging alternative data sources—such as telco usage, payment behavior, and transaction history—they aim to responsibly extend credit access to underserved populations. Their goal is to ensure that loans are offered only to individuals who can repay them, and to structure the terms in a way that promotes long-term financial health.

While Home Credit is currently using various statistical and machine learning methods to make these predictions, they challenge data scientists and machine learning practitioners to push these techniques even further. Doing so will ensure that clients capable of repayment are not rejected and that loans are given with a principal, maturity, and repayment calendar that will empower their clients to be successful. (https://www.kaggle.com/competitions/home-credit-default-risk/overview)

*Project - a brilliant startup idea*

Motivated by the real-world impact of such systems, a friend and I decided to turn this into a startup idea: offer credit risk evaluation as a service for retail banks. Like many successful teams, we divided responsibilities:
- My friend is responsible for sales and operations,
- while I am responsible for everything product-related, from planning and data analysis to building robust ML-driven solutions.

As a first step, I downloaded and explored the Home Credit dataset to begin developing a proof of concept.
We agreed to develop a portfolio of machine learning models. This way, when we meet with potential banking partners, we can demonstrate flexibility, adaptability, and a deep understanding of credit risk from multiple perspectives.

**Dataset information**

Data is taken from Kaggle https://www.kaggle.com/competitions/home-credit-default-risk/data

**Project**

Home Credit Default Risk competition dataset is used for Machine Learning Capstone Project project of Machine Learning module sprint 4. Data analysis is done using python and pandas library. Modeling is done using scikit-learn and optuna. For visualization matplotlib and seaborn libraries were used. The project is done using Jupyter notebooks (4.2.4). The models were deployed on Google Cloud, using Docker.

The project is done using python (version 3.11.4), numpy (2.0.1), pandas (2.2.3), seaborn (0.13.2), matplotlib (3.9.1), missingno (0.5.2), duckdb (1.0.0), dill (0.4.0), fastapi (0.115.2), uvicorn (0.31.1), scikit-learn (1.5.1), xgboost (3.0.5), lightgbm (4.5.0), optuna (4.4.0), scipy (1.14.0) and statsmodels (0.14.2) libraries.

**Project goal**

Project Goal: Build and Compare Multiple ML Models

**Plan**

The project includes:
- Exploratory data analysis.
- Engineering features.
- Checking if the features are statistically important using hypothesis testing.
- Building and evaluating multiple models.
- Deploying machine learning models.

**Structure**
The project is broken into several notebooks:
- Part 1 - Home Credit Project: exploring application data.
- Part 2 - Analysis of Supplementary Data: exploring additional data provided.
- Part 3 - All Data and Statistical Inference: connecting all of the data, correlation, hypothesis testing.
- Part 4 - Model training (XGBoost & LightGBM) and cloud deployment

## Key Findings & Insights

**Part 1 – Application data**
In this section, application data was explored in depth.
Missing data patterns were examined, feature distributions were visualized, correlations were evaluated, and outliers were identified.

Although no strong correlations with the target were found, several notable tendencies appeared:
- Younger applicants had higher default rates.
- Clients with short employment histories struggled more often with repayment.
- Manual and service occupations showed higher risk.
- External risk scores had negative correlation with default, indicating strong predictive power.

**Part 2 – Supplementary Data**
Supplementary datasets were aggregated by client ID.
Most features were heavily skewed, non-normal, and contained many outliers.

**Part 3 – Correlation Analysis & Statistical Inference**
Key insights:
- Credit card repayment patterns, cash withdrawals, and high balances were strong predictors of risk.
- The main application data contained the most important stability-related predictors.
- Older, more educated, and stably employed borrowers were consistently less risky.
- External risk scores were among the strongest features overall.
- Behavioral datasets (Installments, Bureau, Credit Card, POS) were statistically significant and highly predictive.

Statistical tests applied:
- Chi-square test to evaluate categorical feature importance
- Kolmogorov–Smirnov test to check normality
- Mann–Whitney U test for non-normal numerical distributions

These tests confirmed that:
- Strong predictors relate to client stability, socioeconomic status, and financial reliability.
- Weak predictors (e.g., rare document flags or timing features) can be deprioritized.

**Part 4 – Modeling & Deployment**
XGBoost and LightGBM models were trained and deployed on Google Cloud.
API endpoint: https://fastapi-models-166989861873.europe-central2.run.app

While both models outperformed the baseline, they did not reach the target of higher accuracy than 0.92.
Nevertheless, the project successfully demonstrated a complete end-to-end ML workflow:
- Data processing
- Feature engineering
- Statistical analysis
- Model selection
- Cloud deployment

The workflow is scalable and ready for future iterations and improvements.

**Testing the API**

A test script (test_api.py) is provided to evaluate the deployed models using one selected dataset row.
The required input feature order is listed in the README for reference.

Input order: ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY', 'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'APARTMENTS_AVG', 'BASEMENTAREA_AVG', 'YEARS_BEGINEXPLUATATION_AVG', 'YEARS_BUILD_AVG', 'COMMONAREA_AVG', 'ELEVATORS_AVG', 'ENTRANCES_AVG', 'FLOORSMAX_AVG', 'FLOORSMIN_AVG', 'LANDAREA_AVG', 'LIVINGAPARTMENTS_AVG', 'LIVINGAREA_AVG', 'NONLIVINGAPARTMENTS_AVG', 'NONLIVINGAREA_AVG', 'APARTMENTS_MODE', 'BASEMENTAREA_MODE', 'YEARS_BEGINEXPLUATATION_MODE', 'YEARS_BUILD_MODE', 'COMMONAREA_MODE', 'ELEVATORS_MODE', 'ENTRANCES_MODE', 'FLOORSMAX_MODE', 'FLOORSMIN_MODE', 'LANDAREA_MODE', 'LIVINGAPARTMENTS_MODE', 'LIVINGAREA_MODE', 'NONLIVINGAPARTMENTS_MODE', 'NONLIVINGAREA_MODE', 'APARTMENTS_MEDI', 'BASEMENTAREA_MEDI', 'YEARS_BEGINEXPLUATATION_MEDI', 'YEARS_BUILD_MEDI', 'COMMONAREA_MEDI', 'ELEVATORS_MEDI', 'ENTRANCES_MEDI', 'FLOORSMAX_MEDI', 'FLOORSMIN_MEDI', 'LANDAREA_MEDI', 'LIVINGAPARTMENTS_MEDI', 'LIVINGAREA_MEDI', 'NONLIVINGAPARTMENTS_MEDI', 'NONLIVINGAREA_MEDI', 'FONDKAPREMONT_MODE', 'HOUSETYPE_MODE', 'TOTALAREA_MODE', 'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE', 'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21', 'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR']

# Conclusion
This project covered the full credit-risk prediction pipeline – from exploring the data to deploying machine learning models in the cloud.

The analysis showed that stability-related features, external scores, and behavioral patterns are strong indicators of repayment ability.
The deployed models demonstrate functional predictive capability, even if performance has room for improvement.

The work lays a solid foundation for building a production-ready credit-risk scoring system and aligns well with the proposed startup idea.

## Suggestions For Improvement

- Try additional machine learning models beyond XGBoost and LightGBM (e.g., CatBoost, Random Forest, or Neural Networks).
- Engineer new features that could capture deeper relationships in the data.
- Experiment with training models using all available features (without prior selection via hypothesis testing or correlation filtering) to compare performance.
- Utilize more powerful computing resources to allow for larger-scale model training and hyperparameter tuning.
- Optimize hyperparameters using automated search techniques such as Optuna or Bayesian optimization.
- Apply advanced feature selection.
- Improve the data preprocessing and imputation pipeline for handling missing or skewed data more robustly.
- Consider building an ensemble or stacking model to combine predictions from multiple classifiers.
- Perform a more in-depth analysis of the features.