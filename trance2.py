import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from pathlib import Path

uris = ['/ajax/getmostplayedtracks.php?mode=2&id=2&page=1&idMusicStyle=3&param=4w',
        '/ajax/getmostplayedtracks.php?mode=2&id=2&page=2&idMusicStyle=3&param=4w',
        '/ajax/getmostplayedtracks.php?mode=2&id=2&page=3&idMusicStyle=3&param=4w',
        '/ajax/getmostplayedtracks.php?mode=2&id=2&page=4&idMusicStyle=3&param=4w']

headers = {
    'authority': 'www.1001tracklists.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'guid=70844727796c7',
    'referer': 'https://www.1001tracklists.com/genre/trance/index.html',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

most_played_tracks = []

for uri in uris:
    headers.update(path=uri)
    response = requests.get('https://www.1001tracklists.com' + uri, headers=headers)
    data = response.json()
    tracks = data['data']
    for track in tracks:
        soup = BeautifulSoup(track['trLink'], 'html.parser')
        most_played_tracks.append(soup.text)

print(*most_played_tracks, sep='\n')

curr = [p.stem for p in Path(r'C:\Users\Jefferson\Desktop\trance').glob('*.mp3')]

for t in most_played_tracks:
    for c in curr:
        ra = fuzz.ratio(t, c)
        if ra > 70:
            print('{:100}{:100}{:3}'.format(t, c, ra))
