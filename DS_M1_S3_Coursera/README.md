# Coursera course dataset 

## Analysis of Coursera course dataset using python and pandas

Analysis was done using pandas (version 2.0.3), seaborn (version 0.12.2), matplotlib (version 3.7.2) and ipywidgets(version 8.1.0) in Jypyter notebooks (JupyterLab Version 4.0.3). Python version 3.11.4.

The data is scrapped from Coursera official web site and is obtained from kaggle website (https://www.kaggle.com/datasets/siddharthm1698/coursera-course-dataset). Article about the dataset generation : https://medium.com/analytics-vidhya/web-scraping-and-coursera-8db6af45d83f.

All of findings and data can be found in the notebook. 

## Objectives and requirements

**Objectives for this Part**

1. Practice working with data from Kaggle.
2. Practice performing basic EDA.
3. Practice visualizing data with Matplotlib & Seaborn.
4. Practice reading data, performing queries and filtering data using Pandas.

**Requirements**

1. Download the data from Coursera Course Dataset.
2. Load the data using Pandas.
3. Perform data cleaning.
4. Perform exploratory data analysis.
5. Provide clear explanations in your notebook. Your explanations should inform the reader what you are trying to achieve, what results did you get, and what these results mean.
6. Provide suggestions about how your analysis can be improved.

## Summary

* The more courses organization has, the more students they have.
* Course ratings and student enrollement count does not seem to be related.
* Less students the course has the more varied it's rating is.
* There is tendency for average amount of students to decrease in comparison with course difficulty.
* Python courses are more popular than random courses from the dataset

## Findings

There are 891 courses in the Coursera course dataset. It has 6 different features, of which 4 are categorical and 2 are numerical. Categorical features: course title, course organization, course certificate type and course difficulty. Numerical features: course rating and course students enrolled. There are in total 154 different organizations which prepared the courses for Coursera. 

**Organizations in the dataset stats**

Majority of the orgnizations have more than one course (105 out of 154, or 68.18%).

We can see that top 2 most attended organizations are same as ones with most courses, just switched in places: University of Pennsylvania (5,501,300 or 6.82% of all students) and University of Michigan (7,437,700, 9.22%%). There were 7 organizations in top 10 most courses, which are also in top 10 most popular courses. Obviously, having more courses makes your organization more popular to students, but it is not always the case. More than half of students (53%) are in top 10 most popular course organizations. Neither most popular or with most courses organizations are in top highest or lowest rated overall.

There is strong corelation between courses count and how many students have enrolled. It is as expected, as the more courses the organization has, the more chances the student will chose it. There is also weak negative correlation between rating and how many courses has the organization released, which means that there is a tendency to have lower average rating for courses, when you have a lot of them. Students either have higher expectations for these courses, or quantity does not mean quality. From the graphs we saw see that there is some tendencies for organizations with a lot of students and courses to get ratings around 4.7. Ratings for organizations with less courses and students are much more varied.

**Courses stats**

TThe most popular course is Machine Learning by Stanford University (3,200,000 students). The most popular course is attended more than 10 times than on average (average per course students 90,552±6095). We can see that the most popular course is not from most popular organization but it is rated higher than average course (course rating 4.9, when average course ratings are about 4.67±0.005).

Highest rated course and least attended one is El Abogado del Futuro: Legaltech y la Transformación Digital del Derecho, comes from Universidad Austral in Argentina. Course name translated from Spanish is The Lawyer of the Future: Legaltech and the Digital Transformation of Law. It has low amount of students enrolled in it (1,500). The courses name seems to be very specific, it deals with law and tech, therefore it is not surprising that there is low amount of students enrolled in it.

Lowest rated course has just 3.3 rating (compared to 4.67±0.005 average ratings). However, even 140,000 students enrolled in it. That's more students than average (90,552±6095). Perhaps students were not able to get what they are promised from the course, were not pleased with the result or there also could be some reason why the course is highly attended and low rated.

Overall, it looks like there is no relation between course ratings and course students enrolled or relation is minimal. There is also a lot of courses with not that many students and very low count of courses with high amount of students enrolled (exponentially decreasing tendensies for amount of courses with high student enrollement). Most of course ratings seem to be distributed between 4 and 5. There seems to be tendensy to have high course ratings on Coursera. But having high attendance does not guarantee relativelly high course ratings.

**Grouping courses into groups stats**

The courses have 3 certificate types: course specialization and profecional certificate. Most of the courses certification type is course, around third is specialization typer and small percent grants profesional certificate.
Looking at the means according to each group, there seems to be more students enrolled on average in profesional certification course types. This might be due to coursera not having a lot of this type of courses. There are a lot more of specialization and course certificate type courses and the student has higher ability to chose one of courses if they are similar, whereas only 1.35% of courses are profesional ceritificate type and the student might not have luxury of chosing. Profesional certificate courses might also be popular due to their specifics – they seem to be prepared by big companies (like Google or IBM) and might be required to be accepted into the job or be done while in job.  Specialization courses have slightly lower ratings than the rest.

There are also 4 different course difficulty levels: beginner, intermediate, mixed and advanced. More than half of courses are beginner difficulty courses (54.66%). Intermediate and mixed difficulty courses are around 21% and there is only 2% of advanced difficulty courses.
Most of students on average tend to chose mixed rating courses. There is tendency for average amount of students to decrease in comparison with difficulty. Ratings also slightly decrease. Mixed difficulty courses have slightly higher rating than the rest.
Mixed course difficulty courses have highest median and also lowest ratings out of all difficulties. Beginner and intermediate difficulty courses have highest rated courses. Beginner, intemediate and advanced courses have similar ratings.

We can see that python courses have similar ratings as all the courses (courses with Python – 4.66±0.03, all courses 4.67±0.005 average ratings). Average student enrollment into python course is 189,312±56640, which is more than average (90,552±6095). Therefore, Python courses are more popular than a random course from the dataset.

## Suggestions for improvement

No information about how long courses are there. Perhaps low student enrollement in courses is related to the course being new, not because the course or topic is unpopular. To see relation of how frequently courses are updated and their ratings change overtime. Percentage of students finishing the course would be interesting to see. Also, how long on average did they take to finish the course. 

Separating courses into different sectors. Perhaps it could be done by smartly interpreting the course names.

There are courses in other languages than english. Checking statistics based on course language.

Running some statistics between groups, do they belong to same dataset or not. Is there a significant difference between them. Also grouping courses into groups according to both difficulty and course certificate type.

Improving interactive graph. Being able to type in your own keyword instead of chosing one provided in the key list. Being able to compare two groups, not just one group to the main dataset. Also including ability to chose between different difficulty levels and certification types.

