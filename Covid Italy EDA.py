#!/usr/bin/env python
# coding: utf-8

# ## Analyzing tabular data with pandas(Italy covid data Analysis 2020)

# In[2]:


from urllib.request import urlretrieve


# In[3]:


italy_covid_url = 'https://gist.githubusercontent.com/aakashns/f6a004fa20c84fec53262f9a8bfee775/raw/f309558b1cf5103424cef58e2ecb8704dcd4d74c/italy-covid-daywise.csv'

urlretrieve(italy_covid_url, 'italy-covid-daywise.csv')


# In[86]:


import pandas as pd


# In[87]:


covid_df=pd.read_csv('italy-covid-daywise.csv')


# In[88]:


type(covid_df)


# In[89]:


covid_df


# Here's what we can tell by looking at the dataframe:
# 
# - The file provides four day-wise counts for COVID-19 in Italy
# - The metrics reported are new cases, deaths, and tests
# - Data is provided for 248 days: from Dec 12, 2019, to Sep 3, 2020
# 
# Keep in mind that these are officially reported numbers. The actual number of cases & deaths may be higher, as not all cases are diagnosed. 
# 
# We can view some basic information about the data frame using the `.info` method.

# In[9]:


covid_df.info()


# It appears that each column contains values of a specific data type. You can view statistical information for numerical columns (mean, standard deviation, minimum/maximum values, and the number of non-empty values) using the `.describe` method.

# In[10]:


covid_df.describe()


# The `columns` property contains the list of columns within the data frame.

# In[11]:


covid_df.columns


# In[12]:


covid_df.shape


# Here's a summary of the functions & methods:
# 
# * `pd.read_csv` - Read data from a CSV file into a Pandas `DataFrame` object
# * `.info()` - View basic infomation about rows, columns & data types
# * `.describe()` - View statistical information about numeric columns
# * `.columns` - Get the list of column names
# * `.shape` - Get the number of rows & columns as a tuple

# ## Retrieving data from data frame

# 1The first thing you might want to do is retrieve data from this data frame, e.g., the counts of a specific day or the list of values in a particular column. To do this, it might help to understand the internal representation of data in a data frame. Conceptually, you can think of a dataframe as a dictionary of lists: keys are column names, and values are lists/arrays containing data for the respective columns. 

# In[13]:


# Pandas format is simliar to this
covid_data_dict = {
    'date':       ['2020-08-30', '2020-08-31', '2020-09-01', '2020-09-02', '2020-09-03'],
    'new_cases':  [1444, 1365, 996, 975, 1326],
    'new_deaths': [1, 4, 6, 8, 6],
    'new_tests': [53541, 42583, 54395, None, None]
}


# In[14]:


covid_df


# In[15]:


type(covid_df['new_cases'])


# In[16]:


covid_df['new_cases'][246]


# In[17]:


covid_df.at[246,'new_cases']


# In[19]:


covid_df.new_cases


# In[20]:


cases_df=covid_df[['date', 'new_cases']]


# In[21]:


cases_df


# In[22]:


covid_df_copy=covid_df.copy()


# In[23]:


covid_df.loc[243]


# In[24]:


covid_df.head()


# In[25]:


covid_df.tail()


# In[26]:


covid_df.at[0,'new_tests']


# In[27]:


type(covid_df.at[0,'new_tests'])


# The distinction between `0` and `NaN` is subtle but important. In this dataset, it represents that daily test numbers were not reported on specific dates. Italy started reporting daily tests on Apr 19, 2020. 93,5310 tests had already been conducted before Apr 19. 
# 
# We can find the first index that doesn't contain a `NaN` value using a column's `first_valid_index` method.

# In[28]:


covid_df.new_tests.first_valid_index()


# Let's look at a few rows before and after this index to verify that the values change from `NaN` to actual numbers. We can do this by passing a range to `loc`.

# In[30]:


covid_df[103:113]


# In[31]:


covid_df.sample(10)


# ## Analyzing Data from data frames

# 
# Let's try to answer some questions about our data.
# 
# **Q: What are the total number of reported cases and deaths related to Covid-19 in Italy?**
# 
# Similar to Numpy arrays, a Pandas series supports the `sum` method to answer these questions.

# In[137]:


total_cases=covid_df.new_cases.sum()
total_deaths=covid_df.new_deaths.sum()


# In[138]:


