#!/usr/bin/env python
# coding: utf-8

# In[89]:


get_ipython().system('pip install opendatasets --upgrade  --quiet')


# In[236]:


import opendatasets as od


# In[237]:


od.download('stackoverflow-developer-survey-2020')


# In[238]:


import os


# In[239]:


os.listdir('stackoverflow-developer-survey-2020')


# 
# 
# - `README.txt` - Information about the dataset
# - `survey_results_schema.csv` - The list of questions, and shortcodes for each question
# - `survey_results_public.csv` - The full list of responses to the questions 
# 
# Let's load the CSV files using the Pandas library. We'll use the name `survey_raw_df` for the data frame to indicate this is unprocessed data that we might clean, filter, and modify to prepare a data frame ready for analysis.

# In[240]:


import pandas as pd


# In[322]:


survey_raw_df = pd.read_csv('stackoverflow-developer-survey-2020/survey_results_public.csv')


# In[324]:


survey_languages_df = pd.read_csv('countries-languages.csv')


# In[242]:


survey_raw_df


# The dataset contains over 64,000 responses to 60 questions (although many questions are optional). The responses have been anonymized to remove personally identifiable information, and each respondent has been assigned a randomized respondent ID.
# 
# Let's view the list of columns in the data frame. 

# In[243]:


survey_raw_df.columns


# In[244]:


schema_fname = 'stackoverflow-developer-survey-2020/survey_results_schema.csv'
schema_raw = pd.read_csv(schema_fname, index_col='Column').QuestionText


# In[245]:


schema_raw


# We can now use `schema_raw` to retrieve the full question text for any column in `survey_raw_df`.

# In[246]:


schema_raw['YearsCodePro']


# ###  Data preparation and cleaning

# While the survey responses contain a wealth of information, we'll limit our analysis to the following areas:
# 
# - Demographics of the survey respondents and the global programming community
# - Distribution of programming skills, experience, and preferences
# - Employment-related information, preferences, and opinions
# 
# Let's select a subset of columns with the relevant data for our analysis.

# In[247]:


selected_columns = [
    # Demographics
    'Country',
    'Age',
    'Gender',
    'EdLevel',
    'UndergradMajor',
    # Programming experience
    'Hobbyist',
    'Age1stCode',
    'YearsCode',
    'YearsCodePro',
    'LanguageWorkedWith',
    'LanguageDesireNextYear',
    'NEWLearn',
    'NEWStuck',
    # Employment
    'Employment',
    'DevType',
    'WorkWeekHrs',
    'JobSat',
    'JobFactors',
    'NEWOvertime',
    'NEWEdImpt'
]


# In[248]:


len(selected_columns)


# In[249]:


survey_df=survey_raw_df[selected_columns].copy()


# In[250]:


schema=schema_raw[selected_columns]


# In[251]:


survey_df.shape


# In[252]:


survey_df.info()


# Most columns have the data type `object`, either because they contain values of different types or contain empty values (`NaN`). It appears that every column contains some empty values since the Non-Null count for every column is lower than the total number of rows (64461). We'll need to deal with empty values and manually adjust the data type for each column on a case-by-case basis. 
# 
# Only two of the columns were detected as numeric columns (`Age` and `WorkWeekHrs`), even though a few other columns have mostly numeric values. To make our analysis easier, let's convert some other columns into numeric data types while ignoring any non-numeric value. The non-numeric are converted to `NaN`.

# In[253]:


survey_df.Age1stCode.unique()


# In[254]:


survey_df['Age1stCode']=pd.to_numeric(survey_df.Age1stCode,errors='coerce')


# In[255]:


survey_df.YearsCodePro.unique()


# In[256]:


survey_df['YearsCode']=pd.to_numeric(survey_df.YearsCode,errors='coerce')


# In[257]:


survey_df['YearsCodePro']=pd.to_numeric(survey_df.YearsCodePro,errors='coerce')


# In[258]:


survey_df.describe()


