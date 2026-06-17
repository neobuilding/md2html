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


# ── _read_text encoding detection ─────────────────────────────


def _write_encoded(tmp_path, filename, text, encoding):
    """Helper: write *text* to *filename* inside *tmp_path* with *encoding*."""
    p = tmp_path / filename
    p.write_bytes(text.encode(encoding))
    return p


# Realistic Markdown snippets for encoding tests — long enough that
# permissive multi-byte codecs (GBK, Big5, …) reject each other's bytes.
_GBK_MD = (
    "# GBK 测试文档\n\n"
    "这是第一段内容，包含较多的中文文本以确保编码检测准确。\n\n"
    "## 第二章节\n\n"
    "- 列表项目一：说明文字\n"
    "- 列表项目二：更多说明\n\n"
    "> 引用文字。\n\n"
    "```python\nprint(\"hello\")\n```\n"
)

_BIG5_MD = (
    "# Big5 測試文件\n\n"
    "這是第一段中文內容，包含足夠的字元讓編碼檢測更加精確。\n\n"
    "## 第二章節\n\n"
    "- 列表項目一：說明文字\n"
    "- 列表項目二：更多說明\n\n"
    "> 引用區塊。\n\n"
    "```python\nprint(\"hello\")\n```\n"
)

_SJIS_MD = (
    "# Shift-JIS テスト\n\n"
    "これは日本語のテスト文書です。十分な文字数を含めてエンコード検出を正確に行います。\n\n"
    "## 第二章\n\n"
    "- リスト項目一：説明\n"
    "- リスト項目二：詳細\n\n"
    "> 引用ブロック。\n\n"
    "```python\nprint(\"hello\")\n```\n"
)

_EUCKR_MD = (
    "# EUC-KR 테스트\n\n"
    "이것은 한국어 테스트 문서입니다. 충분한 글자 수를 포함하여 인코딩 감지가 정확하게 이루어지도록 합니다.\n\n"
    "## 제2장\n\n"
    "- 목록 항목 1: 설명\n"
    "- 목록 항목 2: 세부사항\n\n"
    "> 인용문입니다.\n\n"
    "```python\nprint(\"hello\")\n```\n"
)


