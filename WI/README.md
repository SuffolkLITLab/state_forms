# README

Notes on the code in this folder

# Things to note

WI was a fairly easy state. The number of pages of each category were derived manually. After saving these numbers into **`cat_page_count`** array, this information was to used to visit all the different pages of each category (by making use a formated URL)

# The script

1. Extracts the names of categories and the link to these categories.
2. After visiting the individual categories, the forms were extracted.

# Additional comments

- The first block of every notebook contains the functions and modules necessary to scrape the states (when downloading **.pdf** files, use the **`download_pdf()`** (**`download_pdf_unmasked()`** is for debbuging purposes only).
- **_NEVER_** start by trying to scrape the entire website at once. Break your process into digestible steps.
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not needed.
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata).
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail.
- Some website don't appreciate the multiple (and fast) requests our script is sending to their server. Be gentle with your data provider by adding **`time.sleep()`**.

# Cells to run
