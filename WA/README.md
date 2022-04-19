# README

Notes on the code in this folder

# Things to note

Information on Washington is gathered from "List of All Forms". HTML of the page doesn't separate forms by groups explicitly, so I had to use re.split on h3 tags containing the group names applied to the string object of HTML page to split forms by groups.
In my code, I am adding headers to the request to simulate user agent, since the website wouldn't allow to gather information without them.

# Actions taken

1. Extracts groups for forms using re.split and associate forms with them.
2. Extract forms and metadata.
3. Download each form from metadata table.