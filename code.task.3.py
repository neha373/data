# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 22:23:53 2025

@author: muskan
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# Load the dataset (Replace 'your_file.csv' with actual filename)
df = pd.read_csv(r"C:\Users\muskan\Downloads\violin_plot_data.csv")

# Ensure required columns exist
required_columns = {'category', 'app_name', 'rating', 'review_count'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

# Filter categories with more than 50 apps
category_counts = df['category'].value_counts()
valid_categories = category_counts[category_counts > 50].index
df_filtered = df[df['category'].isin(valid_categories)]

# Filter apps containing letter 'C'
df_filtered = df_filtered[df_filtered['app_name'].str.contains('C', case=False, na=False)]

# Exclude apps with fewer than 10 reviews and ratings >= 4.0
df_filtered = df_filtered[(df_filtered['review_count'] >= 10) & (df_filtered['rating'] < 4.0)]

# Check if the current time is between 4 PM and 6 PM IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()
allowed_start = datetime.strptime("16:00", "%H:%M").time()
allowed_end = datetime.strptime("18:00", "%H:%M").time()

if allowed_start <= current_time <= allowed_end:
    # Plot violin plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='category', y='rating', data=df_filtered, inner='quartile', palette='muted')
    plt.xticks(rotation=45)
    plt.title('Distribution of Ratings for App Categories')
    plt.ylabel('Ratings')
    plt.xlabel('App Category')
    plt.show()
else:
    print("Graph is not displayed outside the allowed time window (4 PM - 6 PM IST).")
