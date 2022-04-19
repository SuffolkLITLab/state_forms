#create a csv file with group links

import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['group', 'court', 'link'])
url = 'https://www.illinoiscourts.gov/documents-and-forms/approved-forms/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

courts = soup.find_all('section', class_='tab-content cloneable')
for court in courts:
    # get the name of the court
    court_name = court.find('h2', class_='tab-title').get_text().strip().split()[0]

    # get the links associated with this court
    groups = court.find_all('li')
    for group in groups:
        tag = group.find('a')
        group_name = tag.get_text().strip()
        link = "https://www.illinoiscourts.gov" + tag["href"]
        df.loc[len(df.index)] = [group_name, court_name, link] #df with links to each group

df.to_csv("group_links.csv")
