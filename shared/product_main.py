import logging
from collections.abc import Callable

from shared.config import parse_args
from shared.pipeline import run_pipeline
from shared.types import ProductSpec, TocItem

log = logging.getLogger(__name__)


def product_main(product: ProductSpec, get_toc_items: Callable[[], list[TocItem]]) -> None:
    """Shared entry point for all product modules."""
    pdf_config = parse_args(product)
    items = get_toc_items()
    log.info("Building %s documentation...\n", product.name)
    run_pipeline(product, items, pdf_config)
