# README

Notes on the code in this folder

# Things to note

ND was challenging and time-consuming. There were two links for the ND website. The code explicitly mentions in which blocks each link is visited and scraped. The structure of the tables in which the forms resided was very vague. After extracting the group names, the subcategories/pdfs of each group was counted manually (and saved in the **`num_of_forms`** and **`groups_subcats`** arrays). The first six subcategories/pdfs are under the first group, the next five under the second group and so on...

# The script

1. Extracts the different categories and the links included in each category (these include both subcategories and pdfs).
2. In the for-loop, after checking whether the link is a pdf or a subcategory, we either download the page or visit the subcategory and extract the forms included.

# Additional comments

- The first block of every notebook contains the functions and modules necessary to scrape the states (when downloading **.pdf** files, use the **`download_pdf()`** (**`download_pdf_unmasked()`** is for debbuging purposes only).
- **_NEVER_** start by trying to scrape the entire website at once. Break your process into digestible steps.
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not needed.
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata).
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail.
- Some website don't appreciate the multiple (and fast) requests our script is sending to their server. Be gentle with your data provider by adding **`time.sleep()`**.

# Cells to run

- Run all cells to collect the data (for both URLs).
