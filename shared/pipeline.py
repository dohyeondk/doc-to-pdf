import logging
import os

from playwright.sync_api import Error as PlaywrightError

from shared.types import TocItem, PdfConfig, ProductSpec
from shared.browser import managed_browser
from shared.pdf_page import download_page_as_pdf
from shared.section_page import generate_section_title_pdf
from shared.pdf_merge import merge_pdfs_with_toc
from shared.pdf_utils import get_pdf_filename

log = logging.getLogger(__name__)


def run_pipeline(
    product: ProductSpec,
    toc_items: list[TocItem],
    pdf_config: PdfConfig,
) -> None:
    """Shared orchestration: download all pages, then merge with TOC."""
    output_dir = product.output_dir
    merged_output = product.merged_filename

    os.makedirs(output_dir, exist_ok=True)

    page_count = sum(1 for i in toc_items if i.type == "page")
    section_count = sum(1 for i in toc_items if i.type == "section")
    log.info("Found %d items (%d pages, %d sections)", len(toc_items), page_count, section_count)

    failures: list[tuple[str, str]] = []

    with managed_browser() as browser:
        for i, item in enumerate(toc_items, 1):
            filename = get_pdf_filename(i, item.title)
            output_path = os.path.join(output_dir, filename)
            progress = f"[{i}/{len(toc_items)}]"

            if item.type == "section":
                log.info("%s Section: %s", progress, item.title)
                try:
                    created = generate_section_title_pdf(
                        item.title, output_path, browser, pdf_config
                    )
                    log.info("    %s", "Created section page" if created else "Skipped (already exists)")
                except PlaywrightError as e:
                    log.error("    Error creating section page: %s", e)
                    failures.append((item.title, str(e)))
            else:
                log.info("%s Downloading: %s", progress, item.title)
                log.info("    URL: %s", item.url)
                log.info("    Saving to: %s", filename)

                try:
                    downloaded = download_page_as_pdf(
                        item.url, output_path, browser, pdf_config, product
                    )
                    log.info("    %s", "Success" if downloaded else "Skipped (already exists)")
                except (PlaywrightError, OSError) as e:
                    log.error("    Error: %s", e)
                    failures.append((item.title, str(e)))

    log.info("All PDFs saved to: %s/", output_dir)

    if failures:
        log.warning("%d item(s) failed:", len(failures))
        for title, err in failures:
            log.warning("  - %s: %s", title, err)

    merge_pdfs_with_toc(toc_items, output_dir, merged_output, product)
