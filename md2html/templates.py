"""
HTML/CSS templates and CDN scripts for md2html.

This module contains the self-contained CSS themes (light/dark)
and the CDN-based JavaScript bundles for Mermaid diagrams and
MathJax rendering.
"""

# ── Light Theme ──────────────────────────────────────────────

LIGHT_CSS = r"""
/* === md2html Light Theme === */
:root {
    --bg: #ffffff;
    --fg: #24292e;
    --border: #e1e4e8;
    --code-bg: #f6f8fa;
    --blockquote-border: #0366d6;
    --blockquote-bg: #f0f7ff;
    --th-bg: #f6f8fa;
    --link: #0366d6;
    --muted: #6a737d;
    --hr: #eaecef;
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
                 "PingFang SC", "Microsoft YaHei", Helvetica, Arial, sans-serif;
    max-width: __MAX_WIDTH__;
    margin: 2rem auto;
    padding: 0 1.5rem 3rem;
    line-height: 1.75;
    color: var(--fg);
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 2em;
    margin-bottom: 0.6em;
    font-weight: 600;
    line-height: 1.3;
}
h1 { font-size: 2em; border-bottom: 2px solid var(--border); padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.25em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1.1em; }
h5, h6 { font-size: 1em; color: var(--muted); }

p { margin: 0.8em 0; }

a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Code */
code {
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "SF Mono",
                 Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.88em;
}
:not(pre) > code {
    background: var(--code-bg);
    padding: 0.15em 0.4em;
    border-radius: 4px;
    color: #d63384;
}
pre {
    background: var(--code-bg);
    padding: 1em 1.2em;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1em 0;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}
pre code { background: none; padding: 0; font-size: 0.85em; line-height: 1.6; }

/* Blockquote */
blockquote {
    border-left: 4px solid var(--blockquote-border);
    margin: 1em 0;
    padding: 0.6em 1em;
    background: var(--blockquote-bg);
    border-radius: 0 6px 6px 0;
    color: var(--muted);
}
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
}
th, td {
    border: 1px solid var(--border);
    padding: 8px 14px;
    text-align: left;
}
th {
    background: var(--th-bg);
    font-weight: 600;
}
tr:nth-child(even) td { background: rgba(0,0,0,0.02); }

/* Lists */
ul, ol { padding-left: 2em; margin: 0.6em 0; }
li { margin: 0.25em 0; }
li > p { margin: 0.2em 0; }

/* Task list */
.task-list-item { list-style: none; margin-left: -1.5em; }
.task-list-item input { margin-right: 0.4em; }

/* Images */
img { max-width: 100%; height: auto; border-radius: 6px; margin: 0.5em 0; }

/* HR */
hr {
    border: none;
    border-top: 2px solid var(--hr);
    margin: 2em 0;
}

/* Mermaid */
.mermaid {
    text-align: center;
    margin: 1.5em 0;
    padding: 1em;
    background: #fafbfc;
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* Footnotes */
.footnote { font-size: 0.88em; color: var(--muted); }
.footnote hr { margin: 0.5em 0; border-top: 1px solid var(--border); }
.footnote ol { padding-left: 1.5em; }

/* Admonitions (callouts) */
.admonition {
    border-left: 4px solid;
    padding: 0.8em 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
}
.admonition.note      { border-color: #0366d6; background: #f0f7ff; }
.admonition.warning   { border-color: #d73a49; background: #fff0f0; }
.admonition.tip       { border-color: #28a745; background: #f0fff4; }
.admonition.info      { border-color: #6f42c1; background: #f8f0ff; }
.admonition-title {
    font-weight: 600;
    margin-bottom: 0.3em;
    text-transform: uppercase;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

/* Abbreviation */
abbr { cursor: help; border-bottom: 1px dotted var(--muted); }

/* Responsive */
@media (max-width: 640px) {
    body { padding: 0 1rem 2rem; margin-top: 1rem; }
    h1 { font-size: 1.6em; }
    h2 { font-size: 1.3em; }
    pre { padding: 0.8em; }
    table { font-size: 0.85em; }
    th, td { padding: 6px 8px; }
}

/* Print */
@media print {
    body { max-width: none; margin: 0; padding: 1cm; font-size: 12pt; }
    pre, .mermaid { break-inside: avoid; }
    a { color: inherit; }
}
"""


