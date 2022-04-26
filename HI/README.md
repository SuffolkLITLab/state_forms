# README

Notes on the code in this folder

# Things to note

HI was a fairly easy state to scrape. One of the challenges was the extraction of the **titles**. The multipe if statements included in the script exist to deal with the various HTML formats.

The end result was quite unusual. The downloaded files were less than the files saved in the metadata file. This was the result of duplicate downloads. The last block of the notebook extracts the metadata from the file and looks for duplicate keys. After identifying which forms were saved twice in the metadata file, delete the duplicate copies.

# The script

1. Extracts the different categories and the links to these categories (block #2).
2. Extracts the individual forms (block #3). Only pdfs were encountered thus only **`download_pdf()`** was used to obtain the forms.

# Additional comments

- The first block of every notebook contains the functions and modules necessary to scrape the states (when downloading **.pdf** files, use the **`download_pdf()`** (**`download_pdf_unmasked()`** is for debbuging purposes only) .
- **_NEVER_** start by trying to scrape the entire website at once. Break your process into digestible steps.
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not needed.
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata).
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail.
- Some website don't appreciate the multiple (and fast) requests our script is sending to their server. Be gentle with your data provider by adding **`time.sleep()`**.

# Cells to run

- All cells need to be executed for the data to be collected **_except_** from the last block. One should run the last block if and only if incosistencies are found between the number of forms downloaded and the number of forms saved in the metadata file.
