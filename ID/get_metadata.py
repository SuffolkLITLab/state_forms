import hashlib
import re
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def get_file_url(form):
    links = form.find_all("a")
    for link in links:
        if "pdf" in link["href"]:
            file_url = link["href"]
    file_url = "https://courtselfhelp.idaho.gov" + file_url
    return file_url

def parse_group(group_soup):
    group_name = group_soup.find("h5").get_text().strip()
    forms = group_soup.find_all("li")
    for form in forms:
        title = form.contents[0]
        file_url = get_file_url(form)
        filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
        file_id = hashme(file_url)
        today = date.today().strftime("%Y-%m-%d")
        df.loc[len(df.index)] = [file_id, 'ID', 'courtselfhelp.idaho.gov', title,
                                 group_name, file_url, filename, today] #add file data to our table
    return



df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])
url = "https://courtselfhelp.idaho.gov/Forms"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

groups = soup.find_all('section')
for group in groups:
    group_name = group.find("h5").get_text().strip()
    print("Parsing: " + group_name)
    parse_group(group)
df.to_csv("files.csv", index=False)