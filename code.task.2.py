# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 21:40:44 2025

@author: kunal
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# Load the dataset (Replace 'your_file.csv' with actual filename)
df = pd.read_csv(r"C:\Users\kunal\Downloads\User_Reviews.csv")

# Ensure required columns exist
required_columns = {'category', 'rating', 'size', 'installs', 'review_count', 'last_update'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

# Convert 'size' to numeric (assuming size is in MB or GB, convert GB to MB for comparison)
def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'G' in size:
        return float(size.replace('G', '')) * 1000
    return 0  # Default if size is not mentioned

df['size'] = df['size'].astype(str).apply(convert_size)

# Convert 'last_update' to datetime format
df['last_update'] = pd.to_datetime(df['last_update'], errors='coerce')

# Filter data based on conditions
df_filtered = df[(df['rating'] >= 4.0) & (df['size'] >= 10) & (df['last_update'].dt.month == 1)]

# Get top 10 categories by number of installs
top_categories = df_filtered.groupby('category')['installs'].sum().nlargest(10).index
df_filtered = df_filtered[df_filtered['category'].isin(top_categories)]

# Aggregate data to get average rating and total review count per category
category_stats = df_filtered.groupby('category').agg({
    'rating': 'mean',
    'review_count': 'sum'
}).reset_index()

# Plot grouped bar chart
fig, ax1 = plt.subplots(figsize=(12, 6))

sns.barplot(x='category', y='rating', data=category_stats, color='blue', label='Avg Rating', ax=ax1)
ax1.set_ylabel('Average Rating', color='blue')
ax1.set_ylim(3.5, 5)
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
sns.barplot(x='category', y='review_count', data=category_stats, color='green', label='Total Reviews', ax=ax2)
ax2.set_ylabel('Total Review Count', color='green')
ax2.tick_params(axis='y', labelcolor='green')

plt.title('Comparison of Average Rating and Total Reviews for Top 10 Categories')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()
