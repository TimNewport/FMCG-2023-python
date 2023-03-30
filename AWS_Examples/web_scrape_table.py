import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.example.com' # replace with the URL of the webpage
table_index = 0 # set to the index of the table you want to download (0 = first table on page)

# retrieve the webpage and parse it with beautifulsoup
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

# find the table you want
table = soup.find_all('table')[table_index]

# download the contents of the table
table_rows = table.find_all('tr')
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)