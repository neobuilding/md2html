"""
Preprocessing utilities for Markdown input.

Handles edge cases that common Markdown editors (Typora, Obsidian)
tolerate but Python-Markdown does not.
"""

import re
import html as html_mod

# Sentinel prefix for Mermaid placeholder blocks
_MERMAID_PLACEHOLDER_PREFIX = "MD2HTML_MERMAID_BLOCK_"

# Pattern to detect list items (bulleted, numbered, task lists)
_LIST_START_RE = re.compile(
    r"^(\s*)([-*+]|\d+[.)])\s+(\[[ xX]\]\s*)?", re.MULTILINE
)

# Pattern for fenced Mermaid blocks
_MERMAID_FENCE_RE = re.compile(
    r"^([ \t]*)(```|~~~)mermaid\s*\n(.*?)\n\1\2",
    re.MULTILINE | re.DOTALL,
)


def extract_mermaid_blocks(md_text: str) -> tuple[str, dict[str, str]]:
    """Extract ```mermaid ... ``` blocks and replace with placeholders.

    The placeholder blocks survive the Python-Markdown pipeline intact.
    They are restored to ``<pre class="mermaid">`` elements in the
    post-processing step.

    Args:
        md_text: Raw Markdown source.

    Returns:
        A tuple of ``(processed_text, {placeholder_key: mermaid_source})``.
    """
    blocks: dict[str, str] = {}
    counter = [0]

    def replace_block(m: re.Match) -> str:
        indent = m.group(1) or ""
        content = m.group(3).strip()
        if not content:
            return m.group(0)  # empty block → leave as-is
        key = f"{_MERMAID_PLACEHOLDER_PREFIX}{counter[0]}"
        blocks[key] = content
        counter[0] += 1
        return f"{indent}```placeholder-mermaid\n{key}\n{indent}```"

    return _MERMAID_FENCE_RE.sub(replace_block, md_text), blocks


def restore_mermaid_blocks(html_text: str, blocks: dict[str, str]) -> str:
    """Replace placeholder ``<code>`` tags with Mermaid ``<pre>`` elements.

    Handles both Pygments-wrapped (``highlight > pre > code``) and plain
    ``<code>`` wrappers.

    Args:
        html_text: Converted HTML with placeholder ``<code>`` tags.
        blocks: Mapping from ``{placeholder_key: mermaid_source}``.

    Returns:
        HTML with ``<pre class="mermaid">`` blocks.
    """
    for key, content in blocks.items():
        # Case 1: Pygments highlighted output
        # <div class="highlight"><pre><span></span><code>KEY\n</code></pre></div>
        pattern1 = re.compile(
            r"<div class=\"highlight\"><pre><span></span><code>"
            + re.escape(key)
            + r"\s*</code></pre></div>",
            re.DOTALL,
        )
        replacement = (
            f'<pre class="mermaid">\n{html_mod.escape(content)}\n</pre>'
        )
        html_text, count = pattern1.subn(replacement, html_text)

        # Case 2: Plain <code> wrapping (fallback when Pygments is disabled)
        if count == 0:
            pattern2 = re.compile(
                r"<code[^>]*>\s*" + re.escape(key) + r"\s*</code>",
                re.DOTALL,
            )
            html_text = pattern2.sub(
                f'<pre class="mermaid">\n{html_mod.escape(content)}\n</pre>',
                html_text,
            )

    return html_text


def fix_list_spacing(md_text: str) -> str:
    """Insert blank lines before list items when they immediately follow
    a non-blank, non-list line.

    Python-Markdown requires a blank line before list items that follow
    paragraphs, while editors like Typora and Obsidian handle this
    gracefully.  This function normalizes the gap so that all lists are
    parsed correctly.

    Args:
        md_text: Raw Markdown source.

    Returns:
        Normalized Markdown with blank lines inserted where needed.
    """
    lines = md_text.split("\n")
    result: list[str] = []
    prev_was_blank = True  # beginning-of-file is treated as blank

    for line in lines:
        stripped = line.strip()
        is_list_item = bool(_LIST_START_RE.match(line))

        if is_list_item and not prev_was_blank:
            prev_line = result[-1] if result else ""
            prev_stripped = prev_line.strip() if prev_line else ""

            # Do NOT insert blank line when:
            #   - Previous line is already a list item (continuation)
            #   - Previous line looks like a fenced code block delimiter
            prev_is_list_continuation = bool(_LIST_START_RE.match(prev_line))
            prev_is_code_block = prev_stripped.startswith("```") or (
                len(prev_line) - len(prev_line.lstrip()) >= 4
                and not prev_stripped.startswith(
                    ("#", ">", "-", "*", "|", "<")
                )
            )

            if not prev_is_list_continuation and not prev_is_code_block:
                result.append("")

        result.append(line)
        prev_was_blank = stripped == ""

    return "\n".join(result)
