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

def find_forms(soup):
    forms_dict = dict()
    links = soup.find("div", id="content").find_all("a", href=True)
    for link in links:
        if ".pdf" in link["href"]:
            form_url = link["href"]
            title = link.get_text().strip()
            forms_dict.update({title: form_url})
    return forms_dict

def forms2df(forms_dict, group_name):
    for form in forms_dict:
        title = form
        file_url = forms_dict[form]
        filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
        file_id = hashme(file_url)
        today = date.today().strftime("%Y-%m-%d")
        df.loc[len(df.index)] = [file_id, 'KS', 'kansasjudicialcouncil.org', title,
                                 group_name, file_url, filename, today]  # add file data to our table
        return

def parse_subgroups(url, group_name):
    print(url)
    time.sleep(3)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    container = soup.find("div", class_="container-fluid")
    if container: #continue going deeper if we have more subgroups
        subgroups = container.find_all("a")
        # print("going deeper...")
        for subgroup in subgroups:
            print(subgroup)
            subgroup_url = "https://www.kansasjudicialcouncil.org" + subgroup["href"]
            parse_subgroups(subgroup_url, group_name)
    else: #base case, we have links to forms themselves, not subgroups anymore
        forms_dict = find_forms(soup)
        forms2df(forms_dict, group_name) #put forms into df
        return

def main():
    url = "https://www.kansasjudicialcouncil.org/legal-forms"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    # parse_groups(soup)
    groups = soup.find("div", class_="container-fluid").find_all("a")
    for group in groups:
        group_name = " ".join(group.get_text().split())
        group_url = "https://www.kansasjudicialcouncil.org" + group["href"]
        parse_subgroups(group_url, group_name)
        print("______________________")
    df.to_csv("files.csv", index=False)

main()