import hashlib
import re
from datetime import date
import pandas as pd
import requests
from bs4 import BeautifulSoup

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()



def get_soup():
    url = 'https://www.courts.wa.gov/forms/?fa=forms.static&staticID=14'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html5lib')
    return soup





df = pd.DataFrame(columns=["id","jurisdiction","group", "source","title","url","filename","downloaded_on", "filetype"])
soup = get_soup()

tables = soup.find('table')
str_t = str(tables)
names_n_groups = re.split('<h3>\s*<a name=\"[^\"]+\">\s*([^<>]+)\s*<\/a>\s*<\/h3>', str_t) #split by group,capture group names
del names_n_groups[0]
for i in range(len(names_n_groups)):
    if i%2==0: #even numbers are the names of the groups
        group_name = names_n_groups[i]
    else: #content of the group, now search for files in the group
        content = BeautifulSoup(names_n_groups[i], 'html5lib')
        elements = content.find_all('tr', class_="secondary3bg")
        for element in elements:
            title = element.find("b")
            if title:
                title = title.text.strip()
                links = element.find_all("a", href=True)
                for link in links:
                    url = link["href"]
                    # print(url)
                    if ".docx" in url:
                        filetype = "docx"
                        file_url = "https://www.courts.wa.gov/forms/" + url
                        filename = re.search('.*\/(.*\.docx)', file_url).group(1)
                        file_id = hashme(file_url)
                        today = date.today().strftime("%Y-%m-%d")
                        df.loc[len(df.index)] = [file_id, 'WA', group_name, 'www.courts.wa.gov', title,
                                                 file_url, filename, today, filetype]  # add file data to our table
                    if ".pdf" in url:
                        filetype = "pdf"
                        file_url = "https://www.courts.wa.gov/forms/" + url
                        filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
                        file_id = hashme(file_url)
                        today = date.today().strftime("%Y-%m-%d")
                        df.loc[len(df.index)] = [file_id, 'WA', group_name, 'www.courts.wa.gov', title,
                                                 file_url, filename, today, filetype]  # add file data to our table
df.to_csv("wa_files.csv", index=False)

