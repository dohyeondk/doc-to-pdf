# doc-to-pdf

Download documentation sites as single PDFs with bookmarked table of contents.

## Supported Products

| Product | Command | Sections | Source |
|---------|---------|----------|--------|
| [Linear](https://linear.app/docs/) | `python -m products.linear` | 15 sections, ~97 pages | Playwright sidebar scraping |
| [Obsidian](https://help.obsidian.md/) | `python -m products.obsidian` | Sections from Publish API | Obsidian Publish API |
| [Zed](https://zed.dev/docs/) | `python -m products.zed` | Flat (no sections) | HTML sidebar scraping |

## Installation

```bash
git clone https://github.com/dohyeondk/doc-to-pdf.git
cd doc-to-pdf
uv sync
playwright install chromium
```

## Usage

```bash
# Generate with default settings (Letter, 100% scale)
python -m products.linear
python -m products.obsidian
python -m products.zed

# Customize output
python -m products.linear --font-scale 90 --paper-size A4
python -m products.obsidian --margin-left 0.5 --margin-right 0.5
python -m products.zed --no-background
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--font-scale` | `100` | Font scale percentage (100 = baseline readable size) |
| `--paper-size` | `Letter` | Paper size: Letter, A4, Legal, Tabloid |
| `--margin-top` | `0.45` | Top margin in inches |
| `--margin-right` | `0.25` | Right margin in inches |
| `--margin-bottom` | `0.45` | Bottom margin in inches |
| `--margin-left` | `0.25` | Left margin in inches |
| `--no-strip-blank` | off | Disable trailing blank page removal |
| `--no-background` | off | Disable background printing |

## Adding a New Product

Create a new directory under `products/` with three files:

```
products/mysite/
    __init__.py
    __main__.py    # Entry point (see existing products for template)
    config.py      # PRODUCT_SPEC with CSS/JS and site-specific settings
    toc.py         # get_toc_items() -> list[TocItem]
```

## Architecture

```
shared/           # Reusable PDF generation library
    types.py      # TocItem, PdfConfig, ProductSpec dataclasses
    config.py     # CLI argument parsing
    browser.py    # Playwright browser lifecycle
    pdf_page.py   # Single page -> PDF with CSS/JS injection
    section_page.py  # Section title divider pages
    pdf_merge.py  # Merge PDFs with bookmarked TOC
    pdf_utils.py  # Filename sanitization, blank page stripping
    pipeline.py   # Orchestration: download all + merge

products/         # Site-specific modules
    <name>/       # One directory per documentation site
```

## License

MIT
