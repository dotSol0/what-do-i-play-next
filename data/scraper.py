
import requests
from bs4 import BeautifulSoup

def scrape_imslp_metadata(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    data = {}

    rows = soup.find_all("tr")
    for row in rows:
        header = row.find("th")
        value = row.find("td")

        if not header or not value:
            continue

        key = header.get_text(strip=True)
        val = value.get_text(strip=True)

        if key in {
            "Instrumentation",
            "Composer Time Period",
            "Piece Style",
            "First Performance"
        }:
            data[key] = val

    return data
