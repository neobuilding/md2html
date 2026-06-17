# Contributing to md2html

Thank you for your interest in contributing! This document outlines the
process for reporting issues, proposing features, and submitting code
changes.

---

## Code of Conduct

Be respectful, constructive, and inclusive. Harassment of any kind will
not be tolerated.

---

## How to Contribute

### Reporting Bugs

1. **Search existing issues** to avoid duplicates.
2. Use the **Bug Report** issue template.
3. Include:
    - Your OS and Python version (`python --version`).
    - The exact command that triggered the problem.
    - A minimal Markdown snippet that reproduces the issue.
    - Expected vs actual behaviour.

### Proposing Features

1. Open a **Feature Request** issue.
2. Describe the use case — what problem does this solve?
3. If possible, suggest an approach or API design.

### Pull Requests

1. **Fork** the repository and create a feature branch.
2. Follow the existing code style (PEP 8, type hints where useful).
3. **Add tests** for new functionality.
4. Run the test suite:

    ```bash
    pip install -e ".[dev]"
    pytest
    ```

5. Ensure all tests pass before submitting.
6. Write clear commit messages (imperative mood, 50/72 rule).
7. Open a PR against `main` using the PR template.

### Commit Message Format

md2html follows [Conventional Commits](https://www.conventionalcommits.org/).
The commit type determines the next version number in auto-releases.

```
<type>(<scope>): <short summary>
```

**Types that trigger a release:**

| Type                         | Version bump  | Example                         |
| ---------------------------- | ------------- | ------------------------------- |
| `feat`                       | minor (0.x.0) | `feat(parser): add GBK support` |
| `fix`                        | patch (0.0.x) | `fix(cli): handle empty input`  |
| `feat!:` / `BREAKING CHANGE` | major (x.0.0) | `feat!: drop Python 3.9`        |

**Types that do NOT trigger a release:**
`docs`, `test`, `chore`, `refactor`, `style`.

Other notes:

- Use imperative mood (`add` not `added` / `adds`).
- Keep the summary under 50 characters.
- Add a body paragraph for non-obvious changes.

---

## Development Setup

```bash
# Clone
git clone https://github.com/neobuilding/md2html.git
cd md2html

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install runtime dependencies only
pip install -r requirements.txt

# Or install in editable mode with dev dependencies (for contributing)
pip install -e ".[dev]"

# Run tests
pytest

# Run the CLI
md2html examples/demo.md
```

> **`-r requirements.txt` vs `-e ".[dev]"`**:
>
> - `-r requirements.txt` — standard install, runtime dependencies only, for **everyday use**.
> - `-e ".[dev]"` — editable install, code changes take effect immediately
>   (no reinstall needed), plus testing tools (`pytest`, `pytest-cov`), for
>   **development / contributing**.

---

## Project Architecture

````
Markdown input
      │
      ▼
preprocess.fix_list_spacing()       ← normalise list spacing
      │
      ▼
preprocess.extract_mermaid_blocks() ← extract ```mermaid``` blocks
      │
      ▼
converter.convert_markdown()        ← Python-Markdown + extensions
      │
      ▼
preprocess.restore_mermaid_blocks() ← restore <pre class="mermaid">
      │
      ▼
converter.wrap_html()               ← embed CSS, scripts, <meta>
      │
      ▼
Self-contained HTML output
````

---

## Testing

Tests use `pytest`. To add a test:

1. Create a file in `tests/` named `test_<module>.py`.
2. Use the `md2html` package API directly:

    ```python
    from md2html import convert_markdown, wrap_html
    from md2html.preprocess import fix_list_spacing
    ```

3. For parameterised tests, use `@pytest.mark.parametrize`.

Run with coverage:

```bash
pytest --cov=md2html --cov-report=term
```

---

## Style Guide

- **Python**: [PEP 8](https://peps.python.org/pep-0008/), 88-character line limit.
- **Docstrings**: [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- **Imports**: standard library → third-party → project-local.
- **Type hints**: encouraged for public API signatures.

---

## Release Process

md2html supports two release methods. Both produce the same result — a GitHub Release with pre-built binaries for Windows, macOS, and Linux.

**Method 1 — Auto Release (recommended):**

1. Go to the repository **Actions** tab → select **CI**.
2. Click **Run workflow**.
3. Leave `version` empty to auto-detect from commits, or type a specific version (e.g. `v0.2.0`).
4. Click **Run workflow**.

The workflow reads commits since the last tag and calculates the next version automatically using Conventional Commits rules. It then builds for all 3 platforms and creates a GitHub Release — all in one pipeline.

**Method 2 — Manual tag (for precise control):**

```bash
# 1. Update version in pyproject.toml (if publishing to PyPI)
# 2. Tag the release
git tag v0.2.0

# 3. Push the tag — ci.yml handles the rest
git push origin v0.2.0
```

> **Note:** `CHANGELOG.md` is auto-generated by the GitHub Release (`generate_release_notes: true`), so manual maintenance is not required.

---

## Questions?

Open a discussion or issue — we are happy to help.
