import os
from shared.types import TocItem, PdfConfig, ProductSpec
from shared.browser import managed_browser
from shared.pdf_page import download_page_as_pdf
from shared.section_page import generate_section_title_pdf
from shared.pdf_merge import merge_pdfs_with_toc
from shared.pdf_utils import get_pdf_filename


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
    print(f"Found {len(toc_items)} items ({page_count} pages, {section_count} sections)\n")

    with managed_browser() as browser:
        for i, item in enumerate(toc_items, 1):
            filename = get_pdf_filename(i, item.title)
            output_path = os.path.join(output_dir, filename)

            if item.type == "section":
                print(f"[{i}/{len(toc_items)}] Section: {item.title}")
                try:
                    created = generate_section_title_pdf(
                        item.title, output_path, browser, pdf_config
                    )
                    if created:
                        print("    Created section page\n")
                    else:
                        print("    Skipped (already exists)\n")
                except Exception as e:
                    print(f"    Error: {e}\n")
            else:
                print(f"[{i}/{len(toc_items)}] Downloading: {item.title}")
                print(f"    URL: {item.url}")
                print(f"    Saving to: {filename}")

                try:
                    downloaded = download_page_as_pdf(
                        item.url, output_path, browser, pdf_config, product
                    )
                    if downloaded:
                        print("    Success\n")
                    else:
                        print("    Skipped (already exists)\n")
                except Exception as e:
                    print(f"    Error: {e}\n")

    print(f"\nAll PDFs saved to: {output_dir}/")

    merge_pdfs_with_toc(toc_items, output_dir, merged_output, product)
