# md2html

> Enhanced Markdown to HTML converter — batteries included.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/neobuilding/md2html/actions/workflows/ci.yml/badge.svg)](https://github.com/neobuilding/md2html/actions)

**md2html** converts Markdown files into beautiful, self-contained HTML pages with zero external CSS dependencies. It supports Mermaid diagrams, Pygments syntax highlighting, LaTeX math, task lists, admonitions, and more — all out of the box.

---

## Features

| Feature                    | Description                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------- |
| 📝 **Full Markdown**       | Tables, task lists, footnotes, abbreviations, admonitions, definition lists, emoji |
| 📊 **Mermaid diagrams**    | Flowcharts, sequence diagrams, Gantt charts, pie charts (client-side via CDN)      |
| 🎨 **Syntax highlighting** | 450+ languages via Pygments with inline styles (no CSS dependency)                 |
| 📐 **LaTeX math**          | Inline and display math via MathJax 3                                              |
| 🌓 **Dual themes**         | Light (GitHub-style) and dark themes                                               |
| 📱 **Responsive**          | Adapts to desktop, tablet, and mobile; print-friendly CSS                          |
| 📦 **Self-contained**      | Single HTML file — zero external stylesheets, ready to share                       |
| 📂 **Batch mode**          | Convert multiple files at once                                                     |
| 🔒 **Safe overwrite**      | Prompts before overwriting existing files                                          |

---

## Quick Start

### Installation

```bash
pip install -r requirements.txt
# or for editable development install
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Convert a single file (outputs to <input>.html by default)
md2html README.md

# Specify output path and title
md2html notes.md -o notes.html --theme dark --title "My Notes"

# Limit page width
md2html report.md -w 860px

# Pipe from stdin
cat input.md | md2html - -o output.html

# Batch convert
md2html *.md -o out/
```

### Command-Line Options

| Option            | Description                                 | Default               |
| ----------------- | ------------------------------------------- | --------------------- |
| `input`           | Markdown file path(s); `-` for stdin        | _(required)_          |
| `-o, --output`    | Output path; directory for batch mode       | `<input>.html`        |
| `-t, --title`     | HTML document title                         | derived from filename |
| `--theme`         | `light` or `dark`                           | `light`               |
| `-w, --max-width` | Content area max width (`none`, `960px`, …) | `none`                |
| `--no-mermaid`    | Disable Mermaid support                     | enabled               |
| `--no-math`       | Disable MathJax support                     | enabled               |
| `--no-highlight`  | Disable code highlighting                   | enabled               |

### Invocation Methods

md2html supports multiple invocation styles:

| Method | Command | Notes |
|--------|---------|-------|
| **CLI entry point** | `md2html input.md` | Requires `pip install -e .`; available globally after install |
| **Package module** | `python -m md2html input.md` | No install needed; works from project root |
| **Single script** | `python md2html.py input.md` | Standalone, no package structure |
| **Windows wrapper** | `md2html.bat input.md` | Auto-activates venv; good for Windows users |

```bash
# Method 1: CLI entry point (recommended)
md2html doc.md -o doc.html --theme dark

# Method 2: run as package module
python -m md2html doc.md -o doc.html --theme dark

# Method 3: run single-file script directly
python md2html.py doc.md -o doc.html --theme dark

# Method 4: Windows bat wrapper
md2html.bat doc.md -o doc.html --theme dark
```

All methods accept the same command-line options and produce identical output.

---

## Project Structure

```
md2html/
├── md2html/                # Python package
│   ├── __init__.py
│   ├── __main__.py         # python -m md2html
│   ├── cli.py              # CLI entry point
│   ├── converter.py        # Core Markdown → HTML pipeline
│   ├── preprocess.py       # Mermaid extraction & list fixups
│   └── templates.py        # CSS themes & CDN scripts
├── tests/                  # Unit tests
│   └── test_converter.py
├── examples/               # Demo Markdown files
│   └── demo.md
├── .github/                # CI & community files
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml           # Package metadata & build config
├── requirements.txt         # Runtime dependencies
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guide
└── README.md                # This file
```

---

## Markdown Extensions

Beyond standard Markdown, md2html supports these syntax extensions:

| Syntax           | Example              | Notes                            |
| ---------------- | -------------------- | -------------------------------- |
| Task lists       | `- [x] Done`         | Checkbox rendered inline         |
| Admonitions      | `!!! note "Title"`   | `note`, `warning`, `tip`, `info` |
| Strikethrough    | `~~text~~`           | Via `pymdownx.tilde`             |
| Superscript      | `^text^`             | Via `pymdownx.caret`             |
| Highlight        | `==text==`           | Via `pymdownx.mark`              |
| Emoji            | `:smile:`            | Shortcode rendering              |
| Footnotes        | `[^1]`               | Auto-numbered footnotes          |
| Abbreviations    | `*[HTML]: …`         | Tooltip on hover                 |
| Definition lists | `term\n: definition` | `<dl>` element                   |

---

## How It Works

1. **Preprocessing** — extract Mermaid blocks into placeholders; insert missing blank lines before lists for compatible parsing.
2. **Markdown parsing** — Python-Markdown with pymdown-extensions produces HTML.
3. **Postprocessing** — restore Mermaid blocks as `<pre class="mermaid">` elements.
4. **Assembly** — wrap HTML body with embedded CSS, CDN script tags, and `<meta>` tags into a self-contained document.

Mermaid diagrams and MathJax math are rendered **client-side** by the browser — no server-side rendering needed.

---

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our development process, how to set up the environment, and how to submit pull requests.

### Development Setup

```bash
git clone https://github.com/neobuilding/md2html.git
cd md2html
pip install -e ".[dev]"
pytest
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
