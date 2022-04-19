# go through each group, add files and their urls into the table
import hashlib
import re
import time
from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
from csv import reader

df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title', 'court',
                           'group', 'url', 'filename', 'downloaded_on'])


def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def parse_group(group_name, court, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    tables = soup.find_all('table') #find table of forms
    if not tables: #if table of files doesnt exist - so files too
        return #theres nothing in this group
    for table in tables:
        files = table.find_all('a', href=True)  # find the links to the files for this group
        for file in files:
            title = file.get_text().strip()
            file_url = file["href"]
            if "http" not in file_url: #some tags dont store a direct link
                file_url = "https://www.illinoiscourts.gov" + file_url
            if ".pdf" in file_url:
                filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
                file_id = hashme(file_url)
                today = date.today().strftime("%Y-%m-%d")
                df.loc[len(df.index)] = [file_id, 'IL', 'www.illinoiscourts.gov', title, court,
                               group_name, file_url, filename, today] #add file data to our table


def main():
    with open('group_links.csv', 'r') as file:
        csv_reader = reader(file)
        next(csv_reader)
        for row in csv_reader:
            name = row[1]
            if name == "Spanish":
                continue #its a collection of forms in spanish. we dont need other languages, right?
            court = row[2]
            url = row[3]
            print("Parsing: " + url)
            parse_group(name, court, url)
            time.sleep(3) #wait before new request
    df.to_csv("files.csv", index=False)

main()