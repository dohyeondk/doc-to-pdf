from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TocItem:
    """A single entry in the table of contents."""
    type: str                    # "page" or "section"
    title: str
    url: Optional[str]           # None for section title pages
    section: Optional[str]       # Parent section name, or None


@dataclass
class PdfConfig:
    """Unified PDF generation configuration."""
    paper_size: str = "Letter"
    font_scale: int = 100        # Percentage; 100 = baseline readable size
    margin_top: float = 0.45     # inches
    margin_right: float = 0.25
    margin_bottom: float = 0.45
    margin_left: float = 0.25
    print_background: bool = True
    strip_blank_pages: bool = True

    @property
    def chromium_scale(self) -> float:
        """Convert font_scale percentage to Chromium's scale parameter.
        100% maps to 0.85 (the baseline used by Obsidian/Linear)."""
        return (self.font_scale / 100.0) * 0.85

    @property
    def margins(self) -> dict:
        return {
            "top": f"{self.margin_top}in",
            "right": f"{self.margin_right}in",
            "bottom": f"{self.margin_bottom}in",
            "left": f"{self.margin_left}in",
        }


@dataclass
class ProductSpec:
    """Product-specific configuration provided by each product module."""
    name: str
    custom_css: str
    prepare_js: Optional[str] = None
    content_selector: Optional[str] = None
    wait_until: str = "networkidle"
    scroll_for_lazy_images: bool = False
    pdf_metadata_title: str = ""
    pdf_metadata_author: str = ""
    has_sections: bool = False

    @property
    def output_dir(self) -> str:
        """Per-product subdirectory under output/."""
        return f"output/{self.name.lower()}"

    @property
    def merged_filename(self) -> str:
        """Final merged PDF path under output/."""
        return f"output/{self.name}.pdf"
