import hashlib
import re
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup
import pandas as pd
df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def parse_group(soup):
    group_name = soup.find("h3").get_text()
    list = soup.find_all("li")
    for l in list:
        title = re.search("[A-Z]{1,5}-[0-9]{1,5}(.*)\n", str(l))
        if title: #this is a form (others may be other pdfs, so we consider only those)
            title = title.group(1)
            title = re.sub("<.*>", "", title)
            # print(l)
            pdf_links = l.find_all("a", href=True)
            for pdf_link in pdf_links:
                file_url = pdf_link["href"]
                if ".pdf" in file_url:
                    print(pdf_link)
                    actual_title = pdf_link.get_text() + " | " + title
                    filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
                    file_id = hashme(file_url)
                    today = date.today().strftime("%Y-%m-%d")
                    df.loc[len(df.index)] = [file_id, 'AK', 'courts.alaska.gov', actual_title,
                                     group_name, file_url, filename, today]  # add file data to our table



url = 'https://courts.alaska.gov/forms/index.htm#dv'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')
groups = soup.find_all("div", class_="home-top")[1] #get main content
str_g = str(groups) #make it a string
groups_separated = str_g.split("<!-- ******") #split by group
groups_separated = groups_separated[1:-3] #get rid of unnecessary stuff
for g_s in groups_separated:
    parse_group(BeautifulSoup(g_s, 'html5lib')) #pass into parser as a bs object
    
df.to_csv("files.csv", index=False)