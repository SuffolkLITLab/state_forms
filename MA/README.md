# README

Notes on the code in this folder

# Things to note

MA was the first state that was scraped and as a result the code is quite messy. Unlike other notebooks, this one **does not** start with the helper functions but rather with collecting the categories later used in block #8. An unusual number of errors were encountered during download. As a result, **_Selenium_** was used to extract most of these faulty forms.

# The script

1. Extracts the different categories and the links to these categories.
2. Extracts the individual forms and zip files from the categories. Due to the presence of zip files, some additional functions are used (look helper functions).

# Additional comments

- **_NEVER_** start by trying to scrape the entire website at once. Break your process into digestible steps.
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not needed.
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata).
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail.
- Some website don't appreciate the multiple (and fast) requests our script is sending to their server. Be gentle with your data provider by adding **`time.sleep()`**.

# Cells to run

- To collected the data, run every cell up to cell #8.
- From cells #9 and onwards, **_Selenium_** is being used in the efforts to retrieve most of the forms that were downloaded unsuccesfully. The code makes use of the **_Save as PDF_** button provided by the MA website. Most of the forms were succesfully downloaded using this method.
- The **_Selenium_** approach was far from perfect. The HTML was varying a lot between pages and as a result the script was not always able to locate the saving button. In the cases were the script fails to download the page, the browser freezes in the page in which the error occured and thus a manual download was used.
