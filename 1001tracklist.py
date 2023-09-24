import requests
from bs4 import BeautifulSoup


uris = [
    "/ajax/getmostplayedtracks.php?mode=2&id=2&page=1&idGenre=3&showRank=true&param=2023",
    "/ajax/getmostplayedtracks.php?mode=2&id=2&page=2&idGenre=3&showRank=true&param=2023",
    "/ajax/getmostplayedtracks.php?mode=2&id=2&page=3&idGenre=3&showRank=true&param=2023",
    "/ajax/getmostplayedtracks.php?mode=2&id=2&page=4&idGenre=3&showRank=true&param=2023",
]


most_played_tracks = []

for uri in uris:
    response = requests.get("https://www.1001tracklists.com" + uri)
    data = response.json()
    tracks = data["data"]
    for track in tracks:
        soup = BeautifulSoup(track, "html.parser")
        most_played_tracks.append(soup.select_one("a.spR").text)

print(*most_played_tracks, sep="\n")
