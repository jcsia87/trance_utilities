import requests
from bs4 import BeautifulSoup

URL = 'https://www.1001tracklists.com/charts/trance/weekly/index.html'
URL2 = 'https://www.1001tracklists.com/charts/trance/weekly/index2.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for i in soup.select(".iBlock > a"):
    print(i.text)

page = requests.get(URL2, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for i in soup.select(".iBlock > a"):
    print(i.text)

input()