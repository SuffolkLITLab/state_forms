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

        if os.path.exists(f"pdf_forms/{file_id}" + ".pdf"):
            continue

        print("Accessing: " + url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        pdf = open("pdf_forms/" + file_id + ".pdf", 'wb')
        pdf.write(response.content)

        time.sleep(3)
    pdf.close()
