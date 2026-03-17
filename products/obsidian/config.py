from shared.types import ProductSpec

CUSTOM_CSS = """
.site-body-left-column,
.site-body-right-column,
.site-header,
.site-footer,
.graph-view-container,
.backlinks,
.mod-footer,
.outline-view-container,
.site-body-left-column-site-name,
.published-search-container,
.published-search-input-container,
.theme-toggle-input-container,
.nav-header,
.nav-folder,
.nav-file,
.site-component-navbar,
.extra-title {
    display: none !important;
}

.callout.is-collapsed {
    height: auto !important;
    overflow: visible !important;
}
.callout.is-collapsed .callout-content {
    display: block !important;
}

.site-body-center-column {
    margin: 0 auto !important;
    padding: 0 20px !important;
}
"""

PREPARE_JS = """() => {
    // Remove non-content elements
    const removeSelectors = [
        '.site-body-left-column', '.site-body-right-column',
        '.site-header', '.site-footer', '.graph-view-container',
        '.backlinks', '.mod-footer', '.outline-view-container',
        '.extra-title', '.site-component-navbar',
        '.published-search-container', '.nav-header',
    ];
    for (const sel of removeSelectors) {
        document.querySelectorAll(sel).forEach(el => el.remove());
    }

    // Unlock overflow on every wrapper so nothing is clipped.
    const containers = document.querySelectorAll(
        '.published-container, .site-body, ' +
        '.site-body-center-column, .render-container, ' +
        '.render-container-inner, .publish-renderer, ' +
        '.markdown-preview-view, .markdown-rendered, ' +
        '.markdown-preview-sizer'
    );
    for (const el of containers) {
        el.style.setProperty('overflow', 'visible', 'important');
    }
}"""

PRODUCT_SPEC = ProductSpec(
    name="Obsidian",
    output_dir="obsidian-docs-pdf",
    merged_filename="Obsidian.pdf",
    custom_css=CUSTOM_CSS,
    prepare_js=PREPARE_JS,
    content_selector=".markdown-rendered",
    wait_until="networkidle",
    scroll_for_lazy_images=False,
    pdf_metadata_title="Obsidian Help Documentation",
    pdf_metadata_author="Obsidian",
    has_sections=True,
)