# ── Dark Theme ──────────────────────────────────────────────

DARK_CSS = r"""
/* === md2html Dark Theme === */
:root {
    --bg: #0d1117;
    --fg: #c9d1d9;
    --border: #30363d;
    --code-bg: #161b22;
    --blockquote-border: #58a6ff;
    --blockquote-bg: #0d2847;
    --th-bg: #161b22;
    --link: #58a6ff;
    --muted: #8b949e;
    --hr: #21262d;
    --shadow: 0 1px 3px rgba(0,0,0,0.3);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
                 "PingFang SC", "Microsoft YaHei", Helvetica, Arial, sans-serif;
    max-width: __MAX_WIDTH__;
    margin: 2rem auto;
    padding: 0 1.5rem 3rem;
    line-height: 1.75;
    color: var(--fg);
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 2em;
    margin-bottom: 0.6em;
    font-weight: 600;
    line-height: 1.3;
}
h1 { font-size: 2em; border-bottom: 2px solid var(--border); padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.25em; }
h3 { font-size: 1.25em; }
h4 { font-size: 1.1em; }
h5, h6 { font-size: 1em; color: var(--muted); }

p { margin: 0.8em 0; }

a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

code {
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "SF Mono",
                 Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.88em;
}
:not(pre) > code {
    background: var(--code-bg);
    padding: 0.15em 0.4em;
    border-radius: 4px;
    color: #ff7b72;
}
pre {
    background: var(--code-bg);
    padding: 1em 1.2em;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1em 0;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}
pre code { background: none; padding: 0; font-size: 0.85em; line-height: 1.6; }

blockquote {
    border-left: 4px solid var(--blockquote-border);
    margin: 1em 0;
    padding: 0.6em 1em;
    background: var(--blockquote-bg);
    border-radius: 0 6px 6px 0;
    color: var(--muted);
}
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
}
th, td {
    border: 1px solid var(--border);
    padding: 8px 14px;
    text-align: left;
}
th { background: var(--th-bg); font-weight: 600; }
tr:nth-child(even) td { background: rgba(255,255,255,0.02); }

ul, ol { padding-left: 2em; margin: 0.6em 0; }
li { margin: 0.25em 0; }
li > p { margin: 0.2em 0; }

.task-list-item { list-style: none; margin-left: -1.5em; }
.task-list-item input { margin-right: 0.4em; }

img { max-width: 100%; height: auto; border-radius: 6px; margin: 0.5em 0; }

hr { border: none; border-top: 2px solid var(--hr); margin: 2em 0; }

.mermaid {
    text-align: center;
    margin: 1.5em 0;
    padding: 1em;
    background: #0d1117;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.footnote { font-size: 0.88em; color: var(--muted); }
.footnote hr { margin: 0.5em 0; border-top: 1px solid var(--border); }
.footnote ol { padding-left: 1.5em; }

.admonition {
    border-left: 4px solid;
    padding: 0.8em 1em;
    margin: 1em 0;
    border-radius: 0 6px 6px 0;
}
.admonition.note      { border-color: #58a6ff; background: #0d2847; }
.admonition.warning   { border-color: #f85149; background: #2d1114; }
.admonition.tip       { border-color: #3fb950; background: #0d2b15; }
.admonition.info      { border-color: #bc8cff; background: #1a1333; }
.admonition-title {
    font-weight: 600;
    margin-bottom: 0.3em;
    text-transform: uppercase;
    font-size: 0.85em;
    letter-spacing: 0.5px;
}

abbr { cursor: help; border-bottom: 1px dotted var(--muted); }

@media (max-width: 640px) {
    body { padding: 0 1rem 2rem; margin-top: 1rem; }
    h1 { font-size: 1.6em; }
    h2 { font-size: 1.3em; }
    pre { padding: 0.8em; }
    table { font-size: 0.85em; }
    th, td { padding: 6px 8px; }
}

@media print {
    body { max-width: none; margin: 0; padding: 1cm; font-size: 12pt; }
    pre, .mermaid { break-inside: avoid; }
    a { color: inherit; }
}
"""


# ── CDN scripts ──────────────────────────────────────────────

MERMAID_SCRIPT = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({
    startOnLoad: true,
    theme: 'THEME_VAR',
    securityLevel: 'loose',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
});
</script>
"""

MATHJAX_SCRIPT = """
<script>
MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
"""
