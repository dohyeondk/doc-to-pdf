import os
from pypdf import PdfWriter, PdfReader
from shared.types import TocItem, ProductSpec
from shared.pdf_utils import get_pdf_filename


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

    print("\nMerging PDFs with table of contents...")

    section_bookmark = None

    for i, item in enumerate(toc_items, 1):
        pdf_path = os.path.join(output_dir, get_pdf_filename(i, item.title))

        if not os.path.exists(pdf_path):
            print(f"    Warning: Skipping missing file: {pdf_path}")
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

            print(
                f"    [{i}/{len(toc_items)}] Added: {item.title} (page {start_page + 1})"
            )

        except Exception as e:
            print(f"    Error merging {pdf_path}: {e}")

    total_pages = len(writer.pages)

    writer.add_metadata({
        "/Title": product.pdf_metadata_title or f"{product.name} Documentation",
        "/Author": product.pdf_metadata_author or product.name,
    })

    print(f"\nCreated TOC with {len(toc_items)} entries")

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"Merged PDF saved to: {output_path}")
    print(f"  Total pages: {total_pages}")

    return output_path
