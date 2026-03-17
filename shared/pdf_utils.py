import re

from pypdf import PdfReader, PdfWriter


def sanitize_filename(filename: str) -> str:
    """Remove filesystem-invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', "", filename)


def get_pdf_filename(index: int, title: str) -> str:
    """Generate zero-padded indexed PDF filename."""
    return f"{index:03d}. {sanitize_filename(title)}.pdf"


def strip_trailing_blank_pages(pdf_path: str) -> None:
    """Remove trailing pages that have no text, images, or XObjects."""
    reader = PdfReader(pdf_path)
    pages = reader.pages
    if len(pages) <= 1:
        return

    last_good = len(pages) - 1
    while last_good > 0:
        pg = pages[last_good]
        text = (pg.extract_text() or "").strip()
        has_images = bool(pg.images) if hasattr(pg, "images") else False
        has_xobjects = bool(pg.get("/Resources", {}).get("/XObject"))
        if text or has_images or has_xobjects:
            break
        last_good -= 1

    if last_good == len(pages) - 1:
        return  # nothing to strip

    writer = PdfWriter()
    for i in range(last_good + 1):
        writer.add_page(pages[i])
    with open(pdf_path, "wb") as f:
        writer.write(f)
