#create a csv file with group links

import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['group', 'link'])
url = 'https://eforms.alacourt.gov'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

links = soup.find('nav').find_all("a")
for link in links:
    group_name = link.get_text().strip()
    group_url = "https://eforms.alacourt.gov" + link["href"]
    df.loc[len(df.index)] = [group_name, group_url]  # df with links to each group

df.to_csv("group_links.csv")

