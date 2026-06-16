"""
Command-line interface for md2html.

Supports single-file, batch, and stdin input modes.
"""

import argparse
import sys
from pathlib import Path

try:
    from charset_normalizer import from_bytes
    _HAS_CHARSET_NORMALIZER = True
except ImportError:
    _HAS_CHARSET_NORMALIZER = False

from .converter import convert_markdown, wrap_html


def _read_text(path: Path) -> str:
    """Read a text file with automatic encoding detection.

    Strategy
    --------
    1. **UTF-8 variants** — exclusive, fast; invalid bytes always
       raise ``UnicodeDecodeError``.
    2. **``charset-normalizer``** — primary detector for non-UTF-8
       encodings.  Accurate for CJK and most legacy encodings.
    3. **Western probe** — ``charset-normalizer`` sometimes
       misidentifies short Western-European texts (e.g. iso-8859-1
       detected as cp1257).  When the detector's pick is outside
       a "common encodings" whitelist, we probe ``iso-8859-1`` and
       ``cp1252`` as a targeted safety-net.
    4. **CJK manual probe** — best-effort fallback when
       ``charset-normalizer`` is not installed.
    5. **``latin-1`` fallback** — never raises; every byte maps
       to a character.
    """
    raw = path.read_bytes()

    # 1. UTF-8 variants — exclusive, always fast.
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue

    # 2. charset-normalizer — primary non-UTF-8 detector.
    _cn_encoding = None
    _cn_decoded = None
    if _HAS_CHARSET_NORMALIZER:
        _cn_result = from_bytes(raw).best()
        if _cn_result is not None:
            _cn_encoding = _cn_result.encoding
            _cn_decoded = str(_cn_result)

    # 3. Western probe — correct common charset-normalizer
    #    misdetections for iso-8859-1 / cp1252.
    #    Only run this when charset-normalizer actually returned
    #    a result (otherwise fall through to the CJK probe below).
    _WESTERN = ("iso-8859-1", "cp1252")
    _COMMON = frozenset({
        "utf-8", "utf-8-sig", "ascii",
        "iso-8859-1", "iso-8859-2", "iso-8859-15",
        "cp1252",  # Western European — very common
        "gbk", "gb2312", "gb18030",        # Simplified Chinese
        "big5", "big5hkscs",                # Traditional Chinese
        "shift_jis", "cp932",               # Japanese
        "euc_jp",                           # Japanese (Unix)
        "euc_kr", "cp949",                  # Korean
        "utf-16", "utf-16-le", "utf-16-be",
    })
    if _cn_encoding is not None and _cn_encoding not in _COMMON:
        for enc in _WESTERN:
            try:
                return raw.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue

    # 4. If charset-normalizer returned a common encoding, use it.
    if _cn_decoded is not None:
        return _cn_decoded

    # 5. CJK manual probe — best-effort when charset-normalizer is
    #    not installed or returned nothing.
    #    Order: more exclusive codecs first.
    #    NOTE: gbk/euc_kr are both "promiscuous" (they decode each
    #    other's bytes without raising).  We prioritise gbk because
    #    the project's primary audience writes Simplified Chinese.
    for enc in ("big5", "shift_jis", "gbk", "euc_kr"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue

    # 6. Absolute last resort — latin-1 never raises.
    return raw.decode("latin-1", errors="replace")


def _resolve_output_path(out_path: Path) -> Path | None:
    """Prompt the user when an output file already exists.

    Returns the resolved ``Path`` (same, new name, or ``None`` to skip).
    """
    if not out_path.exists():
        return out_path

    prompt = (
        f"\n[!] File exists: {out_path}\n"
        "    [1] Overwrite  [2] Skip  [3] New name\n"
        "    Choose (1/2/3): "
    )

    try:
        answer = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled", file=sys.stderr)
        return None

    if answer == "1":
        return out_path
    if answer == "2":
        return None
    if answer == "3":
        stem = out_path.stem
        suffix = out_path.suffix
        parent = out_path.parent
        n = 2
        while True:
            new_path = parent / f"{stem}_v{n}{suffix}"
            if not new_path.exists():
                print(f"   => {new_path.name}", file=sys.stderr)
                return new_path
            n += 1
    return None


def main() -> int:
    """Entry point for the ``md2html`` CLI.

    Returns an exit code (0 on success, 1 on failure).
    """
    parser = argparse.ArgumentParser(
        description="md2html — enhanced Markdown to HTML converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  md2html README.md
  md2html notes.md -o notes.html --theme dark --title "Notes"
  cat input.md | md2html - -o output.html
  md2html *.md -o out/                        # batch mode
        """,
    )
    parser.add_argument(
        "input",
        nargs="+",
        help='Markdown file path(s); use "-" for stdin',
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path.  Single-file: defaults to '<input>.html'.  "
             "Batch: must be a directory.",
    )
    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Colour theme (default: light)",
    )
    parser.add_argument(
        "--title",
        help="HTML document title (default: derived from filename)",
    )
    parser.add_argument(
        "--no-mermaid",
        action="store_true",
        help="Disable Mermaid diagram support",
    )
    parser.add_argument(
        "--no-math",
        action="store_true",
        help="Disable LaTeX math (MathJax) support",
    )
    parser.add_argument(
        "--no-highlight",
        action="store_true",
        help="Disable Pygments code syntax highlighting",
    )
    parser.add_argument(
        "-w", "--max-width",
        default="none",
        metavar="WIDTH",
        help='Page content max-width, e.g. "960px", "100%%", '
             '"none" (default: none)',
    )

    args = parser.parse_args()

    # ---- stdin mode ----------------------------------------------------------
    if args.input == ["-"]:
        md_text = sys.stdin.read()
        title = args.title or "Document"
        body = convert_markdown(
            md_text,
            args.theme,
            enable_mermaid=not args.no_mermaid,
            enable_math=not args.no_math,
            enable_highlight=not args.no_highlight,
        )
        html = wrap_html(
            body,
            title,
            args.theme,
            not args.no_mermaid,
            not args.no_math,
            max_width=args.max_width,
        )
        if args.output:
            out_path = _resolve_output_path(Path(args.output))
            if out_path is None:
                return 1
            out_path.write_text(html, encoding="utf-8")
            print(f"OK -> {out_path}", file=sys.stderr)
        else:
            print(html)
        return 0

    # ---- file mode -----------------------------------------------------------
    files = args.input
    is_batch = len(files) > 1

    if is_batch:
        if not args.output:
            print("ERROR: batch mode requires -o/--output directory",
                  file=sys.stderr)
            return 1
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)

    for filepath in files:
        path = Path(filepath)
        if not path.exists():
            print(f"WARN: file not found, skipping: {filepath}",
                  file=sys.stderr)
            continue

        md_text = _read_text(path)
        title = args.title or path.stem

        body = convert_markdown(
            md_text,
            args.theme,
            enable_mermaid=not args.no_mermaid,
            enable_math=not args.no_math,
            enable_highlight=not args.no_highlight,
        )
        html = wrap_html(
            body,
            title,
            args.theme,
            not args.no_mermaid,
            not args.no_math,
            max_width=args.max_width,
        )

        if is_batch:
            out_path = Path(args.output) / f"{path.stem}.html"
        else:
            out_path = (
                Path(args.output)
                if args.output
                else path.with_suffix(".html")
            )

        resolved = _resolve_output_path(out_path)
        if resolved is None:
            print(f"SKIP: {path.name}", file=sys.stderr)
            continue
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(html, encoding="utf-8")
        print(f"OK {path.name} -> {resolved}", file=sys.stderr)

    return 0
