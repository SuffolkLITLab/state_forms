# README

Notes on the code in this folder

# The script

-At first glance, we cannot see any categories. When such a website is encountered, try extracting the category list of the **Search** dropdown menu. Since only the names of the categories are found and not their urls, you need to search for clues that will allow you to navigate to individual categories. By manipulating the **start** url (found by inspecting the **_Load More_** button at the bottom), navigating to individual groups became possible.
-The **page_nums** array contains the number of pages that each category has (manually derived).

- The third block of the notebook contains the main logic (which is very similar to other scripts):
  - For each category, we extract the forms from each page and build our metadata file.

# Additional comments

- The first block of every notebook contains the functions and modules necessary to scrape the states (when downloading **.pdf** files, use the **`download_pdf()`** (**`download_pdf_unmasked()`** is for debbuging purposes only) .
- **_NEVER_** start by trying to scrape the entire website at once. Break your process into digestible steps.
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not needed.
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata).
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail.
- Some website don't appreciate the multiple (and fast) requests our script is sending to their server. Be gentle with your data provider by adding **`time.sleep()`**.

# Cells to run

- All blocks of code need to be executed for the data to be collected.
- The **status** column in the dataframe in which the metada data are being saved is used to identify downloads that produced an error. If these errors don't constitute the majority of the downloads, it is recommended to search the download folder and delete the faulty documents. If more than 20% of the downloads resulted into an error, something might be wrong with the script.
