import argparse
import logging

from shared.types import PdfConfig, ProductSpec

log = logging.getLogger(__name__)


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
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Configure logging based on verbosity
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    # Validate arguments
    if not 10 <= args.font_scale <= 300:
        parser.error("--font-scale must be between 10 and 300")

    margins = [args.margin_top, args.margin_right, args.margin_bottom, args.margin_left]
    if any(m < 0 for m in margins):
        parser.error("Margins cannot be negative")

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
