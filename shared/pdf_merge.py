import logging
import os

from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError

from shared.types import TocItem, ProductSpec
from shared.pdf_utils import get_pdf_filename

log = logging.getLogger(__name__)


def merge_pdfs_with_toc(
    toc_items: list[TocItem],
    output_dir: str,
    output_path: str,
    product: ProductSpec,
) -> str:
    """Merge individual PDFs into one file with bookmarks.

    If product.has_sections is True, nests page bookmarks under section bookmarks.
    Otherwise, all bookmarks are flat/top-level.
    """
    writer = PdfWriter()

    log.info("Merging PDFs with table of contents...")

    section_bookmark = None
    skipped = 0

    for i, item in enumerate(toc_items, 1):
        pdf_path = os.path.join(output_dir, get_pdf_filename(i, item.title))

        if not os.path.exists(pdf_path):
            log.warning("    Skipping missing file: %s", pdf_path)
            skipped += 1
            continue

        try:
            reader = PdfReader(pdf_path)
            start_page = len(writer.pages)

            for page in reader.pages:
                writer.add_page(page)

            if product.has_sections and item.type == "section":
                section_bookmark = writer.add_outline_item(
                    item.title, start_page
                )
            elif product.has_sections and item.section and section_bookmark:
                writer.add_outline_item(
                    item.title, start_page, parent=section_bookmark
                )
            else:
                writer.add_outline_item(item.title, start_page)

            log.info(
                "    [%d/%d] Added: %s (page %d)",
                i, len(toc_items), item.title, start_page + 1,
            )

        except (PdfReadError, OSError) as e:
            log.error("    Error merging %s: %s", pdf_path, e)
            skipped += 1

    total_pages = len(writer.pages)

    writer.add_metadata({
        "/Title": product.pdf_metadata_title or f"{product.name} Documentation",
        "/Author": product.pdf_metadata_author or product.name,
    })

    log.info("Created TOC with %d entries (%d skipped)", len(toc_items), skipped)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    log.info("Merged PDF saved to: %s", output_path)
    log.info("  Total pages: %d", total_pages)

    return output_path
