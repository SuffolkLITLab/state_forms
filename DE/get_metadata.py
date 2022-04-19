# go through each group, add files and their urls into the table
import hashlib
import re
import sys
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader


df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on', 'type'])


def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def parse_group(group_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    table = soup.find('table', class_="table table-responsive table-bordered table-condensed table-striped") #find table of forms
    rows = table.find_all("tr")
    for row in rows:
        tds = row.find_all("td") #file is in the second table cell
        form_link = tds[1].find("a", href=True)
        if "Fill-In Form" in tds[4].get_text(): #thats .doc
            filetype = ".doc"
        else:
            filetype = ".pdf"
        if form_link:
            title = form_link.get_text().strip()
            file_url = "https://courts.delaware.gov" + form_link["href"]
            print(file_url)
            filename = re.search('.*\/(.*[0-9])', file_url).group(1)
            file_id = hashme(file_url)
            today = date.today().strftime("%Y-%m-%d")
            df.loc[len(df.index)] = [file_id, 'DE', 'https://courts.delaware.gov', title,
                                     group_name, file_url, filename, today, filetype] #add file data to our table


with open('group_links.csv', 'r') as file:
    csv_reader = reader(file)
    next(csv_reader)
    for row in csv_reader:
        group_name = row[1]
        group_url = row[2]

        print("Parsing: " + group_url)
        parse_group(group_name, group_url)
        time.sleep(3)  # wait before new request
    df.to_csv("files.csv", index=False)