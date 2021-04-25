import requests
from bs4 import BeautifulSoup

trance_100 = 'https://www.beatport.com/genre/trance/7/top-100'

page = requests.get(trance_100)
soup = BeautifulSoup(page.content, 'html.parser')
print('==========Trance - Top 100 Tracks==========')
for i in soup.select(".ec-item"):
    title = i.select_one('.buk-track-primary-title').text
    mix = i.select_one('.buk-track-remixed').text
    print("{}. {} - {} ({})".format(i['data-ec-position'], i['data-ec-d1'], title, mix))

input()
