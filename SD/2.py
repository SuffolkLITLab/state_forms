# go through each group, add files and their urls into the table
import hashlib
import re
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader
from cm import *


df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])


def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def parse_group(group_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    main_content = soup.find("div", id="middlecolumn")
    if main_content == None: #different tag for main content
        main_content = soup.find("div", class_="card border-0")
    anchors = main_content.find_all("a", href=True)
    for a in anchors:
        file_url = a["href"]

        if ".pdf" in file_url:
            title = a.get_text()
            create_metadata(title, file_url, group_name, "SD", "https://ujslawhelp.sd.gov")

with open('group_links.csv', 'r') as file:
    csv_reader = reader(file)
    next(csv_reader)
    for row in csv_reader:
        group_name = row[1]
        group_url = row[2]

        print("Parsing: " + group_url)
        parse_group(group_name, group_url)
        # break
        time.sleep(3)  # wait before new request
