# README

Notes on the code in this folder

# Things to note

GA had many compressed folders containing multiple forms (i.e. zip files). After downloading them, their content was extracte. They were assigned a unique id, which was shared among all the forms inside a zip file. An issue with files inside the zip was that a filename could not be extracted (title is the same as the filename).

# The script:

1. Extracts the different categories and the links to these categories.
2. Extracts the individual forms and zip files from the categories. Due to the presence of zip files, some additional functions are used (look helper functions).


# Additional comments 

- The first block of every notebook contains the functions and modules necessary to scrape the states (when downloading **.pdf** files, use the **`download_pdf()`** (**`download_pdf_unmasked()`** is for debbuging purposes only) . 
- ***NEVER*** start by trying to scrape the entire website at once. Break your process in small steps. 
  - Start by making two arrays; one for the different form categories and one for their unique urls. If all the categories are part of the same page, the latter is not    needed. 
  - When you make sure the categories are extracted succesfully, continue by accessing the individual categories and collecting the forms (along with the necessary metadata). 
  - Once the forms are collected, check your metadata file for downloads that resulted into an error. If more than 20% of the collected **.pdf** files have an error status, use **`download_pdf_unmasked()`** and attempt to download the files again. This will allow you to see the error that caused the original function to fail. 
