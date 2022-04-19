import requests
from bs4 import BeautifulSoup
from cm import *
import pandas as pd

def find_direct_forms(links):
    direct_forms = []
    for link in links:
        if ".pdf" in link["href"]:
            direct_forms.append(link)
    return direct_forms

def find_forms_directories(links):
    forms_directories = []
    for link in links:
        if "uploads" not in link["href"]: #then it is not a file
            forms_directories.append(link)
    return forms_directories

def process_direct_forms(links):
    for link in links:
        title = link.get_text()
        file_url = link["href"]
        group_name = "Unified Judicial System Forms"
        create_metadata(title, file_url, group_name, "SD", "https://ujslawhelp.sd.gov")

def process_directories(links):
    df = pd.DataFrame(columns=['group', 'link'])
    for link in links:
        if "https" in link["href"]: #not an absolute path
            dir_url = link["href"]
        else: #relative path
            dir_url = "https://ujslawhelp.sd.gov/" + link["href"]
        group_name = link.get_text()
        df.loc[len(df.index)] = [group_name, dir_url]  # df with links to each group
        df.to_csv("group_links.csv")

url = 'https://ujslawhelp.sd.gov/onlineforms.aspx'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')
divs = soup.find_all("div", class_="courtmembers")
# some of the links are forms, some - directories.
# for forms taken directly from this page we put group as "Unified Judicial System Forms"
links = []
for div in divs:
    links += div.find_all("a")

direct_forms = find_direct_forms(links) #list of direct forms (pdfs derived directly from first page)
forms_directories = find_forms_directories(links)

# process direct forms
process_direct_forms(direct_forms)

# process directories
process_directories(forms_directories) #we put all groups w respectieve links to each file, continue in 2.py