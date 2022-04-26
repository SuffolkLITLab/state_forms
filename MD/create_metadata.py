import hashlib
import re
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

df = pd.DataFrame(columns=['id', 'jurisdiction', 'source', 'title',
                           'group', 'url', 'filename', 'downloaded_on'])

def hashme(w):
    h = hashlib.md5(w.encode('utf-8'))
    return h.hexdigest()

def get_forms(soup):
    forms = soup.find_all("div", class_="views-row")
    for form in forms:
        title = form.find("h1", class_="form-title").get_text().strip()
        file_url_list = form.find_all("span", class_="file file--mime-application-pdf file--application-pdf")
        if len(file_url_list)==0: #no file for form, skip
            continue
        file_url = file_url_list[0].find("a")["href"]
        group_name_list = form.find_all("div", class_="field field--name-field-type field--type-entity-reference field--label-inline clearfix")
        if len(group_name_list)==0: #that means this is not a form but a brochure, skip
            continue
        group_name = group_name_list[0].find("div", class_="field__item").get_text()
        filename = re.search('.*\/(.*\.pdf)', file_url).group(1)
        file_id = hashme(file_url)
        today = date.today().strftime("%Y-%m-%d")
        df.loc[len(df.index)] = [file_id, 'MD', 'www.courts.state.md.us', title,
                                 group_name, file_url, filename, today]  # add file data to our table
    return

def parse_page():
    driver.implicitly_wait(10) #wait in case page is not fully loaded

    # get the forms
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    get_forms(soup)

    #go to next page
    #find the 'next page' button
    next_page_button = driver.find_elements(by=By.CSS_SELECTOR, value = '#block-mdjudiciary-content > div > div > nav > ul > li.pager__item.pager__item--next')
    if len(next_page_button) > 0: #found a "next" element (we're not at the last page rn)
        next_page_button[0].click()
    else: #this is the last page
        return

    time.sleep(3)
    parse_page()


# open the browser
driver = webdriver.Chrome('/Users/lerasomova/PycharmProjects/courts1/maryland/chromedriver')
driver.get("https://www.courts.state.md.us/courtforms?forms%5B0%5D=languages%3A59")
parse_page()
driver.close()
df.to_csv("files.csv", index=False)