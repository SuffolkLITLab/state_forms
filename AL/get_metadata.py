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
    table = soup.find('table') #find table of forms
    if table: #if we dont have one more menu of choice
        form_links = table.find_all("a")
        for form_link in form_links:
            title = form_link.get_text().strip()
            file_url = "https://eforms.alacourt.gov" + form_link["href"]
            filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
            file_id = hashme(file_url)
            today = date.today().strftime("%Y-%m-%d")
            df.loc[len(df.index)] = [file_id, 'AL', 'https://eforms.alacourt.gov', title,
                                     group_name, file_url, filename, today] #add file data to our table
    else: #we have one more menu of choice
        links = soup.find("nav", class_="templatemo-top-nav col-lg-12 col-md-12").find_all("a")
        for link in links: #go thru each url
            new_url = "https://eforms.alacourt.gov" + link["href"]
            parse_group(group_name, new_url) #now parse this subgroup


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



# parse_group("civil forms", "https://eforms.alacourt.gov/civil-forms/")