# There seems to be a problem with the age column, as the minimum value is 1 and the maximum is 279. This is a common issue with surveys: responses may contain invalid values due to accidental or intentional errors while responding. A simple fix would be to ignore the rows where the age is higher than 100 years or lower than 10 years as invalid survey responses. We can do this using the `.drop` method.

# In[259]:


survey_df.drop(survey_df[survey_df.Age < 10].index, inplace=True)
survey_df.drop(survey_df[survey_df.Age > 100].index, inplace=True)


# In[ ]:





# The same holds for `WorkWeekHrs`. Let's ignore entries where the value for the column is higher than 140 hours. (~20 hours per day)

# In[260]:


survey_df.drop(survey_df[survey_df.WorkWeekHrs>140].index,inplace=True)


# In[261]:


schema.Gender


# In[262]:


survey_df['Gender'].value_counts()


# In[263]:


survey_df['Age'].value_counts()


# In[264]:


import numpy as np


# In[265]:


survey_df.where(~(survey_df.Gender.str.contains(';', na=False)), np.nan, inplace=True)


# In[266]:


survey_df['Gender'].value_counts()


# We've now cleaned up and prepared the dataset for analysis. Let's take a look at a sample of rows from the data frame.

# In[267]:


survey_df.sample(10)


# ## Exploratory Analysis and Visualization
# 
# Before we ask questions about the survey responses, it would help to understand the respondents' demographics, i.e., country, age, gender, education level, employment level, etc. It's essential to explore these variables to understand how representative the survey is of the worldwide programming community. A survey of this scale generally tends to have some [selection bias](https://en.wikipedia.org/wiki/Selection_bias).
# 
# Let's begin by importing `matplotlib.pyplot` and `seaborn`.

# In[268]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### Country
# 
# Let's look at the number of countries from which there are responses in the survey and plot the ten countries with the highest number of responses.

# In[269]:


schema.Country


# In[270]:


survey_df.Country.nunique()


# We can identify the countries with the highest number of respondents using the `value_counts` method.

# In[271]:


survey_df.Country.value_counts()


# In[272]:


top_countries=survey_df.Country.value_counts().head(15)


# In[273]:


top_countries


# In[274]:


survey_df.Country.value_counts()


# In[275]:


plt.figure(figsize=(12,6))
plt.xticks(rotation=75)
plt.title(schema.Country)
sns.barplot(x=top_countries.index, y=top_countries)
plt.show;


# It appears that a disproportionately high number of respondents are from the US and India, probably because the survey is in English, and these countries have the highest English-speaking populations. We can already see that the survey may not be representative of the global programming community - especially from non-English speaking countries. Programmers from non-English speaking countries are almost certainly underrepresented.
# 
# Try finding the percentage of responses from English-speaking vs. non-English speaking countries. You can use [this list of languages spoken in different countries](https://github.com/JovianML/opendatasets/blob/master/data/countries-languages-spoken/countries-languages.csv).

# In[325]:


survey_languages_df


# In[330]:


def is_english_speaking(row):
    languages = row['Languages Spoken'].lower()
    return 'english' in languages


# In[331]:


survey_languages_df['English Speaking'] = survey_languages_df.apply(is_english_speaking, axis=1)


# In[332]:


survey_languages_df


# In[333]:


percentage_english_speaking = (survey_languages_df['English Speaking'].sum() / len(survey_languages_df)) * 100
percentage_non_english_speaking = 100 - percentage_english_speaking


# In[334]:


percentage_english_speaking


# In[336]:


percentage_non_english_speaking


# It is observed that percentage of responses from english speaking country is 48.8 % and that of non -speaking country is 51.5%.

# ### Age
# 
# The distribution of respondents' age is another crucial factor to look at. We can use a histogram to visualize it. 

# In[276]:


schema.Age


# In[277]:


survey_df.Age


# In[278]:


plt.figure(figsize=(12, 6))
plt.title(schema.Age)
plt.xlabel('Age')
plt.ylabel('Number of respondents')

plt.hist(survey_df.Age, bins=np.arange(10,80,5), color='purple');


