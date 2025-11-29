from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import sys

def is_valid_review(review) -> bool:
    """Checks if review is suitable for sentiment analysis"""
    if not isinstance(review, str):
        return False

    text = review.strip()
    if len(text) < 3:
        return False

    stopwords = {"and", "the", "this", "that", "is", "a", "i"} 
    words = [w for w in text.lower().split() if w not in stopwords]
    if len(words) < 3:
        return False
    return True


def sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Performs sentiment analysis on user reviews"""
    analyzer = SentimentIntensityAnalyzer()

    df["is_valid"] = df["user_review"].apply(is_valid_review)
    df = df[df["is_valid"]].reset_index(drop=True)

    reviews = df["user_review"]

    # df["negative"] = [analyzer.polarity_scores(r)["neg"] for r in reviews]
    # df["neutral"] = [analyzer.polarity_scores(r)["neu"] for r in reviews]
    # df["positive"] = [analyzer.polarity_scores(r)["pos"] for r in reviews]
    df["compound"] = [analyzer.polarity_scores(r)["compound"] for r in reviews]

    # this drops neutral (-0.05 <= x <= 0.05) and negative (x < -0.05) reviews 
    # df = df[df["compound"] > 0.05].reset_index(drop=True)
    return df


if __name__ == "__main__":
    username = sys.argv[1]
    path = os.path.join(os.getcwd(), "..", "data", "reviews", f"{username}.csv")
    df = sentiment_analysis(pd.read_csv(path))
    output_path = os.path.join(os.getcwd(), "..", "data", "sentiment_reviews", f"{username}.csv")
    df.to_csv(output_path) 

