import logging
import os

from playwright.sync_api import Browser
from playwright.sync_api import TimeoutError as PlaywrightTimeout

from shared.pdf_utils import strip_trailing_blank_pages
from shared.types import PdfConfig, ProductSpec

log = logging.getLogger(__name__)


def download_page_as_pdf(
    url: str,
    output_path: str,
    browser: Browser,
    pdf_config: PdfConfig,
    product: ProductSpec,
    skip_existing: bool = True,
) -> bool:
    """Navigate to a URL, inject product CSS/JS, and generate a PDF."""
    if skip_existing and os.path.exists(output_path):
        return False

    page = browser.new_page()

    try:
        page.goto(url, wait_until=product.wait_until)

        # Wait for content selector if specified
        if product.content_selector:
            try:
                page.wait_for_selector(product.content_selector, timeout=product.selector_timeout_ms)
            except PlaywrightTimeout:
                log.debug("Content selector %r not found, proceeding anyway", product.content_selector)
        page.wait_for_timeout(product.settle_delay_ms)

        # Scroll through page to trigger lazy-loaded images
        if product.scroll_for_lazy_images:
            page.evaluate("""() => {
                return new Promise(resolve => {
                    const distance = 400;
                    const delay = 100;
                    let scrolled = 0;
                    const maxScroll = document.body.scrollHeight;
                    const timer = setInterval(() => {
                        window.scrollBy(0, distance);
                        scrolled += distance;
                        if (scrolled >= maxScroll) {
                            clearInterval(timer);
                            window.scrollTo(0, 0);
                            resolve();
                        }
                    }, delay);
                });
            }""")
            page.wait_for_timeout(product.settle_delay_ms)

        # Inject CSS overrides
        page.add_style_tag(content=product.custom_css)

        # Run prepare-for-print JS if specified
        if product.prepare_js:
            page.evaluate(product.prepare_js)
            page.wait_for_timeout(500)

        # Generate PDF
        page.pdf(
            path=output_path,
            format=pdf_config.paper_size,
            margin=pdf_config.margins,
            print_background=pdf_config.print_background,
            scale=pdf_config.chromium_scale,
        )
    finally:
        page.close()

    # Strip trailing blank pages if enabled
    if pdf_config.strip_blank_pages:
        strip_trailing_blank_pages(output_path)

    return True