# It appears that a large percentage of respondents are 20-45 years old. It's somewhat representative of the programming community in general. Many young people have taken up computer science as their field of study or profession in the last 20 years.
# 
# 

# In[338]:


def get_age_group(age):
    if age < 10:
        return 'Less than 10 years'
    elif age <= 18:
        return '10-18 years'
    elif age <= 30:
        return '18-30 years'
    elif age <= 45:
        return '30-45 years'
    elif age <= 60:
        return '45-60 years'
    else:
        return 'Older than 60 years'

# Apply the function to create a new column 'AgeGroup'
survey_df['AgeGroup'] = survey_df['Age'].apply(get_age_group)


# In[339]:


survey_df


# What is the most popular language among those who are 18-30 year old??

# In[340]:


df_18_30 = survey_df[survey_df['AgeGroup'] == '18-30 years']


# In[341]:


df_18_30


# In[342]:


language_counts = df_18_30.groupby(['AgeGroup', 'LanguageWorkedWith']).size().reset_index(name='Count')


# In[343]:


language_counts


# In[347]:


most_popular_language = language_counts.loc[language_counts['Count'].idxmax(), 'LanguageWorkedWith']


# In[348]:


most_popular_language


# ### Gender
# 
# Let's look at the distribution of responses for the Gender. It's a well-known fact that women and non-binary genders are underrepresented in the programming community, so we might expect to see a skewed distribution here.
# 

# In[ ]:





# In[279]:


schema.Gender


# In[280]:


gender_counts=survey_df.Gender.value_counts()


# In[281]:


gender_counts


# In[282]:


plt.figure(figsize=(12,6))
plt.title(schema.Gender)
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=180);


# Only about 7.7% of survey respondents who have answered the question identify as women or non-binary. This number is lower than the overall percentage of women & non-binary genders in the programming community - which is estimated to be around 12%. 
# 

# ### Education Level
# 
# Formal education in computer science is often considered an essential requirement for becoming a programmer. However, there are many free resources & tutorials available online to learn programming. Let's compare the education levels of respondents to gain some insight into this. We'll use a horizontal bar plot here.

# In[283]:


sns.countplot(y=survey_df.EdLevel)
plt.xticks(rotation=75);
plt.title(schema['EdLevel'])
plt.ylabel(None);


# It appears that well over half of the respondents hold a bachelor's or master's degree, so most programmers seem to have some college education. However, it's not clear from this graph alone if they hold a degree in computer science.
# 
# 

# In[286]:


ed_level_percentages = survey_df['EdLevel'].value_counts(normalize=True) * 100
plt.figure(figsize=(10, 6))
sns.barplot(x=ed_level_percentages.values, y=ed_level_percentages.index)
plt.title('Percentage of Respondents by Education Level')
plt.xlabel('Percentage')
plt.ylabel('Education Level')

plt.show()


# It turns out that 40% of programmers holding a college degree have a field of study other than computer science - which is very encouraging. It seems to suggest that while a college education is helpful in general, you do not need to pursue a major in computer science to become a successful programmer.
# 
# 

# In[287]:


schema.UndergradMajor


# In[290]:


survey_df.UndergradMajor.value_counts()*100/survey_df.UndergradMajor.count()


# In[292]:


undergrad_pct = survey_df.UndergradMajor.value_counts() * 100 / survey_df.UndergradMajor.count()

sns.barplot(x=undergrad_pct, y=undergrad_pct.index)

plt.title(schema.UndergradMajor)
plt.ylabel(None);
plt.xlabel('Percentage');


# In[ ]:





# It turns out that 40% of programmers holding a college degree have a field of study other than computer science - which is very encouraging. It seems to suggest that while a college education is helpful in general, you do not need to pursue a major in computer science to become a successful programmer.
# 
# 

# ### Employment
# 
# Freelancing or contract work is a common choice among programmers, so it would be interesting to compare the breakdown between full-time, part-time, and freelance work. Let's visualize the data from the `Employment` column.

# In[293]:


schema.Employment


# In[294]:


