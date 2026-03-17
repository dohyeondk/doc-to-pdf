from collections.abc import Generator
from contextlib import contextmanager

from playwright.sync_api import Browser, sync_playwright


@contextmanager
def managed_browser() -> Generator[Browser, None, None]:
    """Context manager that yields a reusable Chromium browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            yield browser
        finally:
            browser.close()
