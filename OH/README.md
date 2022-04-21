# README

Notes on the code in this folder

# Things to note

On the home page of Ohio forms one could find 6 groups of forms. Under each group, there are links to forms and subgroups. The algorithm downloads the forms from the home page, and after proceeds to the pages of subgroups of each grops. Usually we can find form names in "a" tag, but the first group is marked as special case since they have  adifferent structure: for some forms their names are not in "a" but before it. Each form in special case is included in one "p" tag, so we can use "p" tag to get the name of the form.

# Actions taken

1. Divide content by groups presented, ignore "Language Services" since those are translated forms.
2. Get forms that we can find directly on the home page of the forms.
3. Parse subgroups: find forms in "a" tag; for special case, use "p" tag to separate forms.
4. Use cm.py to create metadata for each file.
5. Download each form from metadata table.