from products.zed.config import PRODUCT_SPEC
from products.zed.toc import get_toc_items
from shared.product_main import product_main

if __name__ == "__main__":
    product_main(PRODUCT_SPEC, get_toc_items)
