import re
import pandas as pd
from src.parser import rawToDf



def clean_msg(s):
    if not isinstance(s, str):
        return ""

    s = s.lower()

    s = re.sub(r'<media omitted>', '', s, flags=re.I)
    s = re.sub(r'<this message was edited>', '', s, flags=re.I)

    s = re.sub(r'http\S+|www\S+', '', s)

    s = re.sub(r'@\S+', '', s)

    s = re.sub(r'[^a-z\s]', ' ', s)

    s = re.sub(r'\s+', ' ', s).strip()

    return s


if __name__ == "__main__":
    df = rawToDf("data/chat.txt")

    df['clean_msg'] = df['msg'].apply(clean_msg)

    df = df[df['clean_msg'] != ""]

    print(df[['msg', 'clean_msg']].head(10))
    print("messages after cleaning:", len(df))
