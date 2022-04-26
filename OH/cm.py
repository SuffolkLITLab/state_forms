# go through each group, add files and their urls into the table
import hashlib
import os
import re
import time
from datetime import date
import pandas as pd

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def create_metadata(title, file_url, group_name, state, state_link):
    if os.path.exists("files.csv"):
        df = pd.read_csv("files.csv")
    else:
        df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                                   'group', 'url', 'filename', 'downloaded_on'])
    filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
    file_id = hashme(file_url)
    today = date.today().strftime("%Y-%m-%d")
    df.loc[len(df.index)] = [file_id, state, state_link, title,
                             group_name, file_url, filename, today]  # add file data to our table
    df.to_csv("files.csv", index=False)