print("Number of reported cases is {}  and Number of reported death is {}".format(int(total_cases),int(total_deaths)))


# **Q: What is the overall death rate (ratio of reported deaths to reported cases)?**

# In[139]:


death_rate=covid_df.new_deaths.sum()/covid_df.new_cases.sum()


# In[140]:


print("The overall death rate in Italy is {:.2f} %".format(death_rate*100))


# **Q: What is the overall number of tests conducted? A total of 935310 tests were conducted before daily test numbers were reported.**

# In[141]:


initial_tests=935310
total_tests=initial_tests+covid_df.new_tests.sum()


# In[142]:


total_tests


# **Q: What fraction of tests returned a positive result?**

# In[143]:


positive_rate=total_cases/total_tests


# In[144]:


print("{:.2f} % of tests in Italy let to positive diagnosis".format(positive_rate*100))


# ## Querying and sorting rows
# 
# Let's say we want only want to look at the days which had more than 1000 reported cases. We can use a boolean expression to check which rows satisfy this criterion.

# In[145]:


high_cases=covid_df.new_cases>1000


# In[146]:


high_cases


# In[147]:


covid_df[high_cases]


# In[148]:


from IPython.display import display
with pd.option_context('display.max_rows',100):
    display(covid_df[covid_df.new_cases>1000])


# In[149]:


positive_rate


# In[150]:


high_ratio_df=covid_df[covid_df.new_cases/covid_df.new_tests>positive_rate]


# In[151]:


high_ratio_df


# In[152]:


covid_df['positive_rate']=covid_df.new_cases/covid_df.new_tests


# In[ ]:





# In[156]:


covid_df


# In[ ]:





# In[ ]:





# In[158]:


covid_df


# ### Sorting rows using column values
# 
# The rows can also be sorted by a specific column using `.sort_values`. Let's sort to identify the days with the highest number of cases, then chain it with the `head` method to list just the first ten results.

# In[159]:


covid_df.sort_values('new_cases', ascending=False).head(10)


# In[160]:


covid_df.sort_values('new_deaths', ascending=False).head(10)


# It appears that daily deaths hit a peak just about a week after the peak in daily new cases.
# 
# Let's also look at the days with the least number of cases. We might expect to see the first few days of the year on this list.

# In[161]:


covid_df.sort_values('new_cases').head(10)


# It seems like the count of new cases on Jun 20, 2020, was `-148`, a negative number! Not something we might have expected, but that's the nature of real-world data. It could be a data entry error, or the government may have issued a correction to account for miscounting in the past. Can you dig through news articles online and figure out why the number was negative?
# 
# Let's look at some days before and after Jun 20, 2020.

# In[162]:


covid_df.loc[169:175]


# For now, let's assume this was indeed a data entry error. We can use one of the following approaches for dealing with the missing or faulty value:
# 1. Replace it with `0`.
# 2. Replace it with the average of the entire column
# 3. Replace it with the average of the values on the previous & next date
# 4. Discard the row entirely
# 
# Which approach you pick requires some context about the data and the problem. In this case, since we are dealing with data ordered by date, we can go ahead with the third approach.
# 
# You can use the `.at` method to modify a specific value within the dataframe.

# In[163]:


covid_df.at[172,'new_cases']= (covid_df.at[171,'new_cases']+covid_df.at[173,'new_cases'])/2


# In[164]:


covid_df.loc[169:175]


# Here's a summary of the functions & methods we looked at in this section:
# 
# - `covid_df.new_cases.sum()` - Computing the sum of values in a column or series
# - `covid_df[covid_df.new_cases > 1000]` - Querying a subset of rows satisfying the chosen criteria using boolean expressions
# - `df['pos_rate'] = df.new_cases/df.new_tests` - Adding new columns by combining data from existing columns
# - `covid_df.drop('positive_rate')` - Removing one or more columns from the data frame
# - `sort_values` - Sorting the rows of a data frame using column values
# - `covid_df.at[172, 'new_cases'] = ...` - Replacing a value within the data frame

# ## Working with dates
# 
# While we've looked at overall numbers for the cases, tests, positive rate, etc., it would also be useful to study these numbers on a month-by-month basis. The `date` column might come in handy here, as Pandas provides many utilities for working with dates.

# In[165]:


covid_df['date']


# In[166]:


covid_df['date']=pd.to_datetime(covid_df.date)


# In[167]:


covid_df.date


# In[168]:


