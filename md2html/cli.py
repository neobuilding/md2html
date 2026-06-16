"""
Command-line interface for md2html.

Supports single-file, batch, and stdin input modes.
"""

import argparse
import sys
from pathlib import Path

from .converter import convert_markdown, wrap_html


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

        md_text = path.read_text(encoding="utf-8")
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
