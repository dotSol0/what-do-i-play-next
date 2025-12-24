import requests
from bs4 import BeautifulSoup

TARGET_KEYS = {
    "Instrumentation",
    "Key",
    "Piece Style",
    "First Performance",
    "Year/Date of Composition",
    "Composer Time Period",
    "Average Duration"
}

def scrape_imslp_metadata(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    for row in soup.select("table tr"):
        th = row.find("th")
        td = row.find("td")

        if not th or not td:
            continue

        # 🔑 STRATEGY 1: Look for the specific 'Main Header' class (mh555)
        # This ensures we get "Average Duration" and ignore "Avg. Duration"
        main_label = th.find("span", class_="mh555")
        
        if main_label:
            key = main_label.get_text(strip=True)
        else:
            # 🔑 STRATEGY 2: Fallback for rows without spans (e.g., "Instrumentation")
            # We use stripped_strings to handle any bold/italic tags inside the header
            key = " ".join(th.stripped_strings).strip()

        # Clean up the key (remove trailing colons if any, e.g. "Key:")
        key = key.rstrip(":")

        if key in TARGET_KEYS:
            # For the value, using get_text with a separator ensures lines don't mash together
            data[key] = td.get_text(" ", strip=True)

    return data

#test
row = scrape_imslp_metadata('https://imslp.org/wiki/Amicizia_(Stankovych,_Tatiana)')
print(row)