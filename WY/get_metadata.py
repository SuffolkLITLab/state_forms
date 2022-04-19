#create a csv file with group links
import hashlib
import re
import sys
import time
from datetime import date

import requests
from bs4 import BeautifulSoup
import pandas as pd
df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def li_forms(soup, group_name):
    li_tags = soup.find_all("li")
    for li_tag in li_tags:
        links = li_tag.find_all("a", href=True)
        for link in links:
            file_url = link["href"]
            if ".pdf" in file_url: #thats what we need
                title = link.get_text()
                filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
                file_id = hashme(file_url)
                today = date.today().strftime("%Y-%m-%d")
                df.loc[len(df.index)] = [file_id, 'WY', 'courts.state.wy.us', title,
                                         group_name, file_url, filename, today]  # add file data to our table

def table_forms(soup, group_name):
    tables = soup.find_all("div", class_="panel panel-default")
    for table in tables:
        table_rows = table.find_all("tr")
        for table_row in table_rows:
            table_data = table_row.find_all("td")
            if table_data:
                file_url = table_data[1].find("a")["href"]
                if ".pdf" in file_url:
                    title = table_data[0].get_text()
                    filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
                    file_id = hashme(file_url)
                    today = date.today().strftime("%Y-%m-%d")
                    df.loc[len(df.index)] = [file_id, 'WY', 'courts.state.wy.us', title,
                                             group_name, file_url, filename, today]  # add file data to our table


def parse_group(soup):
    group_name = soup.find("h3")
    if group_name:
        group_name = group_name.get_text()
    else:
        group_name = "Other Forms"
#     search for forms that are not in the table (they're all in lists)
    li_forms(soup, group_name)
#     now search for forms that are in the table
    table_forms(soup, group_name)


url = "https://www.courts.state.wy.us/legal-assistances-and-forms/court-self-help-forms/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html5lib')
groups = soup.find_all("div", {'class':['tab-pane fade in well', 'tab-pane fade in']})
for group in groups:
    parse_group(group)

df.to_csv("files.csv", index=False)
