# Ultimate 25k+ Matches Football Database - European

## Introduction

Football (or soccer) has a long history. Football in its current form arose in England in the middle of the 19th century.

The most admitted story tells that the game was developed in England in the 12th century. In this century, games that resembled football were played on meadows and roads in England. Besides from kicks, the game involved also punches of the ball with the fist. This early form of football was also much more rough and violent than the modern way of playing.

It took, however, long time until the features of today’s football had been taken into practice. For a long time there was no clear distinction between football and rugby. There were also many variations concerning the size of the ball, the number of players and the length of a match.

The game was often played in schools and two of the predominant schools were Rugby and Eton. At Rugby the rules included the possibility to take up the ball with the hands and the game we today know as rugby has its origin from here. At Eton on the other hand the ball was played exclusively with the feet and this game can be seen as a close predecessor to the modern football. 

Another important event in the history of football came about in 1863 in London when the first Football association was formed in England. It was decided that carrying the ball with the hands wasn't allowed. The meeting also resulted in a standardization of the size and weight of the ball. A consequence of the London meeting was that the game was divided into two codes: association football and rugby. (Source: https://www.footballhistory.org/)

**Dataset information**

This is dataset taken from kaggle (https://www.kaggle.com/datasets/prajitdatta/ultimate-25k-matches-football-database-european).

The ultimate Soccer database for data analysis and machine learning. What you get:
- +25,000 matches
- +10,000 players
- 11 European Countries with their lead championship
- Seasons 2008 to 2016
- Players and Teams' attributes* sourced from EA Sports' FIFA video game series, including the weekly updates - - Team line up with squad formation (X, Y coordinates)
- Betting odds from up to 10 providers
- Detailed match events (goal types, possession, corner, cross, fouls, cards etc…) for +10,000 matches


**Project**

Ultimate 25k+ Matches Football Database -European dataset is used for Data analysis capstone project of Data Analysis module sprint 4. Data analysis is done using python and pandas library. For visualization matplotlib and seaborn libraries were used. The project is done in Jupyter notebooks (4.1.2).

The project is done using python (version 3.11.4), duckdb (0.9.1), seaborn (0.12.2), matplotlib (3.7.3), pandas (2.0.3), plotly (5.17.0), sklearn (1.3.0), statsmodels (0.14.1), imlearn (0.0) and scipy (1.11.2) libraries.

**Plan**

Firstly, all of the data in the tables will be explored, in order find out which leagues are in which countries, which leagues score the most/fewest goals, who are the top scorers in each team and league, and other points.

Second, few hypotheses will be tested to try and answer questions such as is there such a thing as home advantage? Do taller players have higher overall rating compared to short ones?

Lastly, models will be created to try and predict how many goals each team will make in each match and who will win? Models will be made using only Spain LIGA BBVA league data from seasons 2009/2010, 2010/2011, 2011/2012, 2013/2014, 2014/2015 to predict outcomes in season 2015/2016.

**Dashboard**

Link to dashboard: https://lookerstudio.google.com/reporting/a0665545-904c-42cb-a48f-09e180ee0841

# Summary

- There are 11 leagues in this dataset from 10 countries – two of the leagues are in the UK. 
- In total the dataset has 285 different teams and 11060 players.
- Top three highest rating players are Leonel Messi, Christiano Ronaldo and Franck Ribery.
- Match table has seasons from 2008/2009 to 2015/2016.
- Most goals scored by a team in a match was 10 and it happened twice: in season 2010/2011 Netherlands Eredivisie league in a match PSV vs Feyenoord, PSV scored 10 goals, and in Spain LIGA BBVA in season 2015/2016 in a match Real Madrid CF vs Rayo Vallecano, Real Madrid CF scored 10 goals, whole Rayo Vallecano scored only two.
- Most goals overall were scored in Spain LIGA BBVA, however Netherlands Eredivisie league has more goals on average per match.
- Most goals were made by Lionel Messi, closely followed by Cristiano Ronaldo. In third place by overall amount of goals is Zlatan Ibrahimovic.
- According to the dataset, there is home advantage, as home team wins 46% of the time, compared to away team – 29%.
- No difference between tall and short players overall scores found.
- Linear regression model was used to predict how many goals each team – away and home – will make each game. Models never predict 0 goals for any of the games, therefore it performance is lacking. 
- Logistic model was used to predict outcome of the match, using away and home teams attributes. Model had several different versions which should be selected depending on needs: if we need to recall as many home victories as possible, versions 1 and 3 should be used. If we wish to try and predict if the match is a draw, home or away victory, versions 2 or 4 will do a better job.

# Suggestions for improvement

- Draw separate map for UK premier leagues, as there are two of them, or find a way to separate UK into countries and have Scotland and England in the map.
- Explain team attributes. Explain more of player attributes.
- Statistics for average team rating over the year.
- For team categorical attributes and numerical attributes graphs make better names.
- Add an interactive radar plot where one could chose a team to check their attributes.
- Remove duplicate entries in team_att, team, and player_att tables for better statistics.
- Include description how betting odds are calculated.
- Include player position analysis.
- Which minute goals were made and by which team.
- Which players made most assists.
- Top scoring team per season and overall.
- Top scoring player per season.
- Average goals per match for players.
- Correlations between different betting companies.
- Use player attributes for prediction models.
- Use team attributes instead of their differences for linear prediction model.
- Include waterfall plots for models.
- Categorize games into 0, 1, 2 and 3 or more goals and use logistic regression model to predict how many goals will be made. 

# Requirements

- Perform data cleaning and feature engineering. Work with features - handle missing data if needed, use SQL and Pandas functions to create other additional features.
- Perform exploratory data analysis. Describe the data with basic statistical parameters - mean, median, quantiles, etc. Use parameters that give you the most important statistical insights of the data. Grouping the data and analyzing the groups - using SQL or Pandas aggregate methods. Visualize the data - you can use line, scatter, histogram plots, density plots, regplots, etc.
- Perform statistical inference. Raise and test statistical hypotheses. Set appropriate significance levels and create confidence intervals for the variables of interest.
- Train linear machine learning models and use them for forecasting. Choose and use appropriate metrics to measure your models' performance.
- Create a dashboard using Looker Studio or another BI tool e.g. Tableau with at least three different types of charts.
- Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
- Present the project - the data, methods, and results.
- Provide suggestions about how your analysis can be improved.

## Bonus Challenges

As a data scientists you will spend significant amount of your time learning new things. Sometimes you will do that for fun, but most of the time you will have an urgent problem and you will need to quickly learn some new skill to be able to solve it. It is very important to gradually build this skill - it is extremely valuable for all data scientists. The bonus challenges are designed to simulate these types of situations. These challenges require you to do something that we haven't covered in the course yet. Instead of trying to do all of the bonus challenges, concentrate on just one or two and do them well. All of the bonus challenges are optional - no points will be deducted if you skip them.

- Use cross validation, information criteria, and/or other methods to make sure that the models are specify your models correctly.
- Try dimensionality reduction algorithm (e.g. PCA, t-SNE, Autoencoder).
- Try clustering your data.
- Try a nonlinear machine learning model to explain relationships between features and predict new values.

# Evaluation Criteria

- Adherence to the requirements. How well did you meet the requirements?
- Depth of your analysis. Did you just skim the surface or did you explored the dataset in depth?
- Visualization quality. Did you use charts effectively to visualize patterns in the data? Are your visualizations properly labeled? Did you use colors effectively? Did you adhere to the principle of proportional ink?
- Code quality. Was your code well-structured? Did you use the appropriate levels of abstraction? Did you remove commented out and unused code? Did you adhere to the PEP8?
- Code performance. Did you use the suitable algorithms and data structures to solve the problems?
- Delivery of the presentation. How clear are your reasoning and explanations?
- Bonus challenges. Have you put extra effort to do one or more of the bonus challenges (no points will be deducted if you skip them)?

