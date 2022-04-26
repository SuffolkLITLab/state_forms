#create a csv file with group links

import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['group', 'link'])
url = 'https://courts.delaware.gov/forms/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')

menu = soup.find('div', id="accordion2")
for m in menu:
    if str(m).strip():
        # print(m)
        links = m.find("table").find_all("a", href=True)
        for link in links:
            # print(link) #links to all forms
            group_name = link.get_text().strip()
            group_url = "https://courts.delaware.gov" + link["href"]
            print(group_url)
            if group_name!="All Forms": #thats not a group
                df.loc[len(df.index)] = [group_name, group_url]  # df with links to each group

df.to_csv("group_links.csv")