(survey_df.Employment.value_counts(normalize=True, ascending=True)*100).plot(kind='barh', color='g')
plt.title(schema.Employment)
plt.xlabel('Percentage');


# It appears that close to 10% of respondents are employed part time or as freelancers.
# 
# 
# 

# In[296]:


schema.DevType


# In[297]:


survey_df.DevType.value_counts()


# In[298]:


def split_multicolumn(col_series):
    result_df = col_series.to_frame()
    options = []
    # Iterate over the column
    for idx, value  in col_series[col_series.notnull()].iteritems():
        # Break each value into list of options
        for option in value.split(';'):
            # Add the option as a column to result
            if not option in result_df.columns:
                options.append(option)
                result_df[option] = False
            # Mark the value in the option column as True
            result_df.at[idx, option] = True
    return result_df[options]


# In[299]:


dev_type_df = split_multicolumn(survey_df.DevType)


# In[300]:


dev_type_df


# The `dev_type_df` has one column for each option that can be selected as a response. If a respondent has chosen an option, the corresponding column's value is `True`. Otherwise, it is `False`.
# 
# We can now use the column-wise totals to identify the most common roles.

# In[301]:


dev_type_totals = dev_type_df.sum().sort_values(ascending=False)
dev_type_totals


# As one might expect, the most common roles include "Developer" in the name. 
# 
# 

# #### Q: What are the most popular programming languages in 2020? 
# 
# To answer, this we can use the `LanguageWorkedWith` column. Similar to `DevType`, respondents were allowed to choose multiple options here.

# In[302]:


survey_df.LanguageWorkedWith


# First, we'll split this column into a data frame containing a column of each language listed in the options.

# In[303]:


languages_worked_df = split_multicolumn(survey_df.LanguageWorkedWith)


# In[304]:


languages_worked_df


# It appears that a total of 25 languages were included among the options. Let's aggregate these to identify the percentage of respondents who selected each language.

# In[305]:


languages_worked_percentages = languages_worked_df.mean().sort_values(ascending=False) * 100
languages_worked_percentages


# In[306]:


plt.figure(figsize=(12, 12))
sns.barplot(x=languages_worked_percentages, y=languages_worked_percentages.index)
plt.title("Languages used in the past year");
plt.xlabel('count');


# Perhaps unsurprisingly, Javascript & HTML/CSS comes out at the top as web development is one of today's most sought skills. It also happens to be one of the easiest to get started. SQL is necessary for working with relational databases, so it's no surprise that most programmers work with SQL regularly. Python seems to be the popular choice for other forms of development, beating out Java, which was the industry standard for server & application development for over two decades.
# 
# 

# #### Q: Which languages are the most people interested to learn over the next year?
# 
# For this, we can use the `LanguageDesireNextYear` column, with similar processing as the previous one.

# In[307]:


languages_interested_df = split_multicolumn(survey_df.LanguageDesireNextYear)
languages_interested_percentages = languages_interested_df.mean().sort_values(ascending=False) * 100
languages_interested_percentages


# In[308]:


plt.figure(figsize=(12, 12))
sns.barplot(x=languages_interested_percentages, y=languages_interested_percentages.index)
plt.title("Languages people are intersted in learning over the next year");
plt.xlabel('count');


# Once again, it's not surprising that Python is the language most people are interested in learning - since it is an easy-to-learn general-purpose programming language well suited for a variety of domains: application development, numerical computing, data analysis, machine learning, big data, cloud automation, web scraping, scripting, etc. We're using Python for this very analysis, so we're in good company!
# 
# 

# #### Q:  Which are the most loved languages, i.e., a high percentage of people who have used the language want to continue learning & using it over the next year?
# 
# While this question may seem tricky at first, it's straightforward to solve using Pandas array operations. Here's what we can do:
# 
# - Create a new data frame `languages_loved_df` that contains a `True` value for a language only if the corresponding values in `languages_worked_df` and `languages_interested_df` are both `True`
# - Take the column-wise sum of `languages_loved_df` and divide it by the column-wise sum of `languages_worked_df` to get the percentage of respondents who "love" the language
# - Sort the results in decreasing order and plot a horizontal bar graph