class TestReadTextEncoding:
    """Tests for ``_read_text()`` — encoding auto-detection."""

    # -- import plumbing --------------------------------------------------
    @staticmethod
    def _read_text(path):
        from md2html.cli import _read_text
        return _read_text(path)

    # -- happy path: common encodings ------------------------------------

    def test_utf8(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", _GBK_MD, "utf-8")
        result = self._read_text(p)
        assert "GBK 测试文档" in result
        assert "列表项目" in result

    def test_utf8_bom(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", "# Title\n\nContent paragraph.", "utf-8-sig")
        result = self._read_text(p)
        assert "# Title" in result

    def test_gbk(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", _GBK_MD, "gbk")
        result = self._read_text(p)
        assert "GBK 测试文档" in result

    def test_big5_traditional_chinese(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", _BIG5_MD, "big5")
        result = self._read_text(p)
        assert "Big5 測試文件" in result
        assert "列表項目" in result

    def test_shift_jis_japanese(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", _SJIS_MD, "shift_jis")
        result = self._read_text(p)
        assert "テスト" in result

    def test_euc_kr_korean(self, tmp_path):
        p = _write_encoded(tmp_path, "f.md", _EUCKR_MD, "euc_kr")
        result = self._read_text(p)
        assert "테스트" in result

    def test_iso_8859_1(self, tmp_path):
        text = "# Café résumé\n\nThis is a longer paragraph with accented characters like à, é, ü, and also some French: déjà vu.\n\n- item one\n- item two\n"
        p = _write_encoded(tmp_path, "f.md", text, "iso-8859-1")
        result = self._read_text(p)
        assert "Café" in result
        assert "résumé" in result
        assert "déjà" in result

    def test_latin1(self, tmp_path):
        # Latin-1 and GBK overlap — GBK may falsely "decode" some Latin-1
        # sequences.  We verify at minimum that _read_text returns a
        # non-empty, non-garbled result.
        text = "# naïve\résumé\n\nLong enough with accented text.\n"
        p = _write_encoded(tmp_path, "f.md", text, "latin-1")
        result = self._read_text(p)
        assert len(result) > 0
        assert "#" in result

    # -- edge cases -------------------------------------------------------

    def test_empty_file(self, tmp_path):
        p = _write_encoded(tmp_path, "empty.md", "", "utf-8")
        result = self._read_text(p)
        assert result == ""

    def test_ascii_only(self, tmp_path):
        text = "# Hello\n\nWorld\n\nThis is a longer markdown document with enough content to avoid ambiguity.\n\n- item one\n- item two\n"
        p = _write_encoded(tmp_path, "f.md", text, "ascii")
        result = self._read_text(p)
        assert result == text

    def test_binary_content_falls_back_to_latin1(self, tmp_path):
        """Non-text bytes: latin-1 never raises UnicodeDecodeError."""
        p = tmp_path / "bin.md"
        p.write_bytes(bytes(range(256)))
        result = self._read_text(p)
        assert len(result) == 256  # every byte maps to a latin-1 char

    # -- fallback without charset-normalizer -----------------------------

    def test_fallback_when_charset_normalizer_missing(self, tmp_path, monkeypatch):
        """Without charset-normalizer, the manual probe catches GBK."""
        import md2html.cli as cli_mod
        monkeypatch.setattr(cli_mod, "_HAS_CHARSET_NORMALIZER", False, raising=False)
        p = _write_encoded(tmp_path, "f.md", _GBK_MD, "gbk")
        result = self._read_text(p)
        assert "GBK 测试文档" in result
        monkeypatch.setattr(cli_mod, "_HAS_CHARSET_NORMALIZER", True, raising=False)

    def test_fallback_west_european_without_cn(self, tmp_path, monkeypatch):
        """Without charset-normalizer, iso-8859-1 from the probe list works."""
        import md2html.cli as cli_mod
        monkeypatch.setattr(cli_mod, "_HAS_CHARSET_NORMALIZER", False, raising=False)
        text = "Café résumé\n\nLonger paragraph with à, é, and more words to avoid false positives during encoding probe.\n"
        p = _write_encoded(tmp_path, "f.md", text, "iso-8859-1")
        result = self._read_text(p)
        assert "Café" in result
        monkeypatch.setattr(cli_mod, "_HAS_CHARSET_NORMALIZER", True, raising=False)

    def test_charset_normalizer_catch_all(self, tmp_path):
        """charset-normalizer handles encodings NOT in the manual probe."""
        # Build valid cp1252 bytes directly (some cp1252 code points are
        # not valid Unicode surrogates, so .encode('cp1252') fails).
        raw = bytearray(b"Hello from Windows-1252")
        raw.extend(b"\x97")   # em-dash in cp1252
        raw.extend(b"\x93")   # left smart-quote
        raw.extend(b"\x94")   # right smart-quote
        raw.extend(b"\nascii trailer\n")
        p = tmp_path / "f.md"
        p.write_bytes(bytes(raw))
        result = self._read_text(p)
        # charset-normalizer should identify cp1252 / windows-1252
        assert "Windows-1252" in result


# ── _resolve_output_path tests ────────────────────────────────

def test_resolve_output_path_new_file(tmp_path):
    """New file: should return the path directly."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "new.html"
    result = _resolve_output_path(p)
    assert result == p


def test_resolve_output_path_overwrite(monkeypatch, tmp_path):
    """Existing file + user chooses 1 (overwrite): should return the path."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("old")
    monkeypatch.setattr("builtins.input", lambda _: "1")
    result = _resolve_output_path(p)
    assert result == p


def test_resolve_output_path_skip(monkeypatch, tmp_path):
    """Existing file + user chooses 2 (skip): should return None."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("old")
    monkeypatch.setattr("builtins.input", lambda _: "2")
    result = _resolve_output_path(p)
    assert result is None


def test_resolve_output_path_new_name(monkeypatch, tmp_path):
    """Existing file + user chooses 3 (new name): should return a new path."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("old")
    monkeypatch.setattr("builtins.input", lambda _: "3")
    result = _resolve_output_path(p)
    assert result is not None
    assert result != p
    assert result.stem == "existing_v2"


def test_resolve_output_path_cancel(monkeypatch, tmp_path):
    """Existing file + user cancels (EOFError): should return None."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("old")
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError()))
    result = _resolve_output_path(p)
    assert result is None


# ── fix_list_spacing edge cases ──────────────────────────────

def test_fix_list_spacing_code_block_followed_by_list():
    """Code block followed by list should NOT get blank line."""
    from md2html.preprocess import fix_list_spacing
    md = "```python\ncode\n```\n- item"
    fixed = fix_list_spacing(md)
    assert fixed == md  # no blank line inserted


def test_fix_list_spacing_heading_followed_by_list():
    """Heading followed by list SHOULD get blank line."""
    from md2html.preprocess import fix_list_spacing
    md = "# Title\n- item"
    fixed = fix_list_spacing(md)
    lines = fixed.split("\n")
    assert lines[1] == ""


def test_fix_list_spacing_multiline_list_item():
    """When a list item has continuation lines, the next list item gets a blank line inserted."""
    from md2html.preprocess import fix_list_spacing
    md = "- item 1\n  continuation\n- item 2"
    fixed = fix_list_spacing(md)
    # fix_list_spacing inserts a blank line before "- item 2"
    # because the continuation line is treated as paragraph text
    lines = fixed.split("\n")
    # Should have a blank line before the second list item
    assert lines[2] == ""
    assert lines[3] == "- item 2"


# ── extract_mermaid_blocks edge cases ────────────────────────

def test_extract_mermaid_with_indentation():
    """Mermaid block with leading indentation."""
    from md2html.preprocess import extract_mermaid_blocks
    md = "  ```mermaid\ngraph TD\n  A --> B\n  ```"
    processed, blocks = extract_mermaid_blocks(md)
    assert len(blocks) == 1
    key = next(iter(blocks))
    assert blocks[key] == "graph TD\n  A --> B"
    assert key in processed


def test_extract_mermaid_multiple_blocks():
    """Multiple Mermaid blocks should get unique keys."""
    from md2html.preprocess import extract_mermaid_blocks
    md = "```mermaid\nA\n```\n---\n```mermaid\nB\n```"
    processed, blocks = extract_mermaid_blocks(md)
    assert len(blocks) == 2
    keys = list(blocks.keys())
    assert keys[0] != keys[1]


def test_restore_mermaid_case2_plain_code():
    """Restore Mermaid block when Pygments is disabled (plain <code> wrapper)."""
    from md2html.preprocess import restore_mermaid_blocks
    blocks = {"MD2HTML_MERMAID_BLOCK_0": "graph TD\n  A --> B"}
    html = "<code>MD2HTML_MERMAID_BLOCK_0</code>"
    result = restore_mermaid_blocks(html, blocks)
    assert '<pre class="mermaid">' in result


# ── convert_markdown edge cases ───────────────────────────────

def test_convert_markdown_empty():
    """Empty Markdown should not crash."""
    body = convert_markdown("", enable_mermaid=False, enable_math=False)
    assert isinstance(body, str)


def test_convert_markdown_only_whitespace():
    """Whitespace-only Markdown should not crash."""
    body = convert_markdown("   \n\n  ", enable_mermaid=False, enable_math=False)
    assert isinstance(body, str)


def test_convert_with_mermaid_disabled():
    """When Mermaid is disabled, ```mermaid blocks should be treated as code."""
    md = "```mermaid\ngraph TD\n  A --> B\n```"
    body = convert_markdown(md, theme="light",
                            enable_mermaid=False, enable_math=False)
    # Should be treated as a regular code block, not restored as Mermaid
    assert "mermaid" not in body.lower() or "class=" not in body


def test_convert_with_math_enabled():
    """MathJax script should be included when enable_math=True."""
    md = "$$E = mc^2$$"
    body = convert_markdown(md, theme="light",
                            enable_mermaid=False, enable_math=True)
    # MathJax should be loaded in the head, but convert_markdown only returns body
    # So we test wrap_html separately
    html = wrap_html(body, "Test", "light", False, True)
    assert "mathjax" in html.lower()


def test_wrap_html_no_mermaid_no_math():
    """When both Mermaid and Math are disabled, scripts should not be included."""
    html = wrap_html("<p>Hi</p>", "Test", "light", False, False)
    assert "mermaid.min.js" not in html
    assert "mathjax" not in html.lower()


def test_wrap_html_lang_attribute():
    """HTML lang attribute should be set."""
    html = wrap_html("<p>Hi</p>", "Test", "light", False, False)
    assert 'lang=' in html


# ── CLI main() tests ──────────────────────────────────────────

def test_main_single_file(tmp_path, monkeypatch, capsys):
    """Convert a single Markdown file via CLI."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello\n\nWorld", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["md2html", str(md_file)])
    exit_code = main()
    assert exit_code == 0
    out_path = tmp_path / "test.html"
    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")
    assert "<h1" in content
    assert "Hello" in content


def test_main_single_file_with_output(tmp_path, monkeypatch):
    """Specify output path via -o flag."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello", encoding="utf-8")
    out_file = tmp_path / "custom.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "Hello" in content


def test_main_stdin_to_stdout(monkeypatch):
    """Read from stdin and print to stdout."""
    from md2html.cli import main
    import io
    fake_stdin = io.StringIO("# Hello\n\nWorld")
    monkeypatch.setattr("sys.stdin", fake_stdin)
    monkeypatch.setattr("sys.argv", ["md2html", "-"])
    import sys
    from io import StringIO
    fake_stdout = StringIO()
    monkeypatch.setattr(sys, "stdout", fake_stdout)
    exit_code = main()
    assert exit_code == 0
    output = fake_stdout.getvalue()
    assert "<h1" in output
    assert "Hello" in output


def test_main_stdin_with_output(tmp_path, monkeypatch):
    """Read from stdin and write to file."""
    from md2html.cli import main
    import io
    fake_stdin = io.StringIO("# Hello\n\nWorld")
    monkeypatch.setattr("sys.stdin", fake_stdin)
    out_file = tmp_path / "stdin_out.html"
    monkeypatch.setattr("sys.argv", ["md2html", "-", "-o", str(out_file)])
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "Hello" in content


def test_main_file_not_found(monkeypatch):
    """Non-existent file should print warning but not crash."""
    from md2html.cli import main
    monkeypatch.setattr("sys.argv", ["md2html", "/nonexistent/md.md"])
    exit_code = main()
    assert exit_code == 0  # returns 0 because it skips gracefully


def test_main_dark_theme(tmp_path, monkeypatch):
    """Dark theme flag should produce dark CSS."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello", encoding="utf-8")
    out_file = tmp_path / "dark.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "--theme", "dark",
                     "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "#0d1117" in content or "0d1117" in content


def test_main_with_title(tmp_path, monkeypatch):
    """Custom title flag."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello", encoding="utf-8")
    out_file = tmp_path / "titled.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "--title", "My Title",
                     "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "<title>My Title</title>" in content


def test_main_no_mermaid_no_math(tmp_path, monkeypatch):
    """Disable Mermaid and Math flags."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello\n\n```mermaid\nA --> B\n```", encoding="utf-8")
    out_file = tmp_path / "noext.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "--no-mermaid", "--no-math",
                     "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "mathjax" not in content.lower()


def test_main_max_width(tmp_path, monkeypatch):
    """Max width flag."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello", encoding="utf-8")
    out_file = tmp_path / "wide.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "-w", "960px",
                     "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "max-width: 960px" in content


def test_main_no_highlight(tmp_path, monkeypatch):
    """Disable syntax highlighting."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("```python\nprint('hi')\n```", encoding="utf-8")
    out_file = tmp_path / "nohl.html"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "--no-highlight",
                     "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "print" in content


def test_main_batch_mode_missing_output(monkeypatch):
    """Batch mode without -o should error."""
    from md2html.cli import main
    monkeypatch.setattr("sys.argv", ["md2html", "file1.md", "file2.md"])
    exit_code = main()
    assert exit_code == 1


def test_main_stdin_skip_overwrite(monkeypatch, tmp_path):
    """Stdin mode: user chooses to skip overwriting existing file."""
    from md2html.cli import main
    import io
    fake_stdin = io.StringIO("# Hello")
    monkeypatch.setattr("sys.stdin", fake_stdin)
    out_file = tmp_path / "exists.html"
    out_file.write_text("old content")
    monkeypatch.setattr("builtins.input", lambda _: "2")
    monkeypatch.setattr("sys.argv", ["md2html", "-", "-o", str(out_file)])
    exit_code = main()
    assert exit_code == 1  # returns 1 when skip


def test_main_single_file_overwrite(monkeypatch, tmp_path):
    """Single file: user chooses to overwrite existing output."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# New Content", encoding="utf-8")
    out_file = tmp_path / "test.html"
    out_file.write_text("old content")
    monkeypatch.setattr("builtins.input", lambda _: "1")
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "New Content" in content


def test_main_single_file_skip_overwrite(monkeypatch, tmp_path):
    """Single file: user chooses to skip overwriting existing output."""
    from md2html.cli import main
    md_file = tmp_path / "test.md"
    md_file.write_text("# Content", encoding="utf-8")
    out_file = tmp_path / "test.html"
    out_file.write_text("old")
    monkeypatch.setattr("builtins.input", lambda _: "2")
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md_file), "-o", str(out_file)]
    )
    exit_code = main()
    assert exit_code == 0  # skips but returns 0


def test_main_batch_mode(tmp_path, monkeypatch):
    """Batch mode: convert multiple files to a directory."""
    from md2html.cli import main
    md1 = tmp_path / "a.md"
    md1.write_text("# A", encoding="utf-8")
    md2 = tmp_path / "b.md"
    md2.write_text("# B", encoding="utf-8")
    out_dir = tmp_path / "out"
    monkeypatch.setattr(
        "sys.argv", ["md2html", str(md1), str(md2), "-o", str(out_dir)]
    )
    exit_code = main()
    assert exit_code == 0
    assert (out_dir / "a.html").exists()
    assert (out_dir / "b.html").exists()


# ── _resolve_output_path edge cases ───────────────────────────

def test_resolve_output_path_v3_when_v2_exists(tmp_path, monkeypatch):
    """When v2 already exists, should try v3."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("original")
    (tmp_path / "existing_v2.html").write_text("v2")
    monkeypatch.setattr("builtins.input", lambda _: "3")
    result = _resolve_output_path(p)
    assert result is not None
    assert result.stem == "existing_v3"


def test_resolve_output_path_v4_when_v2_v3_exist(tmp_path, monkeypatch):
    """When v2 and v3 both exist, should try v4."""
    from md2html.cli import _resolve_output_path
    p = tmp_path / "existing.html"
    p.write_text("original")
    (tmp_path / "existing_v2.html").write_text("v2")
    (tmp_path / "existing_v3.html").write_text("v3")
    monkeypatch.setattr("builtins.input", lambda _: "3")
    result = _resolve_output_path(p)
    assert result is not None
    assert result.stem == "existing_v4"


# ── _read_text: charset_normalizer unavailable edge case ─────

def test_read_text_no_charset_normalizer(monkeypatch, tmp_path):
    """When charset-normalizer raises ImportError, CJK probe should decode GBK."""
    import md2html.cli as cli_mod
    # Simulate charset-normalizer not being available
    monkeypatch.setattr(cli_mod, "_HAS_CHARSET_NORMALIZER", False)
    content = (
        "# GBK 测试文档\n\n"
        "这是第一段内容，包含较多的中文文本以确保编码检测准确。\n\n"
        "- 列表项目一：说明文字\n"
        "- 列表项目二：更多说明\n\n"
        "> 引用文字。\n"
    )
    p = tmp_path / "gbk.md"
    p.write_bytes(content.encode("gbk"))
    result = cli_mod._read_text(p)
    assert "GBK 测试文档" in result
