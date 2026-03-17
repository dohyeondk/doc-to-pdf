from shared.product_main import product_main
from products.obsidian.config import PRODUCT_SPEC
from products.obsidian.toc import get_toc_items

if __name__ == "__main__":
    product_main(PRODUCT_SPEC, get_toc_items)
