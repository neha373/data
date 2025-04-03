# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 19:50:21 2025

@author: kunal
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset (replace 'your_file.csv' with the actual filename)
df = pd.read_csv(r"C:\Users\kunal\Downloads\googleplaystore_user_reviews.csv")

# Ensure required columns exist
required_columns = {'app', 'translated_review', 'sentiment', 'sentiment_polarity', 'sentiment_subjectivity'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns in the dataset: {required_columns - set(df.columns)}")

# Filter apps with more than 1,000 reviews
df_filtered = df[df['app_count'] > 1000]

# Group ratings into defined ranges
def rating_group(rating):
    if rating <= 2:
        return '1-2 stars'
    elif rating <= 4:
        return '3-4 stars'
    else:
        return '4-5 stars'

df_filtered['rating_group'] = df_filtered['rating'].apply(rating_group)

# Get top 5 categories by the number of apps
top_categories = df_filtered['category'].value_counts().nlargest(5).index
df_filtered = df_filtered[df_filtered['category'].isin(top_categories)]

# Pivot the data to get sentiment counts per rating group
sentiment_distribution = df_filtered.groupby(['rating_group', 'review_sentiment']).size().unstack().fillna(0)

# Plot the stacked bar chart
sentiment_distribution.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6))
plt.title('Sentiment Distribution of User Reviews by Rating Groups')
plt.xlabel('Rating Group')
plt.ylabel('Number of Reviews')
plt.legend(title='Sentiment')
plt.xticks(rotation=0)
plt.show()
