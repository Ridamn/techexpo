import re
import pandas as pd
from datetime import datetime

def rawToDf(fp):
    pat = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}[\u202f\s]?[AP]M)\s-\s'
    )

    rows = []
    cur_dt = None
    cur_usr = None
    cur_msg = []

    with open(fp, 'r', encoding='utf-8') as f:
        for ln in f:
            ln = ln.rstrip('\n')
            m = pat.match(ln)

            if m:
                if cur_dt and cur_usr:
                    rows.append([cur_dt, cur_usr, ' '.join(cur_msg).strip()])

                dt_str = m.group(1)
                rest = ln[m.end():]

                try:
                    dt = datetime.strptime(
                        dt_str.replace('\u202f', ' '),
                        '%m/%d/%y, %I:%M %p'
                    )
                except:
                    cur_dt = None
                    cur_usr = None
                    cur_msg = []
                    continue

                if ':' in rest:
                    usr, msg = rest.split(':', 1)
                    cur_dt = dt
                    cur_usr = usr.strip()
                    cur_msg = [msg.strip()]
                else:
                    cur_dt = None
                    cur_usr = None
                    cur_msg = []

            else:
                if cur_msg is not None:
                    cur_msg.append(ln.strip())

    if cur_dt and cur_usr:
        rows.append([cur_dt, cur_usr, ' '.join(cur_msg).strip()])

    df = pd.DataFrame(rows, columns=['dt', 'usr', 'msg'])

    df = df[~df['msg'].str.contains('message was deleted', case=False, na=False)]
    df.reset_index(drop=True, inplace=True)

    return df


if __name__ == "__main__":
    df = rawToDf("data/chat.txt")
    print(df.head())
    print("messages:", len(df))
    print("users:", df['usr'].nunique())
