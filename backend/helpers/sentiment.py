from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import sys

# sentence = """Okay this will be fun - imagine if an illegal alien was a real human being!?! Right? We should make that 🤗
# It’s a decent premise but needed to make the point a lot stronger. And the Mexican kid running away from the cartel to America is a little…
# But he was a great actor go off lil man!"""

def is_valid_review(review):
    if not isinstance(review, str):
        return False

    text = review.strip()
    if len(text) < 20:
        return False

    stopwords = {"and", "the", "this", "that", "is", "a", "i"} 
    words = [w for w in text.lower().split() if w not in stopwords]
    if len(words) < 3:
        return False
    return True


def sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    analyzer = SentimentIntensityAnalyzer()

    df['is_valid'] = df['user review'].apply(is_valid_review)
    df = df[df['is_valid']].reset_index(drop=True)

    reviews = df['user review']

    df['negative'] = [analyzer.polarity_scores(r)['neg'] for r in reviews]
    df['neutral'] = [analyzer.polarity_scores(r)['neu'] for r in reviews]
    df['positive'] = [analyzer.polarity_scores(r)['pos'] for r in reviews]
    df['compound'] = [analyzer.polarity_scores(r)['compound'] for r in reviews]

    # this drops neutral (-0.05 <= x <= 0.05) and negative (x < -0.05) reviews 
    # df = df[df['compound'] > 0.05].reset_index(drop=True)
    return df


if __name__ == '__main__':
    from utils import create_path
    username = sys.argv[1]
    path = create_path([os.getcwd(), '..', 'data', 'reviews', f'{username}.csv'])
    df = sentiment_analysis(pd.read_csv(path))
    output_path = create_path([os.getcwd(), '..', 'data', 'processed_reviews', f'{username}.csv'])
    df.to_csv(output_path, index=False)
else:
    from .utils import create_path

