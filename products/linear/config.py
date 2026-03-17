from shared.types import ProductSpec

CUSTOM_CSS = """
/* Hide non-content chrome */
[class*="Sidebar_"],
[class*="TableOfContents"],
[class*="breadcrumb" i],
[class*="NextPrev"],
[class*="nextPrev"],
[class*="Navigation_next"],
[class*="Navigation_prev"],
[class*="pagination" i],
a[class*="next" i][class*="article" i],
a[class*="prev" i][class*="article" i] {
    display: none !important;
}

.Layout_container__BVtmP {
    display: block !important;
}
.Layout_content__PrPCk {
    margin: 0 auto !important;
}
[class*="layout_wrapper"] {
    padding-left: 0 !important;
}
[class*="DocsArticle_content"] {
    max-width: 100% !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
}

body, html {
    overflow: visible !important;
    height: auto !important;
    color-scheme: light !important;
}

/* White background on page-level containers only */
body, html, main,
[class*="Layout_"],
[class*="DocsArticle"],
[class*="layout_"],
[class*="Prose_"],
div[class*="Flex_"] {
    background: #fff !important;
    background-color: #fff !important;
    color: #1a1a1a !important;
}

/* Force dark text on ALL elements within article */
article, article * {
    color: #1a1a1a !important;
}
article h1, article h2, article h3,
article h4, article h5, article h6 {
    color: #111 !important;
}
article a {
    color: #5e6ad2 !important;
}

/* Collapsible/accordion text */
summary, details, button,
[class*="Collapsible"] {
    color: #1a1a1a !important;
}

/* Inline code */
code:not(pre code) {
    background: #f0f0f3 !important;
    color: #1a1a1a !important;
    border: 1px solid #d4d4d8 !important;
    border-radius: 4px !important;
    padding: 1px 4px !important;
}

/* Code blocks */
pre {
    background: #f4f4f5 !important;
    color: #1a1a1a !important;
    border: 1px solid #e4e4e7 !important;
}
pre code {
    background: transparent !important;
    color: inherit !important;
    border: none !important;
    padding: 0 !important;
}

/* Keyboard shortcuts */
kbd {
    background: #f0f0f3 !important;
    color: #1a1a1a !important;
    border: 1px solid #c4c4c8 !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 0 #a0a0a4 !important;
}

/* Callout/note boxes */
[class*="Note_"] {
    background: #f8f8fa !important;
    border-color: #d4d4d8 !important;
    color: #1a1a1a !important;
}
[class*="Note_"] * {
    color: #1a1a1a !important;
}

/* Tabs */
[class*="Tabs_"] {
    background: transparent !important;
    color: #1a1a1a !important;
}
[class*="Tabs_"] button,
[class*="Tabs_"] a {
    color: #1a1a1a !important;
}

/* Images */
img {
    border: 1px solid #e4e4e7 !important;
    border-radius: 6px !important;
}

/* Table styling */
table, th, td {
    border-color: #e4e4e7 !important;
    color: #1a1a1a !important;
}
th {
    background: #f4f4f5 !important;
}
"""

PREPARE_JS = """() => {
    // Remove sidebar nav, table of contents, and "Next" links
    const removeSelectors = [
        'nav[class*="Sidebar"]',
        '[class*="Sidebar_container"]',
        '[class*="TableOfContents"]',
        '[class*="NextPrev"]',
        '[class*="nextPrev"]',
        '[class*="Navigation_next"]',
        '[class*="Navigation_prev"]',
    ];
    for (const sel of removeSelectors) {
        try {
            document.querySelectorAll(sel).forEach(el => el.remove());
        } catch(e) {}
    }

    // Remove any "Next >" / "< Previous" link blocks by content
    document.querySelectorAll('a').forEach(a => {
        const text = a.textContent.trim();
        if (/^(Next|Previous)\\s*[>›»]?$/i.test(text) || /^[<‹«]?\\s*(Next|Previous)$/i.test(text)) {
            const parent = a.closest('div, nav, footer');
            if (parent && parent.querySelectorAll('a').length <= 2) {
                parent.remove();
            } else {
                a.remove();
            }
        }
    });

    // Unlock overflow on layout wrappers
    const containers = [
        'body', 'html', 'main',
        '.Layout_container__BVtmP',
        '.Layout_content__PrPCk',
        '.layout_wrapper__37hdm',
        '.DocsArticle_root__HZXy4',
        '.DocsArticle_content__QzK2P',
    ];
    document.querySelectorAll(containers.join(', ')).forEach(el => {
        el.style.setProperty('overflow', 'visible', 'important');
        el.style.setProperty('height', 'auto', 'important');
    });
}"""

PRODUCT_SPEC = ProductSpec(
    name="Linear",
    output_dir="linear-docs-pdf",
    merged_filename="Linear.pdf",
    custom_css=CUSTOM_CSS,
    prepare_js=PREPARE_JS,
    content_selector="article",
    wait_until="networkidle",
    scroll_for_lazy_images=True,
    pdf_metadata_title="Linear Documentation",
    pdf_metadata_author="Linear",
    has_sections=True,
)
