#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:36:55 2024

@author: yoojinoh
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

directory = '/Users/yoojinoh/Desktop/SPHSC525 final draft'
#reading in csv files
df1 = pd.read_csv('/Users/yoojinoh/Desktop/SPHSC525 final draft/reaction_times_P1.csv')
df2 = pd.read_csv('/Users/yoojinoh/Desktop/SPHSC525 final draft/reaction_times_P2.csv')
df = pd.concat([df1, df2], ignore_index=True)

#filter data to exclude outliers
clean_df = df[~((df['Reaction Time (ms)'] >= 2500) | (df['Reaction Time (ms)'] <= 200))]
print(clean_df)

#descriptive stats for switch vs. no-switch
switch_stats = clean_df.groupby('Switch')['Reaction Time (ms)'].describe()
print(switch_stats)

#descriptive stats for wordlist vs. sentences
complex_stats = clean_df.groupby('Complex')['Reaction Time (ms)'].describe()
print(complex_stats)

#descriptive stats for switch vs. no-switch by Complex condition

combined_stats = clean_df.groupby(['Complex', 'Switch'])['Reaction Time (ms)'].describe()
print(combined_stats)

#creating box plots to show differences in RT for the conditions

#Switch box plot
plt.figure(figsize=(10, 6))
plt.boxplot([clean_df[clean_df['Switch'] == 'S']['Reaction Time (ms)'],
             clean_df[clean_df['Switch'] == 'N']['Reaction Time (ms)']],
            labels=['Switch', 'No-switch'])
plt.title('RT distribution for Switch vs. No-switch')
plt.xlabel('Switch')
plt.ylabel('RT (ms)')
plt.show()

#Complex box plot
plt.figure(figsize=(10, 6))
plt.boxplot([clean_df[clean_df['Complex'] == 'WL']['Reaction Time (ms)'],
             clean_df[clean_df['Complex'] == 'ST']['Reaction Time (ms)']],
            labels=['Wordlist', 'Sentences'])
plt.title('Reaction Time Distribution for Wordlist vs. Sentences')
plt.xlabel('Complexity')
plt.ylabel('RT (ms)')
plt.show()

#grouped box plots

# Extract data for Complexity conditions
plt.figure(figsize=(10, 6))
data = clean_df
plt.title('Reaction Time Distribution for Wordlist vs. Sentences')
plt.xlabel('Complexity')
plt.ylabel('RT (ms)')
sns.boxplot(x=data['Complex'], y=data['Reaction Time (ms)'], hue=data['Switch'])
plt.show()







