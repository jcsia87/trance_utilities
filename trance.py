import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

URL = 'https://www.1001tracklists.com/charts/trance/weekly/index.html'
URL2 = 'https://www.1001tracklists.com/charts/trance/weekly/index2.html'
headers = {
    'authority': 'www.1001tracklists.com',
    'scheme': 'https',
    'path': '/charts/trance/weekly/index.html',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'
}

tracks = []

# collect tracks from 1001tracklists
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for i in soup.select(".iBlock > a"):
    tracks.append(i.text)

page = requests.get(URL2, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
for i in soup.select(".iBlock > a"):
    tracks.append(i.text)

# compare with owned tracks
with open('current.txt') as f:
    curr = [line.strip() for line in f]

for t in tracks:
    for c in curr:
        ra = fuzz.ratio(t, c)
        if ra > 70:
            print('{:100}{:100}{:3}'.format(t, c, ra))
