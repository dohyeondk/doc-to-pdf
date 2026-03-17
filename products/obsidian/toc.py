import requests
from shared.types import TocItem

SITE_UID = "f786db9fac45774fa4f0d8112e232d67"
BASE_URL = "https://help.obsidian.md"
OPTIONS_API = f"https://publish-01.obsidian.md/options/{SITE_UID}"
CACHE_API = f"https://publish-01.obsidian.md/cache/{SITE_UID}"


def _make_toc_entry(path: str) -> TocItem:
    title = path.rsplit("/", 1)[-1].removesuffix(".md")
    url_path = path.removesuffix(".md").replace(" ", "+")
    section = path.split("/")[0] if "/" in path else None
    return TocItem(
        type="page",
        title=title,
        url=f"{BASE_URL}/{url_path}",
        section=section,
    )


def _make_section_entry(folder_name: str) -> TocItem:
    title = folder_name.rsplit("/", 1)[-1]
    return TocItem(
        type="section",
        title=title,
        url=None,
        section=folder_name.split("/")[0],
    )


def get_toc_items() -> list[TocItem]:
    """Get the ordered list of documentation pages from the Obsidian Publish API."""
    response = requests.get(OPTIONS_API, timeout=30)
    response.raise_for_status()
    options = response.json()

    cache_response = requests.get(CACHE_API, timeout=30)
    cache_response.raise_for_status()
    all_cache_pages = set(cache_response.json().keys())

    nav_ordering = options.get("navigationOrdering", [])
    hidden_items = set(options.get("navigationHiddenItems", []))

    skip_prefixes = ("Attachments", "favicon", "publish.")
    skip_exact = {"Home.md"}

    nav_set = set(nav_ordering)

    toc_items = []
    seen = set()

    for entry in nav_ordering:
        if entry.endswith(".md"):
            if entry in hidden_items or entry in skip_exact:
                continue
            if any(entry.startswith(p) for p in skip_prefixes):
                continue
            if entry in seen:
                continue
            seen.add(entry)
            toc_items.append(_make_toc_entry(entry))
        else:
            if any(entry.startswith(p) for p in skip_prefixes):
                continue

            toc_items.append(_make_section_entry(entry))

            folder_prefix = entry + "/"
            has_explicit_children = any(
                e.startswith(folder_prefix) and e.endswith(".md")
                for e in nav_set
            )

            if not has_explicit_children:
                child_pages = sorted(
                    p for p in all_cache_pages
                    if p.startswith(folder_prefix)
                    and p.endswith(".md")
                    and p not in hidden_items
                    and p not in seen
                )
                for child in child_pages:
                    if any(child.startswith(p) for p in skip_prefixes):
                        continue
                    seen.add(child)
                    toc_items.append(_make_toc_entry(child))

    return toc_items
