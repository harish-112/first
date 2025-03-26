import praw
import pandas as pd
import time
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Step 1: Reddit API Setup (Replace with your credentials)
reddit = praw.Reddit(
    client_id="0KdQkCiXiL1n64VG0Fr9Cw",
    client_secret="hNQjaqAWH9FAjgalNWB9TnOnK8hXWw",
    user_agent="test"
)

# Step 2: Fetch Reddit Comments Dynamically Based on User Input
def fetch_reddit_comments(keyword, post_limit=15, comment_limit=30):
    comments_list = []
    subreddit = reddit.subreddit("all")  # Search across all subreddits

    for submission in subreddit.search(keyword, limit=post_limit):
        submission.comments.replace_more(limit=0)  # Expand all comments
        for comment in submission.comments[:comment_limit]:
            comments_list.append(comment.body)

    return comments_list
# Step 3: Sentiment Analysis
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']  # Overall sentiment score

    if compound >= 0.5:
        return "Positive"
    elif compound <= -0.5:
        return "Negative"
    else:
        return "Neutral"


# Step 4: Process Comments for Sentiment
def process_comments(comments):
    data = {
        "Comment": comments,
        "Sentiment": [analyze_sentiment(comment) for comment in comments]
        }
    return pd.DataFrame(data)

# Step 5: Dynamic Pricing Algorithm Based on Sentiment Analysis
def dynamic_pricing(sentiment_data):
    sentiment_counts = sentiment_data["Sentiment"].value_counts()
    total = len(sentiment_data)

    positive_ratio = (sentiment_counts.get("Positive", 0) / total) * 100
    negative_ratio = (sentiment_counts.get("Negative", 0) / total) * 100

    if negative_ratio >= 20:  # Lowered from 50% → More discounts triggered
        return "Apply 15% Discount"  # Increased discount to make it more impactful
    elif positive_ratio >= 60:  # Lowered from 70% → More price hikes
        return "Increase Price by 8%"  # Increased hike for better impact
    else:
        return "Maintain Current Price"


# Step 6: Run the System Dynamically for User-Input Products
if __name__ == "__main__":
    while True:
        product = input("\nEnter product/service name (or type 'exit' to quit): ").strip()
        if product.lower() == "exit":
            print("Exiting program.")
            break

        print(f"\nFetching discussions for '{product}' on Reddit...")
        all_comments = fetch_reddit_comments(product, post_limit=5, comment_limit=10)

        if not all_comments:
            print(f"No relevant discussions found for '{product}'. Try another product.")
            continue

        sentiment_data = process_comments(all_comments)
        recommendation = dynamic_pricing(sentiment_data)

        # Output results
        print("\nSample Sentiment Analysis:")
        print(sentiment_data.head())
        print(f"\n🔹 Pricing Recommendation for '{product}': {recommendation}")
