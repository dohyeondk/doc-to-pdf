from shared.config import parse_args
from shared.pipeline import run_pipeline
from products.obsidian.config import PRODUCT_SPEC
from products.obsidian.toc import get_toc_items


def main():
    pdf_config = parse_args(PRODUCT_SPEC)
    items = get_toc_items()
    print(f"Building {PRODUCT_SPEC.name} documentation...\n")
    run_pipeline(PRODUCT_SPEC, items, pdf_config)


if __name__ == "__main__":
    main()
