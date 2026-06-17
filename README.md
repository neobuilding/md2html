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

> - `-r requirements.txt`: standard install, runtime dependencies only. Use this for everyday use.
> - `-e ".[dev]"`: editable install + testing tools. Code changes take effect immediately — for development / contributing.

### Standalone Executable (.exe)

For users who don't have Python installed, md2html can be packaged into a single
self-contained `.exe` file using [PyInstaller](https://pyinstaller.org/).
No Python, no venv, no `pip install` — just download and run.

**Build the executable:**

```bash
pip install pyinstaller
# Use md2html.py as entry point (cli.py has relative imports that fail
# when PyInstaller runs it standalone).
# --collect-submodules pymdownx is needed because markdown loads
# pymdownx extensions dynamically via importlib (static analysis
# can't trace them).
pyinstaller --onefile --name md2html --paths . --collect-submodules pymdownx md2html.py
# Output: dist/md2html.exe  (Windows)
#         dist/md2html      (macOS / Linux)
```

**Using the `.spec` file (recommended for repeatable builds):**

The first `pyinstaller` run generates `md2html.spec` — a build config file
that captures all the options above. On subsequent builds you can skip the
long command line and just use:

```bash
pyinstaller md2html.spec
```

**One spec, all platforms.** The `.spec` file is cross-platform — `EXE()`
inside it is PyInstaller's unified executable target, not Windows-specific.
Platform-only options (e.g. `codesign_identity` on macOS) are silently
ignored on other OSes. Run the same spec on each target OS:

```bash
# On Windows       → dist/md2html.exe
# On macOS         → dist/md2html
# On Linux         → dist/md2html
pyinstaller md2html.spec
```

This is also how CI pipelines work: one workflow matrix runs
`pyinstaller md2html.spec` on `ubuntu-latest`, `macos-latest`, and
`windows-latest` in parallel.

**End-user experience:**

```bash
# Windows
md2html.exe input.md -o output.html --theme dark

# macOS / Linux
./md2html input.md -o output.html --theme dark
```

**Pre-built binaries:**

The [latest release](https://github.com/neobuilding/md2html/releases/latest)
includes ready-to-run executables for Windows, macOS, and Linux — built
automatically by GitHub Actions on every version tag.

> **Trade-offs**: The binary is ~15–20 MB (bundles a Python interpreter).
> Pre-built binaries are amd64 only; for other architectures, build from
> source with the commands above.

**Triggering a release (maintainers):**

```bash
# Push a version tag and let GitHub Actions build + publish for all platforms
git tag v0.1.0
git push origin v0.1.0
```

The workflow (`.github/workflows/release.yml`) spins up three parallel
runners, builds via `pyinstaller md2html.spec`, and attaches
`md2html-windows.exe`, `md2html-macos`, and `md2html-linux` to a new
GitHub Release.

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
