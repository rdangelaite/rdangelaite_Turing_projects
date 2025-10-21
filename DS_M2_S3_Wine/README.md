# Red Wine Quality Dataset

## Introduction

The origins of wine can be traced back to 6000 BC from the country of Georgia. In 2022, wine consumption worldwide was estimated to amount to 232 million hectoliters (https://www.statista.com/statistics/232937/volume-of-global-wine-consumption/). This is dataset about red wine, which is made from dark-colored grape varieties. The red color of the wine is coming from anthocyan pigments present in the skin of the grape. Much of the red wine production process involves extraction of color and flavor components from the grape skin (https://en.wikipedia.org/wiki/Red_wine). 

**Dataset information**

This is dataset taken from kaggle (https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009?resource=download).

The two datasets are related to red and white variants of the Portuguese "Vinho Verde" wine. For more details, consult the reference [Cortez et al., 2009]. Due to privacy and logistic issues, only physicochemical (inputs) and sensory (the output) variables are available (e.g. there is no data about grape types, wine brand, wine selling price, etc.).

These datasets can be viewed as classification or regression tasks. The classes are ordered and not balanced (e.g. there are much more normal wines than excellent or poor ones).

**Vinho Verde** is not a grape variety, it is a DOC (denominação de origem controlada, the system of protected designation of origin from Portugal) for the production of wine. The name means "green wine," but translates as "young wine", with wine being released three to six months after the grapes are harvested. Majority of Vinho Verde wines are wine but they also also produce rose and red wines. The Vinho Verde red wines usually have red color and a fruity flavor with the tasting notes of pepper, peony, and sour plum. (Source: https://en.wikipedia.org/wiki/Vinho_Verde)

**Project**

Red Wine Quality dataset is used for Statistical Modeling project of Data Analysis module sprint 3. Data analysis is done using python and pandas library. For visualization matplotlib and seaborn libraries were used. The project is done using Jupyter notebooks (4.0.6).

The project is done using python (version 3.11.4), seaborn (0.12.2), matplotlib (3.8.0), pandas (2.0.3), sklearn (1.3.0), statsmodels (0.14.1) and scipy (1.11.2) libraries.

**Plan**

First, I will do exploratory data analysis, look into wine features.

Second, I will look into three questions: 
* Do chloride levels differ between depending on wine quality?
* Do alcohol levels differ between quality 5 and 6 wines?
* Does pH differ between quality 4 and 7 wines?
And I will try to answer them using hypothesis testing.

Third, I will create few models:
* To predict wine quality using features in the dataset, using logistic regression for classification;
* Linear regression model to predict alcohol content in the wine using rest of the features.

**Dashboard**

This is a link to my created dashboard for this project:
https://lookerstudio.google.com/u/0/reporting/c062b7be-afee-4c1e-9b63-f9c92a4c4645

# Summary of findings

- Some of the features measured in the red wine, have high correlations: fixed acidity with citric acid and density - they positively correlated. Total sulfur dioxide and free sulfur dioxide are also positively correlated. pH is negatively correlated with fixed acidity and citric acid. Volatile acidity is negatively correlated with citric acid, and alcohol is negatively correlated with density.
- Volatile acidity does not seem to correlated with alcohol in any way. We can see a slight tendency for higher quality wines to have higher alcohol content and lower volatile acidity.
- Three hypothesies were tested and here are the results:
  - We can see that there is no statistically significant difference between chloride levels between different quality wines, except for quality 7 and quality 5 wines.
  - The alcohol levels in quality 6 wines tends to be higher compared to quality 5 wines.
  - There is statistically significant difference between quality 4 and 7 wine's pH levels. The pH levels in quality 7 wines tend to slightly higher.
- Logistic regression models were used to classify wines into different qualities:
  - Models to clasify wines to premium (7 or 8 quality) and premium had around 90% accuracy and best performed when all of the features were used.
  - Models to classify wines into three different qualities: low (3 and 4 quality), medium (5 and 6) and high (7 and 8), also performed better when all of the features were used instead of just 4, but testing results were close. The model also failed to clasify wines into low and high qualities and tended to clasify most of wines as medium quality.
- Linear regression model was used to predict alcohol levels in the wine. 3 models were created – model 1 used all features, model 2 just 4 and model 3 used all features and data without outliers. The best at predicting was model 3, as it had lowest AIC score and residuals, however it is unknown how it would perform on real data with outliers. Therefore, model 1 should be overall best from all three tested.

# Suggestions for improvement

- Try more different feature combinations for models to find out if there are any which perform better without all of the features. 
- Investigate sulphate feature more as there is not much information about it online. 
- Make a training/testing sets for linear model. 
- Better visuals for confusion matrixes and models.
- Make more scatterplots for features (how they depend on one another).
- Improve model for classifying wines into three cathegories - low, medium and high as it tends to classify wines only as medium quality.

# Requirements

- Download the data from Red Wine Quality.
- Load the data using Pandas.
- Perform exploratory data analysis. This should include creating statistical summaries and charts, testing for anomalies, checking for correlations and other relations between variables, and other EDA elements.
- Perform statistical inference. This should include defining the target population, forming multiple statistical hypotheses and constructing confidence intervals, setting the significance levels, conducting z or t-tests for these hypotheses.
- Apply linear machine learning models to predict the quality column using the other 11 features. This should include the analysis of model selection using the statistical significance of each feature, R-squared, at least one popular information criteria, and other methods.
- Apply linear machine learning models to predict the alcohol column using the other 11 features. This should include the analysis of model selection using the statistical significance of each feature, R-squared, at least one popular information criteria, and other methods.
- Create a dashboard using Looker Studio or another BI tool e.g. Tableau with at least three different types of charts.
- Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
- Provide suggestions about how your analysis can be improved.

## Evaluation Criteria

- Adherence to the requirements. How well did you meet the requirements?
- Depth of your analysis. Did you just skim the surface or did you explored the dataset in depth?
- Visualization quality. Did you use charts effectively to visualize patterns in the data? Are your visualizations properly labeled? Did you use colors effectively? Did you adhere to the principle of proportional ink?
- Code quality. Was your code well-structured? Did you use the appropriate levels of abstraction? Did you remove commented out and unused code? Did you adhere to the PEP8?
- Code performance. Did you use the suitable algorithms and data structures to solve the problems?
