import nltk
nltk.download("vader_lexicon")
import streamlit as st
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from src.parser import rawToDf
from src.clean_text import clean_msg

st.set_page_config(page_title="ChatScope", layout="wide")

st.title("ChatScope – WhatsApp Chat Analyzer")

up = st.file_uploader("Upload WhatsApp Chat (.txt)", type="txt")

if up:
    with open("temp.txt", "wb") as f:
        f.write(up.getbuffer())

    df = rawToDf("temp.txt")

    df["clean"] = df["msg"].apply(clean_msg)
    df = df[df["clean"] != ""]

    sia = SentimentIntensityAnalyzer()
    df["score"] = df["clean"].apply(lambda x: sia.polarity_scores(x)["compound"])

    def lab(x):
        if x >= 0.05:
            return "positive"
        if x <= -0.05:
            return "negative"
        return "neutral"

    df["sent"] = df["score"].apply(lab)

    st.subheader("Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Messages", len(df))
    c2.metric("Total Users", df["usr"].nunique())
    c3.metric("Avg Sentiment", round(df["score"].mean(), 3))

    st.subheader("Sentiment Distribution")
    st.bar_chart(df["sent"].value_counts())

    st.subheader("Messages per Day")
    d = df["dt"].dt.date.value_counts().sort_index()
    st.line_chart(d)

    st.subheader("Top Active Users")
    u = df["usr"].value_counts().head(10)
    st.bar_chart(u)

    st.subheader("Sample Messages")
    st.dataframe(df[["dt", "usr", "sent", "msg"]].head(50))
