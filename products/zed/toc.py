import logging

import requests
from bs4 import BeautifulSoup

from shared.types import TocItem

log = logging.getLogger(__name__)

BASE_URL = "https://zed.dev/docs"
REQUEST_TIMEOUT = 30


def get_toc_items() -> list[TocItem]:
    """Get the list of TOC items from Zed documentation via HTML scraping."""
    try:
        response = requests.get(BASE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch Zed docs from {BASE_URL}: {e}") from e

    soup = BeautifulSoup(response.text, "html.parser")

    nav = soup.find(id="sidebar")
    if not nav:
        raise ValueError("Could not find navigation menu")

    toc_items = []
    seen_urls = set()

    chapter_items = nav.find_all(class_="chapter-item")

    for item in chapter_items:
        link = item.find("a")
        if not link:
            continue

        text = link.get_text(strip=True)
        href = link.get("href", "")

        if not text or not href or href in seen_urls:
            continue

        full_url = f"{BASE_URL}/{href}"

        seen_urls.add(href)
        toc_items.append(
            TocItem(
                type="page",
                title=text,
                url=full_url,
                section=None,
            )
        )

    return toc_items
