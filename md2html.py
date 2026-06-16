#!/usr/bin/env python3
"""
md2html — Enhanced Markdown to HTML converter.

Usage:
  python md2html.py input.md
  python md2html.py input.md -o output.html --theme dark
  python -m md2html input.md
"""

from md2html.cli import main

if __name__ == "__main__":
    import sys
    sys.exit(main())
