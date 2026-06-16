"""
md2html — Enhanced Markdown to HTML converter.

Convert Markdown files to beautiful, self-contained HTML pages
with Mermaid diagram support, code syntax highlighting, and
LaTeX math rendering.
"""

from .converter import convert_markdown, wrap_html

__version__ = "1.0.0"
__all__ = ["convert_markdown", "wrap_html"]
