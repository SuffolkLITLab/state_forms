# README

Notes on the code in this folder

# Things to note

GA was the first state encountered with compressed folders containing multiple forms (i.e. zip files). I downloaded them and extracted their content. They were assigned a unique id, which was shared among all the forms inside a zip file. An issue with files inside the zip was that a filename could not be extracted (title is the same as the filename).

# Actions taken

1. Extracts the different categories and the links to those categories.
2. Extracts the individual forms and zip files from the categories. Due to the presence of zip files, some additional functions are used (look helper functions)
3. Helper functions are functions used in every states code
