import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from src.parser import rawToDf
from src.clean_text import clean_msg
from clean_text import clean_msg

df = rawToDf("data/chat.txt")
df["txt"] = df["msg"].apply(clean_msg)
df = df[df["txt"] != ""]

sia = SentimentIntensityAnalyzer()
df["score"] = df["txt"].apply(lambda x: sia.polarity_scores(x)["compound"])

def lab(x):
    if x >= 0.05:
        return "positive"
    if x <= -0.05:
        return "negative"
    return "neutral"

df["sent"] = df["score"].apply(lab)

# ---- 1. Overall sentiment distribution ----
plt.figure()
df["sent"].value_counts().plot(kind="bar")
plt.title("Overall Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Messages")
plt.tight_layout()
plt.show()

# ---- 2. Sentiment trend over time ----
df["date"] = df["dt"].dt.date
trend = df.groupby("date")["score"].mean()

plt.figure()
trend.plot()
plt.title("Average Sentiment Over Time")
plt.xlabel("Date")
plt.ylabel("Sentiment Score")
plt.tight_layout()
plt.show()

# ---- 3. Top users by sentiment ----
u = df.groupby("usr")["score"].mean()

plt.figure()
u.sort_values(ascending=False).head(10).plot(kind="bar")
plt.title("Top Positive Users")
plt.xlabel("User")
plt.ylabel("Avg Sentiment")
plt.tight_layout()
plt.show()

plt.figure()
u.sort_values().head(10).plot(kind="bar")
plt.title("Top Negative Users")
plt.xlabel("User")
plt.ylabel("Avg Sentiment")
plt.tight_layout()
plt.show()
