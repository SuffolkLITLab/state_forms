# download all pdf files in our table
import os
import time
from csv import reader

import requests

with open('files.csv', 'r') as file:
    csv_reader = reader(file)
    next(csv_reader)
    for row in csv_reader:
        file_id = row[0]
        url = row[5]
        filetype = row[8]

        if os.path.exists(f"pdf_forms/{file_id}" + filetype):
            continue

        print("Accessing: " + url)
        response = requests.get(url)
        pdf = open("pdf_forms/" + file_id + filetype, 'wb')
        pdf.write(response.content)

        time.sleep(3)
    pdf.close()
