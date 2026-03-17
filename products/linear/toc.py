from playwright.sync_api import sync_playwright
from shared.types import TocItem

BASE_URL = "https://linear.app"
DOCS_URL = f"{BASE_URL}/docs"


def _scrape_nav_structure() -> list[dict]:
    """Scrape the sidebar navigation from Linear docs using Playwright.

    The sidebar uses collapsible sections that must be expanded before
    the child links appear in the DOM.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.goto(DOCS_URL, wait_until="networkidle")

            # Expand all collapsed sidebar sections
            page.evaluate("""() => {
                document.querySelectorAll('[class*="Collapsible_button"]').forEach(btn => {
                    if (btn.getAttribute('data-state') === 'closed') {
                        btn.click();
                    }
                });
            }""")
            page.wait_for_timeout(1000)

            # Extract sections and their child links
            return page.evaluate("""() => {
                const sidebar = document.querySelector('[class*="Sidebar_listInner"]');
                if (!sidebar) return [];

                return Array.from(sidebar.children).map(li => {
                    const button = li.querySelector('[class*="Collapsible_button"]');
                    const section = button ? button.textContent.trim() : '';

                    const links = Array.from(li.querySelectorAll('a[href^="/docs/"]')).map(a => ({
                        title: a.textContent.trim(),
                        href: a.getAttribute('href'),
                    })).filter(l => l.title && l.href);

                    return {section, links};
                });
            }""")
        finally:
            browser.close()


def get_toc_items() -> list[TocItem]:
    """Build flat TOC list with section dividers from live sidebar."""
    nav_structure = _scrape_nav_structure()

    items = []
    seen_hrefs = set()

    for group in nav_structure:
        section = group["section"]
        if not section or not group["links"]:
            continue

        items.append(TocItem(
            type="section",
            title=section,
            url=None,
            section=section,
        ))

        for link in group["links"]:
            href = link["href"]
            if href in seen_hrefs:
                continue
            seen_hrefs.add(href)
            items.append(TocItem(
                type="page",
                title=link["title"],
                url=f"{BASE_URL}{href}",
                section=section,
            ))

    return items
