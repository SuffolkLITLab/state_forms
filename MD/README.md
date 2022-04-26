# README

Notes on the code in this folder

# Things to note

To gather forms of Maryland, one has to move between pages. The original idea was to extract the link to the next page and download the HTML from the next page, but the website turned out to use JavaScript to move between pages, so each time I was trying to acces the next page, my program would return the data from the first page. To overcome this problem, I had to use Selenium to switch between pages.

# Actions taken

1. Open the browser with Selenium, apply BeautifulSoup to driver.page_source. Get metadata for each form on this page.
2. Use Selenium to switch to the next page. Repeat the first step for each page.
3. Download each form from metadata table.