covid_df['year']=pd.DatetimeIndex(covid_df.date).year


# In[169]:


covid_df


# In[170]:


covid_df['month']=pd.DatetimeIndex(covid_df.date).month


# In[171]:


covid_df['day']=pd.DatetimeIndex(covid_df.date).day


# In[172]:


covid_df['weekday']=pd.DatetimeIndex(covid_df.date).weekday


# In[173]:


covid_df


# Let's check the overall metrics for May. We can query the rows for May, choose a subset of columns, and use the `sum` method to aggregate each selected column's values.

# In[174]:


covid_df_may=covid_df[covid_df.month==5]


# In[175]:


covid_df_may


# In[176]:


covid_df_may_metrics=covid_df_may[['new_cases', 'new_deaths','new_tests']]


# In[177]:


covid_may_totals=covid_df_may_metrics.sum()


# In[178]:


covid_may_totals


# In[179]:


type(covid_may_totals)


# In[180]:


covid_df.new_cases.mean()  #Overall Average


# In[181]:


covid_df[covid_df.weekday==6].new_cases.mean()


# In[182]:


#it seems that more cases were reported on Sundays compared to other days .


# ## Grouping and aggregation
# 
# As a next step, we might want to summarize the day-wise data and create a new dataframe with month-wise data. We can use the `groupby` function to create a group for each month, select the columns we wish to aggregate, and aggregate them using the `sum` method. 

# In[183]:


covid_df.groupby('month')


# In[184]:


monthly_groups=covid_month_df=covid_df.groupby('month')[['new_cases','new_deaths','new_tests']]


# In[185]:


monthly_groups.sum()


# Apart from grouping, another form of aggregation is the running or cumulative sum of cases, tests, or death up to each row's date. We can use the `cumsum` method to compute the cumulative sum of a column as a new series. Let's add three new columns: `total_cases`, `total_deaths`, and `total_tests`.

# In[186]:


weekday_groups=covid_month_df=covid_df.groupby('weekday')[['new_cases','new_deaths','new_tests']].sum()


# In[187]:


weekday_groups


# In[188]:


covid_df['total_cases']=covid_df.new_cases.cumsum()


# In[189]:


covid_df


# ## Merging data from multiple sources
# 
# To determine other metrics like test per million, cases per million, etc., we require some more information about the country, viz. its population. Let's download another file `locations.csv` that contains health-related information for many countries, including Italy.

# In[190]:


urlretrieve('https://gist.githubusercontent.com/aakashns/8684589ef4f266116cdce023377fc9c8/raw/99ce3826b2a9d1e6d0bde7e9e559fc8b6e9ac88b/locations.csv', 
            'locations.csv')


# In[191]:


location_df=pd.read_csv('locations.csv')


# In[192]:


location_df


# In[193]:


location_df[location_df.location=="Italy"]


# In[194]:


covid_df['location']="Italy"


# In[195]:


covid_df


# In[211]:


merged_df=covid_df.merge(location_df, on="location")


# In[197]:


merged_df


# In[198]:


merged_df['cases_per_million']=merged_df.total_cases*1e6/merged_df.population


# In[205]:


covid_df['total_cases'] = covid_df.new_cases.cumsum()


# In[208]:


covid_df['total_deaths'] = covid_df.new_deaths.cumsum()


# In[209]:


covid_df['total_tests'] = covid_df.new_tests.cumsum() + initial_tests


# In[210]:


covid_df


# In[212]:


merged_df=covid_df.merge(location_df, on="location")


# In[213]:


merged_df


# In[214]:


merged_df['cases_per_million']=merged_df.total_cases*1e6/merged_df.population


# In[215]:


merged_df['deaths_per_million']=merged_df.total_deaths*1e6/merged_df.population


# In[216]:


merged_df['test_per_million']=merged_df.total_tests*1e6/merged_df.population


# In[217]:


merged_df


# In[219]:


result_df = merged_df[['date',
                       'new_cases', 
                       'total_cases', 
                       'new_deaths', 
                       'total_deaths', 
                       'new_tests', 
                       'total_tests', 
                       'cases_per_million', 
                       'deaths_per_million', 
                       'test_per_million']]


# In[220]:


result_df


# In[223]:


result_df.to_csv('result.csv',index=None) # not include index


# In[224]:


jovian.commit()


# In[226]:


jovian.commit(outputs=['result.csv'])


# In[ ]:




