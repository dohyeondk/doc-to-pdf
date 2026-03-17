---
name: add-doc
description: Scaffold a new documentation product for doc-to-pdf. Use when the user wants to add a new documentation site to download as PDF.
disable-model-invocation: false
user-invocable: true
argument-hint: <site-name> <docs-url>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, WebFetch
---

# Add New Documentation Product

You are adding a new product to the doc-to-pdf monorepo. A "product" is a documentation website that gets downloaded as a single PDF with bookmarked table of contents.

## Input

The user provides: `$ARGUMENTS`

Parse this for:
- **site-name**: lowercase identifier (e.g., `raycast`, `tailwind`). This becomes the directory name under `products/`.
- **docs-url**: the documentation site URL to scrape.

If either is missing, ask the user before proceeding.

## Steps

### 1. Investigate the documentation site

Before writing any code, visit the docs URL and understand:

- **Navigation structure**: How is the sidebar/TOC organized? Is it flat or has sections?
- **Content selector**: What CSS selector wraps the main content? (e.g., `main`, `.content`, `article`)
- **Elements to hide**: What needs CSS `display: none` for clean PDF output? (nav, header, footer, sidebar, TOC widgets, cookie banners, etc.)
- **Lazy loading**: Does the site lazy-load images? (check for `loading="lazy"` attributes)
- **Wait strategy**: Does the site need `networkidle` (heavy JS) or `load` (static/SSR)?
- **TOC source**: How to get the page list — scrape sidebar HTML, call an API, or hardcode?

Use `WebFetch` to inspect the docs page HTML. Look at the sidebar/navigation to understand the TOC structure.

### 2. Create the product directory

Create `products/<site-name>/` with these 4 files:

#### `__init__.py`
Empty file.

#### `config.py`
```python
from shared.types import ProductSpec

CUSTOM_CSS = """
/* Hide navigation chrome, headers, footers for clean PDF output */
<selectors-to-hide> {
    display: none !important;
}

/* Fix body/content overflow for proper PDF rendering */
<content-layout-fixes>
"""

# Optional: JS to run before PDF generation (e.g., expand collapsed sections, remove overlays)
PREPARE_JS = None  # or a JS string

PRODUCT_SPEC = ProductSpec(
    name="<Display Name>",
    custom_css=CUSTOM_CSS,
    prepare_js=PREPARE_JS,
    content_selector="<main-content-selector or None>",
    wait_until="<networkidle or load>",
    scroll_for_lazy_images=<True or False>,
    pdf_metadata_title="<Display Name> Documentation",
    pdf_metadata_author="<Company/Author>",
    has_sections=<True if TOC has section groupings, False if flat>,
)
```

Key decisions:
- `content_selector`: Set if the page has a clear content wrapper to wait for. Leave `None` if not needed.
- `wait_until`: Use `"networkidle"` for JS-heavy sites, `"load"` for static/SSR sites.
- `scroll_for_lazy_images`: Set `True` only if the site uses lazy-loaded images.
- `has_sections`: Set `True` if the TOC has grouped sections (generates divider pages). `False` for flat page lists.

#### `toc.py`
```python
from shared.types import TocItem

def get_toc_items() -> list[TocItem]:
    """Build the ordered list of documentation pages."""
    # Choose ONE approach:
    #
    # A) HTML scraping (most common) — parse the sidebar from the docs URL
    # B) API-based — fetch from a documentation API if available
    # C) Hardcoded — manually list pages (last resort, requires manual updates)
    ...
```

Each `TocItem` has:
- `type`: `"page"` or `"section"` (section = divider page, only if `has_sections=True`)
- `title`: Display title for the bookmark
- `url`: Full URL for pages, `None` for sections
- `section`: Parent section name or `None`

**For HTML scraping**, use `requests` + `BeautifulSoup`:
```python
import requests
from bs4 import BeautifulSoup
from shared.types import TocItem

BASE_URL = "https://..."

def get_toc_items() -> list[TocItem]:
    response = requests.get(BASE_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    # Find sidebar links, build TocItem list
    ...
```

Always include `timeout=30` on network requests.

#### `__main__.py`
```python
from shared.product_main import product_main
from products.<site_name>.config import PRODUCT_SPEC
from products.<site_name>.toc import get_toc_items

if __name__ == "__main__":
    product_main(PRODUCT_SPEC, get_toc_items)
```

### 3. Test the TOC

Run the TOC function to verify it returns sensible items:

```bash
python -c "from products.<site_name>.toc import get_toc_items; items = get_toc_items(); print(f'{len(items)} items'); [print(f'  [{i.type}] {i.title} -> {i.url}') for i in items[:10]]"
```

Check:
- Correct number of pages
- URLs are valid and complete
- Titles are readable
- Sections (if any) appear before their child pages

### 4. Test a single page PDF

Do a quick test downloading just one page:

```bash
python -c "
from shared.browser import managed_browser
from shared.pdf_page import download_page_as_pdf
from shared.types import PdfConfig
from products.<site_name>.config import PRODUCT_SPEC
import logging; logging.basicConfig(level=logging.INFO, format='%(message)s')

config = PdfConfig()
with managed_browser() as browser:
    download_page_as_pdf('<first-page-url>', '/tmp/test-page.pdf', browser, config, PRODUCT_SPEC, skip_existing=False)
print('Done — check /tmp/test-page.pdf')
"
```

Open the PDF and verify:
- Navigation chrome is hidden
- Content is readable and properly formatted
- No overlapping elements or broken layouts
- Images loaded (if any)

If the PDF looks wrong, iterate on `CUSTOM_CSS` and `PREPARE_JS` in `config.py`.

### 5. Add output directory to .gitignore

The output directory pattern `<site-name>-docs-pdf/` should already be covered by the existing gitignore. Verify with:

```bash
grep "docs-pdf" .gitignore
```

If not covered, note this to the user.

### 6. Summary

After creating all files, print:
- The product name and docs URL
- Number of TOC items found
- How to run: `python -m products.<site_name>`
- Any caveats (fragile selectors, missing pages, etc.)
