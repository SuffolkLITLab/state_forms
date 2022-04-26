# README

Notes on the code in this folder

# Things to note

Most of Wyoming's forms are gathered in tables that could be found under different groups, but some of them show up in lists outside of table, so we have li_forms() function for forms under "li" tag, and table_forms() under "table" tag. In my code, I am adding headers to the request to simulate user agent, since the website wouldn't allow to gather information without them.

# Actions taken

1. Extracts groups for forms and associate forms with them.
2. Check in which way the forms may be present: table or lists, extract forms and metadata from each.
3. Make a metadata table, download each form.
