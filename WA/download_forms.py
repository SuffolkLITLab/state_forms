#now we need to download the files

import os
import time
from csv import reader
import requests

with open('wa_files.csv', 'r') as file:
    csv_reader = reader(file)
    next(csv_reader)
    for row in csv_reader:
        file_id = row[0]
        url = row[5]
        if ".docx" in url:
            ftype = ".docx"
        elif ".pdf" in url:
            ftype = ".pdf"

        if os.path.exists(f"forms/{file_id}" + ftype):
            continue

        print("Accessing: " + url)
        response = requests.get(url)
        file = open("forms/" + file_id + ftype, 'wb')
        file.write(response.content)

        time.sleep(3)
    file.close()
