# special case: in this subgroup some forms have content of "a" link which is not a name of the form
import sys

import requests
from bs4 import BeautifulSoup
import pandas as pd
from cm import *

SPECIAL_CASE = "Domestic and Juvenile"

def get_special_forms(soup, group_name):
    paragraphs = soup.find_all("p") #each paragraph - max one form
    for p in paragraphs:
        links = p.find_all("a", href=True)
        for link in links:
            if ".pdf" in link["href"]:
                file_url = "http://www.supremecourt.ohio.gov" + link["href"]
                title = link.get_text().strip()
                if title == "PDF":
                    title = p.find(text=True, recursive=False).strip()
                    if title[-1]=="(":
                        title = title[:-1].strip() #clean up since some text ends with "("
                create_metadata(title, file_url, group_name, "OH", "www.supremecourt.ohio.gov")
                break #we're done with this form
    # sys.exit()
#     get a tags w .pdf
# if name of a is pdf then get direct text as title

def get_forms(soup, group_name, special_case):
    if special_case:
        get_special_forms(soup, group_name)
    a_tags = soup.find_all("a", href=True)
    for a_tag in a_tags:
        if ".pdf" in a_tag["href"]:
            file_url = a_tag["href"]
            if "http" not in file_url:
                file_url = "http://www.supremecourt.ohio.gov" + file_url
            title = a_tag.get_text()
            create_metadata(title, file_url, group_name, "OH", "www.supremecourt.ohio.gov")

def parse_subgroups(soup, group_name, special_case):
    a_tags = soup.find_all("a", href=True)
    for a_tag in a_tags:
        if ".pdf" not in a_tag["href"]:
            subgroup_url = "https://www.supremecourt.ohio.gov" + a_tag["href"]
            response = requests.get(subgroup_url)
            soup = BeautifulSoup(response.text, 'html5lib')
            get_forms(soup, group_name, special_case)


def parse_groups(soup):
    group_name = soup.find("strong").get_text()
    if group_name == "Language Services": #translated forms, we dont need them
        return

    #   get forms from this group
    get_forms(soup, group_name, special_case=False) #special case is false because we're at the home page right now, SC is for subgroups only

    #   we may have subgroups in this group, parse them

    if group_name==SPECIAL_CASE:
        special_case = True
    else:
        special_case = False

    parse_subgroups(soup, group_name, special_case)




def main():
    df = pd.DataFrame(columns=['group', 'link'])
    url = 'https://www.supremecourt.ohio.gov/JCS/courtSvcs/forms.asp'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html5lib')
    groups_soup = soup.find_all("dl")
    for gs in groups_soup:
        parse_groups(gs)

main()