# In[309]:


languages_loved_df = languages_worked_df & languages_interested_df


# In[310]:


languages_loved_df


# In[312]:


languages_loved_percentages = (languages_loved_df.sum() * 100/ languages_worked_df.sum()).sort_values(ascending=False)


# plt.figure(figsize=(12, 12))
# sns.barplot(x=languages_loved_percentages, y=languages_loved_percentages.index)
# plt.title("Most loved languages");
# plt.xlabel('count');

# [Rust](https://www.rust-lang.org) has been StackOverflow's most-loved language for [four years in a row](https://stackoverflow.blog/2020/01/20/what-is-rust-and-why-is-it-so-popular/). The second most-loved language is TypeScript, a popular alternative to JavaScript for web development.
# 
# Python features at number 3, despite already being one of the most widely-used languages in the world. Python has a solid foundation, is easy to learn & use, has a large ecosystem of domain-specific libraries, and a massive worldwide community.
# 
# 

# #### Q: In which countries do developers work the highest number of hours per week? Consider countries with more than 250 responses only.
# 
# To answer this question, we'll need to use the `groupby` data frame method to aggregate the rows for each country. We'll also need to filter the results to only include the countries with more than 250 respondents.

# In[314]:


countries_df = survey_df.groupby('Country')[['WorkWeekHrs']].mean().sort_values('WorkWeekHrs', ascending=False)


# In[315]:


countries_df


# The Asian countries like Iran, China, and Israel have the highest working hours, followed by the United States. However, there isn't too much variation overall, and the average working hours seem to be around 40 hours per week.
# 
# 

# #### Q: How important is it to start young to build a career in programming?
# 
# Let's create a scatter plot of `Age` vs. `YearsCodePro` (i.e., years of coding experience) to answer this question.

# In[316]:


schema.YearsCodePro


# In[317]:


sns.scatterplot(x='Age', y='YearsCodePro', hue='Hobbyist', data=survey_df)
plt.xlabel("Age")
plt.ylabel("Years of professional coding experience");


# You can see points all over the graph, which indicates that you can **start programming professionally at any age**. Many people who have been coding for several decades professionally also seem to enjoy it as a hobby.
# 
# We can also view the distribution of the `Age1stCode` column to see when the respondents tried programming for the first time.

# In[318]:


plt.title(schema.Age1stCode)
sns.histplot(x=survey_df.Age1stCode, bins=30, kde=True);


# ## Inferences and Conclusions
# 
# We've drawn many inferences from the survey. Here's a summary of a few of them:
# 
# - Based on the survey respondents' demographics, we can infer that the survey is somewhat representative of the overall programming community. However, it has fewer responses from programmers in non-English-speaking countries and women & non-binary genders.
# 
# - The programming community is not as diverse as it can be. Although things are improving, we should make more efforts to support & encourage underrepresented communities, whether in terms of age, country, race, gender, or otherwise.
# 
# 
# - Although most programmers hold a college degree, a reasonably large percentage did not have computer science as their college major. Hence, a computer science degree isn't compulsory for learning to code or building a career in programming.
# 
# - A significant percentage of programmers either work part-time or as freelancers, which can be a great way to break into the field, especially when you're just getting started.
# 
# - Javascript & HTML/CSS are the most used programming languages in 2020, closely followed by SQL & Python.
# 
# - Python is the language most people are interested in learning - since it is an easy-to-learn general-purpose programming language well suited for various domains.
# 
# - Rust and TypeScript are the most "loved" languages in 2020, both of which have small but fast-growing communities. Python is a close third, despite already being a widely used language.
# 
# - Programmers worldwide seem to be working for around 40 hours a week on average, with slight variations by country.
# 
# - You can learn and start programming professionally at any age. You're likely to have a long and fulfilling career if you also enjoy programming as a hobby.

# In[320]:


jovian.commit()


# In[ ]:




