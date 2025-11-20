from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import csv
import os
import re

analyzer = SentimentIntensityAnalyzer()

#analyzer

# sentence = """Okay this will be fun - imagine if an illegal alien was a real human being!?! Right? We should make that 🤗

# It’s a decent premise but needed to make the point a lot stronger. And the Mexican kid running away from the cartel to America is a little…
# But he was a great actor go off lil man!"""

# vs = analyzer.polarity_scores(sentence)

# print(vs)

# reading excel file and then outputting values for the reviews. 

def is_valid_review(review):
    if not isinstance(review, str):
        return False

    text = review.strip()

    if len(text) < 20:
        return False

    stopwords = {"and", "the", "this", "that", "is", "a", "i"}  # example
    words = [w for w in text.lower().split() if w not in stopwords]

    if len(words) < 3:
        return False

    return True

path = r"C:\Users\zhang\School\B365\Project-ez2-ermili-cch8-dvchavan\reviews\schaffrillas.csv"
output_path = r"C:\Users\zhang\School\B365\Project-ez2-ermili-cch8-dvchavan\processed_reviews\schaffrillas_sentiment.csv"

df = pd.read_csv(path)

df['is_valid'] = df['user review'].apply(is_valid_review)

df = df[df['is_valid']].reset_index(drop=True)

reviews = df['user review'].astype(str)

df['negative'] = [analyzer.polarity_scores(r)['neg'] for r in reviews]
df['neutral'] = [analyzer.polarity_scores(r)['neu'] for r in reviews]
df['positive'] = [analyzer.polarity_scores(r)['pos'] for r in reviews]
df['compound'] = [analyzer.polarity_scores(r)['compound'] for r in reviews]

df = df[df['compound'] > 0.05].reset_index(drop=True)

df.to_csv(output_path, index=False)

