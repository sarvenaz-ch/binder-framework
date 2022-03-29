# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:47:39 2022

@author: local_ergo
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

''' LOADING DATA'''
data = pd.read_csv('Value_of_Energy_Cost_Savings_Program_Savings_for_Businesses_-_FY2020.csv')


#%%
print('_______________  Q4-1   ________________\n')
print(sum(data['Company Name'].duplicated()),' companies have the same name? , if so...')
print('- Number of companies:', len(set(data['Company Name'])))

print('_______________  Q4-2   ________________\n')
queens = data.groupby(by = ['City']).get_group('Queens')
print('- Number of jobs created by companies in Queens:', int(queens['Job created'].sum()))
del queens

print('_______________  Q4-3   ________________\n')
domain = []
for email in data['company email'].dropna():    
    if len(email.split('@')) == 1: # Removing invalid email addresses
        continue
    domain.append(email.split('@')[1].lower())
print('- Number of unique email domains:', len(set(domain)))
# del domain, email

print('_______________  Q4-4   ________________\n')
# Extract each companies separte NTAs
data['NTA_split'] = data['NTA'].str.split('-') 
data = data.explode('NTA_split')

NTA_count = data.groupby(by = ['NTA_split'])['Company Name'].count()
NTA_count.drop(NTA_count[NTA_count< 5].index, inplace = True) # Drop the NTAs with fewer businesses than 5

# Create a dataset where each NTA has at least 5 entries
df = data.drop(data[~data['NTA_split'].isin( list(NTA_count.index))].index)
avg_saving = df.groupby(by = ['NTA_split'])['Total Savings'].mean()
total_jobs_created = df.groupby(by = ['NTA_split'])['Job created'].sum()

# adding group level statistics to the dataframe
df['avg savings'] = df.groupby(by = 'NTA_split')['Total Savings'].transform('mean')
df['total job created'] = df.groupby(by = 'NTA_split')['Job created'].transform('sum')
print('- Average savings and total job created based on NTA are calculated.')
del avg_saving, total_jobs_created, NTA_count
 
print('_______________  Q4-5   ________________\n')
print('- The statistics is calculated and added to the dataframe.')
df.to_csv('milestone_day4.csv')
print('- Data saved in the csv file.')

#%%
print('_______________  Q5-2-1   ________________\n')
fig, ax = plt.subplots(3, figsize = (9,16))
x = df['Job created']
y = df['avg savings']

ax[0].scatter(x, y, s=60, alpha=0.7, edgecolors="k")
plt.title('Standard Scale');plt.xlabel('Job created'); plt.ylabel('avg savings'); 

ax[1].set_xscale("log");
ax[1].scatter(x, y, s=60, alpha=0.7, edgecolors="k")
plt.title('X-axis Logarithmic Scale'); plt.xlabel('Job created'); plt.ylabel('avg savings'); 

ax[2].set_yscale("log");
ax[2].scatter(x, y, s=60, alpha=0.7, edgecolors="k")
plt.title('y-axis Logarithmic Scale'); plt.xlabel('Job created'); plt.ylabel('avg savings'); 
plt.show()

print('_______________  Q5-2-2  ________________\n')
plt.subplot(211)
plt.hist(df['avg savings'], bins = 150)
plt.subplot(212)
plt.title('Standard Scale')

plt.hist(df['avg savings'], bins = 200)
plt.xscale('log')
plt.show()

# print('_______________  Q5-2-3  ________________\n')
# plt.plot(y = df['Job created'] )
# check to see if the date type is date object 
print(df[df['Effective Date'] == np.datetime64('NaT')].index)
df['Effective Date'] = pd.to_datetime(df['Effective Date'])
df['Effictive month'] = df['Effective Date'].dt.month
y = df.groupby(by = 'Effictive month')['total job created'].sum()
plt.plot(y.index, y)
plt.xlabel('month'); plt.ylabel('total job created')
plt.show()

