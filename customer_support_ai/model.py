import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob

# Load dataset
df = pd.read_csv("twcs.csv")
df = df[df["inbound"] == True]
df = df.sample(8000)

# Sentiment using TextBlob
def get_sentiment(text):
    score = TextBlob(str(text)).sentiment.polarity
    if score < -0.05:
        return "negative"
    elif score > 0.05:
        return "positive"
    else:
        return "neutral"

df["sentiment"] = df["text"].apply(get_sentiment)

# Issue classification
def detect_issue(text):
    text = text.lower()
    if "bill" in text or "refund" in text:
        return "billing"
    elif "internet" in text or "network" in text or "wifi" in text:
        return "network"
    elif "payment" in text or "card" in text:
        return "payment"
    else:
        return "general"

df["issue"] = df["text"].apply(detect_issue)

# Vectorization
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=10000)
X = vectorizer.fit_transform(df["text"])

# Train models
sentiment_model = LogisticRegression(max_iter=300)
sentiment_model.fit(X, df["sentiment"])

issue_model = LogisticRegression(max_iter=300)
issue_model.fit(X, df["issue"])

# Save models
pickle.dump(sentiment_model, open("models/sentiment.pkl","wb"))
pickle.dump(issue_model, open("models/issue.pkl","wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl","wb"))

print("High accuracy TextBlob-based AI trained")
