import argparse
from shared.types import PdfConfig, ProductSpec


def parse_args(product: ProductSpec | None = None) -> PdfConfig:
    """Parse CLI arguments into a PdfConfig.

    If a ProductSpec is provided, its defaults are used where applicable.
    CLI arguments always take precedence.
    """
    defaults = PdfConfig()

    parser = argparse.ArgumentParser(
        description=f"Generate PDF from {product.name if product else 'documentation'}"
    )
    parser.add_argument(
        "--font-scale", type=int, default=defaults.font_scale,
        help="Font scale percentage (100 = baseline readable size, default: 100)"
    )
    parser.add_argument(
        "--paper-size", default=defaults.paper_size,
        choices=["Letter", "A4", "Legal", "Tabloid"],
        help="Paper size (default: Letter)"
    )
    parser.add_argument("--margin-top", type=float, default=defaults.margin_top)
    parser.add_argument("--margin-right", type=float, default=defaults.margin_right)
    parser.add_argument("--margin-bottom", type=float, default=defaults.margin_bottom)
    parser.add_argument("--margin-left", type=float, default=defaults.margin_left)
    parser.add_argument(
        "--no-strip-blank", action="store_true",
        help="Disable trailing blank page removal"
    )
    parser.add_argument(
        "--no-background", action="store_true",
        help="Disable background printing"
    )

    args = parser.parse_args()

    return PdfConfig(
        paper_size=args.paper_size,
        font_scale=args.font_scale,
        margin_top=args.margin_top,
        margin_right=args.margin_right,
        margin_bottom=args.margin_bottom,
        margin_left=args.margin_left,
        print_background=not args.no_background,
        strip_blank_pages=not args.no_strip_blank,
    )
