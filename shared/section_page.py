import os
from playwright.sync_api import Browser
from shared.types import PdfConfig


def generate_section_title_pdf(
    title: str,
    output_path: str,
    browser: Browser,
    pdf_config: PdfConfig,
    skip_existing: bool = True,
) -> bool:
    """Generate a single-page PDF with a centered section title."""
    if skip_existing and os.path.exists(output_path):
        return False

    page = browser.new_page()
    try:
        page.set_content(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  html, body {{
    margin: 0; padding: 0;
    height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-family: ui-sans-serif, -apple-system, system-ui, sans-serif;
    background: #fff;
  }}
  h1 {{
    font-size: 36px;
    font-weight: 600;
    color: #222;
    text-align: center;
  }}
</style>
</head><body><h1>{title}</h1></body></html>""", wait_until="load")
        page.pdf(
            path=output_path,
            format=pdf_config.paper_size,
            margin=pdf_config.margins,
            print_background=True,
        )
    finally:
        page.close()
    return True
