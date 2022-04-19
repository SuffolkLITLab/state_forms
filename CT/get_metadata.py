# go through each group, add files and their urls into the table
import hashlib
import re
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader


df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])


def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def parse_group(group_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    table = soup.find('table', id="ContentPlaceHolder1_formGridView") #find table of forms
    rows = table.find_all("tr")
    for row in rows:
        form_link = row.find_all("a", href=True)
        if not form_link: #if thats a row without link to a form then we dont consider it
            continue
        if ".pdf" not in form_link[0]["href"]: #when its not a pdf file
            continue

        title = row.find_all("td")[1].get_text().strip()
        if "Polish" in title or "Portuguese" in title or "Spanish" in title:
            continue #we dont need them
        file_url = "https://www.jud.ct.gov/webforms/" + form_link[0]["href"]
        filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
        file_id = hashme(file_url)
        today = date.today().strftime("%Y-%m-%d")
        df.loc[len(df.index)] = [file_id, 'CT', 'www.jud.ct.gov', title,
                                          group_name, file_url, filename, today] #add file data to our table


with open('group_links.csv', 'r') as file:
    csv_reader = reader(file)
    next(csv_reader)
    for row in csv_reader:
        group_name = row[0]
        group_url = row[1]
        print("Parsing: " + group_url)
        parse_group(group_name, group_url)
        time.sleep(3)  # wait before new request

    df.to_csv("files.csv", index=False)

