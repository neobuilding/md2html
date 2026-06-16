"""
Unit tests for the md2html package.
"""

import pytest

from md2html import __version__, convert_markdown, wrap_html
from md2html.preprocess import extract_mermaid_blocks, fix_list_spacing, restore_mermaid_blocks
from md2html.templates import DARK_CSS, LIGHT_CSS, MATHJAX_SCRIPT, MERMAID_SCRIPT


# ── Version ──────────────────────────────────────────────────

def test_version():
    assert __version__ == "1.0.0"


# ── CSS templates ─────────────────────────────────────────────

def test_light_css_contains_max_width_placeholder():
    assert "__MAX_WIDTH__" in LIGHT_CSS


def test_dark_css_contains_max_width_placeholder():
    assert "__MAX_WIDTH__" in DARK_CSS


@pytest.mark.parametrize("css", [LIGHT_CSS, DARK_CSS])
def test_css_has_core_selectors(css):
    for selector in ["body", "h1", "h2", "code", "pre", "blockquote",
                      "table", "ul, ol", ".mermaid", ".admonition",
                      "@media print"]:
        assert selector in css, f"Missing selector: {selector}"


# ── Scripts ───────────────────────────────────────────────────

def test_mermaid_script_contains_cdn():
    assert "mermaid.min.js" in MERMAID_SCRIPT


def test_mathjax_script_contains_cdn():
    assert "mathjax@3" in MATHJAX_SCRIPT


# ── List spacing fix ──────────────────────────────────────────

def test_fix_list_spacing_adds_blank_line():
    md = "**Title**\n- item 1\n- item 2"
    fixed = fix_list_spacing(md)
    lines = fixed.split("\n")
    assert lines[1] == ""  # blank line inserted before list


def test_fix_list_spacing_preserves_blank_line():
    md = "Para\n\n- item"
    fixed = fix_list_spacing(md)
    assert "Para\n\n- item" == fixed


def test_fix_list_spacing_consecutive_lists():
    md = "- one\n- two"
    fixed = fix_list_spacing(md)
    assert fixed == md  # no extra blank line between list items


def test_fix_list_spacing_task_lists():
    md = "**To do**\n- [ ] task"
    fixed = fix_list_spacing(md)
    lines = fixed.split("\n")
    assert lines[1] == ""


# ── Mermaid extraction ────────────────────────────────────────

def test_extract_mermaid_basic():
    md = "```mermaid\ngraph TD\n  A --> B\n```"
    processed, blocks = extract_mermaid_blocks(md)
    assert len(blocks) == 1
    key = next(iter(blocks))
    assert blocks[key] == "graph TD\n  A --> B"
    assert key in processed
    assert "```mermaid" not in processed


def test_extract_mermaid_multiple():
    md = "```mermaid\nA --> B\n```\nText\n```mermaid\nC --> D\n```"
    processed, blocks = extract_mermaid_blocks(md)
    assert len(blocks) == 2


def test_extract_mermaid_empty_block():
    md = "```mermaid\n\n```"
    processed, blocks = extract_mermaid_blocks(md)
    assert len(blocks) == 0  # empty blocks are left as-is


# ── Mermaid restoration ───────────────────────────────────────

def test_restore_mermaid_produces_pre_tag():
    blocks = {"MD2HTML_MERMAID_BLOCK_0": "graph TD\n  A --> B"}
    html = '<div class="highlight"><pre><span></span><code>MD2HTML_MERMAID_BLOCK_0\n</code></pre></div>'
    result = restore_mermaid_blocks(html, blocks)
    assert '<pre class="mermaid">' in result
    assert "A --&gt; B" in result


# ── Core converter ────────────────────────────────────────────

def test_convert_basic_markdown():
    md = "# Hello\n\nWorld"
    body = convert_markdown(md, enable_mermaid=False, enable_math=False)
    assert "Hello</h1>" in body  # toc extension adds id="hello"
    assert "<p>World</p>" in body


def test_convert_table():
    md = "| A | B |\n|---|---|\n| 1 | 2 |"
    body = convert_markdown(md, enable_mermaid=False, enable_math=False)
    assert "<table>" in body


def test_convert_code_block():
    md = "```python\nprint('hello')\n```"
    body = convert_markdown(md, theme="light",
                            enable_mermaid=False, enable_math=False)
    assert "print" in body


def test_convert_task_list():
    md = "- [x] Done\n- [ ] Todo"
    body = convert_markdown(md, enable_mermaid=False, enable_math=False)
    assert "task-list-item" in body
    assert "checked" in body


def test_convert_mermaid_integration():
    md = "## Flow\n\n```mermaid\ngraph TD\n  A --> B\n```"
    body = convert_markdown(md, theme="light",
                            enable_mermaid=True, enable_math=False)
    assert '<pre class="mermaid">' in body
    assert "A --&gt; B" in body


def test_convert_without_highlight():
    """Without superfences + highlight, fenced code is not parsed."""
    md = "```python\nprint('hello')\n```"
    body = convert_markdown(md, theme="light",
                            enable_mermaid=False, enable_math=False,
                            enable_highlight=False)
    # Without superfences, ``` is treated as inline code
    assert "print" in body


def test_convert_strikethrough():
    md = "~~deleted~~"
    body = convert_markdown(md, enable_mermaid=False, enable_math=False)
    assert "<del>" in body


def test_convert_blockquote():
    md = "> quote"
    body = convert_markdown(md, enable_mermaid=False, enable_math=False)
    assert "<blockquote>" in body


# ── HTML wrapper ──────────────────────────────────────────────

def test_wrap_html_doctype():
    html = wrap_html("<p>Hi</p>", "Test", "light", False, False)
    assert html.startswith("<!DOCTYPE html>")


def test_wrap_html_title():
    html = wrap_html("<p>Hi</p>", "My Title", "light", False, False)
    assert "<title>My Title</title>" in html


def test_wrap_html_max_width():
    html = wrap_html("<p>Hi</p>", "Test", "light", False, False,
                     max_width="960px")
    assert "max-width: 960px" in html
    assert "__MAX_WIDTH__" not in html


def test_wrap_html_max_width_none():
    html = wrap_html("<p>Hi</p>", "Test", "light", False, False,
                     max_width="none")
    assert "max-width: none" in html


def test_wrap_html_dark_theme():
    html = wrap_html("<p>Hi</p>", "Test", "dark", False, False)
    assert "#0d1117" in html


def test_wrap_html_with_mermaid():
    html = wrap_html("<p>Hi</p>", "Test", "light", True, False)
    assert "mermaid.min.js" in html


def test_wrap_html_with_math():
    html = wrap_html("<p>Hi</p>", "Test", "light", False, True)
    assert "mathjax@3" in html


def test_wrap_html_escapes_title():
    html = wrap_html("<p>Hi</p>", 'A & B < C', "light", False, False)
    assert "&amp;" in html
    assert "&lt;" in html
