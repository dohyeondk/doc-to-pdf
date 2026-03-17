from shared.types import ProductSpec

CUSTOM_CSS = """
#sidebar, .header-bar, .toc-container, .footer-buttons, footer.footer, .pagetoc {
    display: none !important;
}

body, #body-container {
    height: inherit;
    overflow: inherit;
}

.content main {
    margin-inline-start: inherit;
    margin-inline-end: inherit;
}
"""

PRODUCT_SPEC = ProductSpec(
    name="Zed",
    output_dir="zed-docs-pdf",
    merged_filename="Zed.pdf",
    custom_css=CUSTOM_CSS,
    prepare_js=None,
    content_selector=None,
    wait_until="load",
    scroll_for_lazy_images=False,
    pdf_metadata_title="Zed Documentation",
    pdf_metadata_author="Zed Industries",
    has_sections=False,
)
