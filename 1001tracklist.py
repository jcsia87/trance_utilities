import argparse
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.1001tracklists.com"
ENDPOINT = f"{BASE_URL}/ajax/getmostplayedtracks.php"
PAGE_SIZE = 10
MAX_PAGES = 10  # Server cap matching StatisticUpdater.maxPages in framework.js


def get_top_trance_tracks(period: str = "3m", max_pages: int = MAX_PAGES) -> list[dict]:
    """Fetch top trance tracks from 1001Tracklists for the given time period.

    Valid periods from the left submenu: '4w', '3m', '6m', '12m', '2026', '2025'.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Referer": f"{BASE_URL}/genre/trance/index.html",
            "X-Requested-With": "XMLHttpRequest",
        }
    )

    tracks = []
    for page in range(1, min(max_pages, MAX_PAGES) + 1):
        response = session.get(
            ENDPOINT,
            params={
                "mode": 2,          # Top / most played tracks
                "id": 2,            # Genre-scoped chart
                "idGenre": 3,       # Trance
                "param": period,    # e.g. '3m' = Last 3 Months
                "showRank": "true",
                "page": page,
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()

        items = payload.get("data") or []
        if not payload.get("success") or not items:
            break

        for html_fragment in items:
            soup = BeautifulSoup(html_fragment, "html.parser")
            rank_el = soup.select_one(".bRank")
            title_el = soup.select_one(".ml5 > a") or soup.select_one("a")
            plays_el = soup.select_one(".playC span")
            label_el = soup.select_one(".trackLabel")

            if not title_el:
                continue

            tracks.append(
                {
                    "rank": int(rank_el.get_text(strip=True)) if rank_el else len(tracks) + 1,
                    "title": title_el.get_text(strip=True),
                    "plays": int(plays_el.get_text(strip=True)) if plays_el else None,
                    "label": " ".join(label_el.get_text().split()) if label_el else None,
                    "url": BASE_URL + title_el["href"] if title_el.get("href") else None,
                }
            )

        if len(items) < PAGE_SIZE:
            break

    return tracks


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch top Trance tracks from 1001Tracklists.")
    parser.add_argument(
        "--period",
        default="3m",
        help="Timeframe from the left menu (4w, 3m, 6m, 12m, 2026, 2025). Default: 3m",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=MAX_PAGES,
        help="Number of pages to fetch (10 tracks per page, max 10). Default: 10",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Include rank, DJ support play count, and label in output.",
    )
    args = parser.parse_args()

    tracks = get_top_trance_tracks(period=args.period, max_pages=args.pages)
    for track in tracks:
        if args.details:
            plays = f"{track['plays']} plays" if track["plays"] is not None else "? plays"
            label = f" [{track['label']}]" if track["label"] else ""
            print(f"{track['rank']:>3}. {track['title']}{label} ({plays})")
        else:
            print(track["title"])


if __name__ == "__main__":
    main()
