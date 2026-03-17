# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python monorepo that downloads documentation websites as single PDFs with bookmarked table of contents. Uses Playwright (Chromium) to render pages, then merges them with pypdf.

## Setup & Commands

```bash
uv sync                        # Install dependencies
playwright install chromium    # Install browser (first time only)

# Run a product (see products/ for available ones)
python -m products.<name>

# With options
python -m products.<name> --font-scale 90 --paper-size A4
```

Python 3.10+, managed with uv. Virtual env at `.venv/`. No test suite exists.

```bash
# Linting & formatting
uv run ruff check .            # Lint
uv run ruff check --fix .      # Lint with auto-fix
uv run ruff format .            # Format
```

## Architecture

**Two-layer design: shared library + product modules.**

`shared/` is the reusable PDF generation pipeline:
- `types.py` — Core dataclasses: `TocItem` (page/section entry), `PdfConfig` (paper/margins/scale), `ProductSpec` (per-site CSS/JS/selectors)
- `pipeline.py` — Orchestrator: iterates TOC items, downloads each page as PDF via Playwright, generates section divider pages, then merges all into one PDF with bookmarks
- `pdf_page.py` — Renders a single URL to PDF: injects custom CSS/JS from ProductSpec, waits for page load, optionally scrolls for lazy images
- `section_page.py` — Generates section title divider PDFs
- `pdf_merge.py` — Merges individual PDFs into one with bookmarked TOC using pypdf
- `browser.py` — Playwright browser lifecycle (context manager)
- `config.py` — CLI argument parsing into `PdfConfig`

`products/<name>/` each contain three files:
- `__main__.py` — Entry point: calls `parse_args()`, `get_toc_items()`, `run_pipeline()`
- `config.py` — `PRODUCT_SPEC` with site-specific CSS, JS injection, content selector, and metadata
- `toc.py` — `get_toc_items()` returns `list[TocItem]` (how TOC is built varies: hardcoded, API, or HTML scraping)

## Adding a New Product

Create `products/mysite/` with `__init__.py`, `__main__.py`, `config.py`, `toc.py` following the pattern of existing products. The key customization points are the CSS/JS in `config.py` (to strip navigation chrome and force light theme) and the TOC source in `toc.py`.

## Release Process

1. Run lint: `uv run ruff check .` and `uv run ruff format --check .`
2. Push to `main` (CI runs lint via GitHub Actions)
3. Tag and push: `git tag v<version> && git push --tags`
4. GitHub Actions generates all PDFs and creates a Release with them attached

## Key Design Decisions

- Each page is rendered and saved as an individual PDF first (to `<name>-docs-pdf/` directory), then merged. This allows incremental re-runs — existing PDFs are skipped.
- `font_scale=100` maps to Chromium scale `0.85` (the baseline). The `chromium_scale` property on `PdfConfig` handles conversion.
- Products with `has_sections=True` get section divider pages inserted as TOC hierarchy; flat products just list pages.
- Output directories (`*-docs-pdf/`) and PDFs (`*.pdf`) are gitignored.
