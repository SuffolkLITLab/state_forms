#create a csv file with group links

import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['group', 'link'])
url = 'https://www.jud.ct.gov/webforms/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

links = soup.find('span', id="ContentPlaceHolder1_catgLinks").find_all("a")
for link in links:
    group_name = link.get_text().replace("|","").strip()
    group_url = url + link["href"]
    if group_name!="Spanish" and group_name!="Polish" and group_name!="Portuguese":
        df.loc[len(df.index)] = [group_name, group_url]  # df with links to each group
df.to_csv("group_links.csv", index=False)