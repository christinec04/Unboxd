from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
import sys

def is_valid_review(review) -> bool:
    """Checks if review is suitable for sentiment analysis"""
    if not isinstance(review, str):
        return False

    text = review.strip()
    MIN_CHAR_LENGTH = 3
    if len(text) < MIN_CHAR_LENGTH:
        return False

    # If the review has words or numbers, it is valid
    alphanum_count = sum(c.isalnum() for c in text)
    if alphanum_count > 0:
        return True
    
    # If the review has no alphanumeric content (ex. "!!!" or "..."),
    # we allow it only if it's short to prevent symbol-spamming
    MAX_SYMBOL_LENGTH = 15
    if len(text) <= MAX_SYMBOL_LENGTH:
        return True
    return False


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
    from paths import Path
    username = sys.argv[1]
    df = sentiment_analysis(pd.read_csv(os.path.join(Path.REVIEWS_FOLDER, f"{username}.csv")))
    df.to_csv(os.path.join(Path.SENTIMENT_REVIEWS_FOLDER, f"{username}.csv")) 

