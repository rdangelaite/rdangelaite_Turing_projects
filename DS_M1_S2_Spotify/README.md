# Top 50 Spotify Tracks of 2020

## Analysis of Top 50 Spotify tracks of 2020 using python and pandas.

Analysis was done using pandas package (version 2.0.3) and matplotlib (version 3.7.2) in Jypyter notebooks (JupyterLab Version 4.0.3). Python version 3.11.4.

The data for the project was obtained from Kaggle Top 50 Spotify Tracks- 2020 (https://www.kaggle.com/datasets/atillacolak/top-50-spotify-tracks-2020?select=spotifytoptracks.csv)

# Summary

As expected there are 50 songs in the top 50 song list of 2020. The dataset has 16 different features. Data was checked for missing and duplicated values. Also the outlier values were checked. There was 50% of songs with outlier features, however they were not removed from data analysis, as the data set is small and there are strict rules for creating music. There are 40 different artists in the list of whose 7 appeared more than once in list. Top 50 songs features 45 different albums, of which 4 appeared more than once. The most popular song was Blinding lights by The Weeknd.

Overall, songs with higher loudness score seems to be more popular as there are more songs with higher loudness score (19 songs with loudness score higher than -5 dB), than with lower loudness score in the top 50 (9 songs with loudness lower than -8 dB). Songs with high danceability are popular as well: 32 songs with danceability higher than 0.7, compared to only one which has low danceability (less than 0.4).

Pop and Hip-Hop are most popular genres in the top 50, both appearing 15 times in the list. However, pop is most popular genre with all of its subgenres added up (22 songs). Hip-Hop is the second most popular genre (16 songs). Some of the genres appeared only once in the top 50 list (without counting pop/hip-hop subgenres: disco, nu-disco, soft rock, trap, experimental, reggaeton). Some of the songs had few genres. Genres were separated and in total there were 22 different genres or 15 genres if we consider pop and hip-hop sub-genres not a different genre from pop/hip-hop.

For correlation analysis, monotonic associations between variables were assumed and Spearman's correlation was used. Monotonicity is "less restrictive" than that of a linear relationship. Energy and loudness are strongly correlated (0.75) and energy and acousticness are strongly negatively correlated (-0.66). There were no values which were not at least weakly correlated (since there were no correlations which were equal to 0). There were quite few features which were very weakly correlated with each other (correlation between -0,05 and 0,05, for example danceability and instrumentalness, duration and danceability, valence and tempo, liveness and tempo), however energy feature was missing from that list. As it stands, energy feature seems to be weakly or moderatelly correlated with all of the features.

For Pop, Hip-Hop/Rap, Dance/Electronic, and Alternative/Indie genres danceability, loudness and acousticness were compared. Alternative/Indie songs have lowest mean danceability and highest variation in it (0.662±0.211). However, they have very little variability in loudness between them (-5.421±0.775 dB). They also have much higher mean acousticness (0.584±0.204) score compared to rest of genres. Dance/Electronic songs have highest loudness score (-5.338±1.479 dB) and lowest acousticness score (0.099±0.096). Pop songs have highest variability in loudness score (-6.263±3.004 dB). Hip-hop/Rap songs have highest mean danceability out of these genres (0.766±0.085) and lowest loudness score (-6.918±1.892 dB). There are some outlier values with every high acousticness in Pop and Hip-Hop/Rap songs, but overall their mean acousticness is low (Pop – 0.315±0.308; Hip-Hop/Rap – 0.189±0.186).

## Suggestions what could be improved

More investigation regarding outliers. Perhaps they are not outliers at all, but are due to differences in genres. These outlier features might be also due to style differences of different artists. Investigate more songs from these genres. However, if outlier song is in top list, it might be good to understand what makes it popular.

Comparisons between songs, if top 50 list has more danceable and louder songs compared to another list of songs, for example top 1000.

Investigate duration preferences. How does length of songs compare to not so popular songs.

Are there any genres which are unusual to this top 50 list? Compare it to other year top 50 lists.

Sometimes artists release stand alone songs without any albums. Investigate if there are any in the top 50 list, and how many if there are.

It would be nice to know how many times the songs were listened to. Also, investigating, for example, how many minutes each song was listened to might give clearer comparison if there is a huge difference between lengths of songs. Perhaps, there are artists which has more than one song in the top 50, and total listening time for their songs is higher, than other artists who is higher, but has only one song.

Also are there many unique individuals who are listening to a song? Perhaps, it is few individuals who listen to the song over and over again.

**The following are context and requirements for the project.**

## Context

Imagine that you are a data analyst working for Spotify. Your team is responsible for content analysis, and in this quarter, you have decided to analyze Spotify's top hits and quantify what makes a hit song. Your team's product manager has many ideas and prepared a list of questions (requirements) that she wants you to get answers to. After reviewing the list of over 20 questions, you are not in a good mood - you'll have to work a couple of days to get all the answers. Luckily, a few days ago, an experienced data scientist working in your team queried the top 50 tracks for her machine learning project and agreed to share the data with you. This is a significant help - your SQL skills are not too sharp yet, and you don't yet know where to find all the relevant tables in your data warehouse. With this dataset, you are confident that you'll be able to answer all your PM's questions and maybe even look into some things that she didn't ask for.

### Objectives for this Part

* Practice working with data from Kaggle.
* Practice performing basic EDA.
* Practice reading data, performing queries and filtering data using Pandas.

## Requirements

1. Download the data from Spotify Top 50 Tracks of 2020 dataset.
2. Load the data using Pandas.
3. Perform data cleaning by:
   - Handling missing values.
   - Removing duplicate samples and features.
   - Treating the outliers.
4. Perform exploratory data analysis. Your analysis should provide answers to these questions:
   - How many observations are there in this dataset?
   - How many features this dataset has?
   - Which of the features are categorical?
   - Which of the features are numeric?
   - Are there any artists that have more than 1 popular track? If yes, which and how many?
   - Who was the most popular artist?
   - How many artists in total have their songs in the top 50?
   - Are there any albums that have more than 1 popular track? If yes, which and how many?
   - How many albums in total have their songs in the top 50?
   - Which tracks have a danceability score above 0.7?
   - Which tracks have a danceability score below 0.4?
   - Which tracks have their loudness above -5?
   - Which tracks have their loudness below -8?
   - Which track is the longest?
   - Which track is the shortest?
   - Which genre is the most popular?
   - Which genres have just one song on the top 50?
   - How many genres in total are represented in the top 50?
   - Which features are strongly positively correlated?
   - Which features are strongly negatively correlated?
   - Which features are not correlated?
5. How does the danceability score compare between Pop, Hip-Hop/Rap, Dance/Electronic, and Alternative/Indie genres?
6. How does the loudness score compare between Pop, Hip-Hop/Rap, Dance/Electronic, and Alternative/Indie genres?
7. How does the acousticness score compare between Pop, Hip-Hop/Rap, Dance/Electronic, and Alternative/Indie genres?
8. Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results you got, and what these results mean.
9. Provide suggestions about how your analysis can be improved.
    

