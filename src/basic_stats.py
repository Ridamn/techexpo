import pandas as pd
import matplotlib.pyplot as plt
from parser import rawToDf

df = rawToDf("data/chat.txt")

# ---- 1. Messages per user ----
u = df['usr'].value_counts().head(10)

plt.figure()
u.plot(kind='bar')
plt.title("Top 10 Active Users")
plt.xlabel("User")
plt.ylabel("Messages")
plt.tight_layout()
plt.show()

# ---- 2. Messages per day ----
df['date'] = df['dt'].dt.date
d = df['date'].value_counts().sort_index()

plt.figure()
d.plot()
plt.title("Messages Per Day")
plt.xlabel("Date")
plt.ylabel("Messages")
plt.tight_layout()
plt.show()

# ---- 3. Messages per hour ----
df['hour'] = df['dt'].dt.hour
h = df['hour'].value_counts().sort_index()

plt.figure()
h.plot(kind='bar')
plt.title("Hourly Activity")
plt.xlabel("Hour of Day")
plt.ylabel("Messages")
plt.tight_layout()
plt.show()
