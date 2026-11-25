import time
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA_DIR = Path("data")

# name_topic -> official URL
SOURCES = {
    "ssa_ssn": "https://www.ssa.gov/number-card",
    "uscis_greencard": "https://www.uscis.gov/green-card",
    "state_immigrantvisa": "https://travel.state.gov/content/travel/en/us-visas/immigrate/the-immigrant-visa-process.html",
}

HEADERS = {
    "User-Agent": "Ceylon2US student project (github.com/rishikaevenjalin-bit/ceylon2us)"
}


def fetch_page_text(url):
    """Download a web page and return only its readable text."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()

    main_content = soup.find("main") or soup.body
    return main_content.get_text(separator="\n", strip=True)


def main():
    today = date.today().isoformat()

    for name, url in SOURCES.items():
        try:
            text = fetch_page_text(url)
        except requests.RequestException as error:
            print(f"❌ {name}: {error}")
            continue

        out_path = DATA_DIR / f"{name}_{today}.txt"
        out_path.write_text(f"SOURCE URL: {url}\n\n{text}", encoding="utf-8")
        print(f"✅ {name}: {len(text.split())} words -> {out_path.name}")

        time.sleep(2)


if __name__ == "__main__":
    main()
