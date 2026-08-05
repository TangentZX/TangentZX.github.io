# Taxonomy Connected Tree Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render the chapter homepages and category archive as a clearly nested connected-line tree with aligned, accessible article rows in both color schemes and at desktop/mobile widths.

**Architecture:** Keep `hooks/taxonomy.py` as the single taxonomy data source and preserve its heading/list/link ordering. Add only semantic `<time>` and separator spans to each generated Markdown list item so `docs/resources/css/taxonomy.css` can lay out fixed date and flexible title columns; all tree rails, connectors, indentation, theme colors, hover/focus states, and responsive behavior remain CSS-only and scoped below `.taxonomy-categories`.

**Tech Stack:** Python 3.13, MkDocs 1.6.1, Material for MkDocs 9.6.20, Markdown `attr_list`/`md_in_html`, CSS custom properties and `color-mix()`, Python `unittest`.

## Global Constraints

- Apply the new tree only to `docs/study/index.md`, `docs/ctf/index.md`, `docs/sth/index.md`, and `docs/archive/categories.md` through their existing `.taxonomy-categories` wrapper.
- Preserve article front matter, category paths, URLs, links, and newest-to-oldest ordering.
- Preserve the current Markdown heading hierarchy and unordered article-list structure.
- Use `#6171F5` in the light theme and `#7DAFE9` in the dark theme.
- Do not introduce JavaScript, collapsible interactions, block-card category styling, or changes to the tag cloud.
- At narrow widths, retain complete dates, allow titles to wrap naturally, reduce indentation, and prevent horizontal overflow.
- Generated pages remain owned by `hooks/taxonomy.py`; do not hand-edit the generated taxonomy blocks.

---

## File Map

- `hooks/taxonomy.py`: adds stable semantic hooks around the date and visual separator while retaining Markdown list/link output.
- `docs/resources/css/taxonomy.css`: owns all connected-tree presentation; existing archive landing-card and tag-cloud rules remain intact.
- `tests/test_taxonomy.py`: verifies semantic generated Markdown and undated-article behavior without coupling to CSS.
- `tests/test_site_contract.py`: verifies the stylesheet contains the required scoped theme, hierarchy, interaction, and responsive contracts.
- `tests/test_built_site.py`: verifies MkDocs converts the semantic Markdown rows into the expected final HTML on chapter and archive pages.

### Task 1: Add Semantic Article-Row Markup

**Files:**
- Modify: `tests/test_taxonomy.py`
- Modify: `hooks/taxonomy.py`
- Modify: `tests/test_built_site.py`

**Interfaces:**
- Consumes: `Article.date_text`, `Article.title`, `_relative_link(article, base_dir)`, and the existing newest-first `list[Article]` order.
- Produces: `render_article_list(articles: list[Article], base_dir: Path) -> str` with one Markdown list item per article, containing `.taxonomy-article__date` and `.taxonomy-article__separator` while leaving the title as the existing Markdown link.

- [ ] **Step 1: Write focused failing renderer tests**

Add this method to `TaxonomyCollectorTests` in `tests/test_taxonomy.py`:

```python
    def test_article_rows_expose_semantic_dates_without_changing_links(self):
        dated = taxonomy.Article(
            path=Path("study/dated.md"),
            title="Dated article",
            date_text="2026-08-05",
            date_key=(2026, 8, 5),
            categories=(("校内", "笔记"),),
            tags=(),
            section="study",
        )
        undated = taxonomy.Article(
            path=Path("study/undated.md"),
            title="Undated article",
            date_text="",
            date_key=(0, 0, 0),
            categories=(("校内", "笔记"),),
            tags=(),
            section="study",
        )

        rendered = taxonomy.render_article_list([dated, undated], Path("study"))

        self.assertIn(
            '<time class="taxonomy-article__date" datetime="2026-08-05">2026-08-05</time>',
            rendered,
        )
        self.assertIn(
            '<time class="taxonomy-article__date">未注明日期</time>',
            rendered,
        )
        self.assertEqual(rendered.count('class="taxonomy-article__separator"'), 2)
        self.assertIn('[Dated article](<dated.md>)', rendered)
        self.assertIn('[Undated article](<undated.md>)', rendered)
```

- [ ] **Step 2: Run the focused test and verify the red state**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy.TaxonomyCollectorTests.test_article_rows_expose_semantic_dates_without_changing_links -v
```

Expected: `FAIL`; the current renderer emits plain date text and has no `taxonomy-article__date` class.

- [ ] **Step 3: Add the minimal semantic markup**

Replace `render_article_list` in `hooks/taxonomy.py` with:

```python
def render_article_list(articles: list[Article], base_dir: Path) -> str:
    lines = []
    for article in articles:
        shown_date = article.date_text or "未注明日期"
        datetime_attribute = (
            f' datetime="{escape(article.date_text)}"' if article.date_text else ""
        )
        link = _relative_link(article, base_dir)
        lines.append(
            f'- <time class="taxonomy-article__date"{datetime_attribute}>'
            f'{escape(shown_date)}</time>'
            '<span class="taxonomy-article__separator" aria-hidden="true">·</span>'
            f'[{article.title}](<{link}>)'
        )
    return "\n".join(lines)
```

This deliberately retains the Markdown `-` list marker and Markdown title link. It adds no wrapper around categories and does not reorder input.

- [ ] **Step 4: Run taxonomy tests and regenerate owned pages**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy -v
D:\Project\new-blog\.venv\Scripts\python.exe hooks\taxonomy.py
D:\Project\new-blog\.venv\Scripts\python.exe hooks\taxonomy.py
```

Expected: taxonomy tests pass; the first generator run updates the three chapter indexes and category archive; the second prints `taxonomy: no changes`.

- [ ] **Step 5: Add a final-HTML integration assertion**

Add this method to `BuiltSiteTests` in `tests/test_built_site.py`:

```python
    def test_taxonomy_article_rows_keep_semantic_dates_in_built_html(self):
        for relative in (
            "study/index.html",
            "ctf/index.html",
            "sth/index.html",
            "archive/categories/index.html",
        ):
            html = (SITE / relative).read_text(encoding="utf-8")
            self.assertIn('class="taxonomy-article__date"', html, relative)
            self.assertIn('class="taxonomy-article__separator"', html, relative)
            self.assertRegex(
                html,
                r'<time class="taxonomy-article__date" datetime="\d{4}-\d{2}-\d{2}">',
            )
```

- [ ] **Step 6: Build and verify the semantic HTML test**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_built_site.BuiltSiteTests.test_taxonomy_article_rows_keep_semantic_dates_in_built_html -v
```

Expected: strict build succeeds and the new built-site test passes.

- [ ] **Step 7: Commit the semantic row change**

```powershell
git add -- hooks/taxonomy.py tests/test_taxonomy.py tests/test_built_site.py docs/study/index.md docs/ctf/index.md docs/sth/index.md docs/archive/categories.md
git diff --cached --name-only
git commit -m "feat: add semantic taxonomy article rows"
```

Expected staged files: exactly the seven files listed above. Do not stage article drafts or unrelated generated content.

### Task 2: Style the Connected-Line Tree

**Files:**
- Modify: `tests/test_site_contract.py`
- Modify: `docs/resources/css/taxonomy.css`

**Interfaces:**
- Consumes: `.taxonomy-categories`, heading levels `h2` through `h6`, ordinary generated `ul > li`, `.taxonomy-article__date`, `.taxonomy-article__separator`, and the title link that is a direct child of each `li`.
- Produces: CSS variables `--taxonomy-accent`, `--taxonomy-branch`, and `--taxonomy-indent`, plus scoped connected rails, article-row grid, light/dark theme adaptation, focus/hover feedback, and a `44rem` responsive layout.

- [ ] **Step 1: Write the failing stylesheet contract test**

Add this method to `SiteContractTests` in `tests/test_site_contract.py`:

```python
    def test_taxonomy_uses_connected_tree_styles(self):
        css = (ROOT / "docs/resources/css/taxonomy.css").read_text(encoding="utf-8")

        for token in (
            "--taxonomy-accent: #6171f5",
            "--taxonomy-accent: #7dafe9",
            ".taxonomy-categories h2",
            ".taxonomy-categories h3::before",
            ".taxonomy-categories h4::before",
            ".taxonomy-categories ul > li::before",
            "grid-template-columns: 6.4rem 0.6rem minmax(0, 1fr)",
            ".taxonomy-article__date",
            ".taxonomy-categories li:focus-within",
            "@media (max-width: 44rem)",
            "grid-template-columns: 5.35rem minmax(0, 1fr)",
        ):
            self.assertIn(token, css)
```

- [ ] **Step 2: Run the contract test and verify the red state**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_site_contract.SiteContractTests.test_taxonomy_uses_connected_tree_styles -v
```

Expected: `FAIL` because the existing stylesheet has only identical left borders and no article-row grid.

- [ ] **Step 3: Replace only the taxonomy-category rule block**

In `docs/resources/css/taxonomy.css`, replace the existing rules from `.taxonomy-categories {` through the existing `.taxonomy-categories ul { ... }` block with the following. Leave `.taxonomy-index`, `.tag-cloud`, and tag weight rules unchanged.

```css
.taxonomy-categories {
  --taxonomy-accent: #6171f5;
  --taxonomy-branch: color-mix(in srgb, var(--taxonomy-accent) 30%, transparent);
  --taxonomy-indent: 1.15rem;
  margin-top: 1.2rem;
}

.taxonomy-categories h2,
.taxonomy-categories h3,
.taxonomy-categories h4,
.taxonomy-categories h5,
.taxonomy-categories h6 {
  position: relative;
  min-width: 0;
  padding-block: 0.12rem;
  padding-right: 0.35rem;
  line-height: 1.35;
}

.taxonomy-categories h2 {
  margin: 1.85rem 0 0.75rem;
  padding-left: 0.8rem;
  font-size: 1.38em;
  font-weight: 650;
  border-left: 0.22rem solid var(--taxonomy-accent);
}

.taxonomy-categories h3,
.taxonomy-categories h4,
.taxonomy-categories h5,
.taxonomy-categories h6 {
  margin-top: 1rem;
  margin-bottom: 0.35rem;
  padding-left: 0.7rem;
  border-left: 1px solid var(--taxonomy-branch);
}

.taxonomy-categories h3 {
  margin-left: calc(var(--taxonomy-indent) * 1);
  font-size: 1.16em;
  font-weight: 620;
}

.taxonomy-categories h4 {
  margin-left: calc(var(--taxonomy-indent) * 2);
  font-size: 1.06em;
  font-weight: 600;
}

.taxonomy-categories h5 {
  margin-left: calc(var(--taxonomy-indent) * 3);
  font-size: 1em;
  font-weight: 580;
}

.taxonomy-categories h6 {
  margin-left: calc(var(--taxonomy-indent) * 4);
  font-size: 1em;
  font-weight: 560;
}

.taxonomy-categories h3::before,
.taxonomy-categories h4::before,
.taxonomy-categories h5::before,
.taxonomy-categories h6::before {
  position: absolute;
  top: 50%;
  left: -0.55rem;
  width: 0.55rem;
  border-top: 1px solid var(--taxonomy-branch);
  content: "";
}

.taxonomy-categories ul {
  margin-top: 0.15rem;
  margin-bottom: 1rem;
  padding: 0.15rem 0 0.2rem 0.75rem;
  list-style: none;
  border-left: 1px solid var(--taxonomy-branch);
}

.taxonomy-categories h2 + ul { margin-left: 0.1rem; }
.taxonomy-categories h3 + ul { margin-left: calc(var(--taxonomy-indent) * 1 + 0.1rem); }
.taxonomy-categories h4 + ul { margin-left: calc(var(--taxonomy-indent) * 2 + 0.1rem); }
.taxonomy-categories h5 + ul { margin-left: calc(var(--taxonomy-indent) * 3 + 0.1rem); }
.taxonomy-categories h6 + ul { margin-left: calc(var(--taxonomy-indent) * 4 + 0.1rem); }

.taxonomy-categories ul > li {
  position: relative;
  display: grid;
  grid-template-columns: 6.4rem 0.6rem minmax(0, 1fr);
  align-items: baseline;
  min-width: 0;
  margin: 0;
  padding: 0.34rem 0.5rem;
  border-radius: 0.45rem;
  transition: background-color 140ms ease;
}

.taxonomy-categories ul > li::before {
  position: absolute;
  top: 1.05em;
  left: -0.75rem;
  width: 0.65rem;
  border-top: 1px solid var(--taxonomy-branch);
  content: "";
}

.taxonomy-categories li:hover,
.taxonomy-categories li:focus-within {
  background: color-mix(in srgb, var(--taxonomy-accent) 8%, transparent);
}

.taxonomy-categories li > a {
  min-width: 0;
  overflow-wrap: anywhere;
}

.taxonomy-categories li > a:focus-visible {
  border-radius: 0.15rem;
  outline: 2px solid var(--taxonomy-accent);
  outline-offset: 2px;
}

.taxonomy-article__date {
  color: color-mix(in srgb, var(--md-typeset-color) 62%, transparent);
  font-size: 0.82rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.taxonomy-article__separator {
  color: color-mix(in srgb, var(--md-typeset-color) 38%, transparent);
  text-align: center;
}
```

- [ ] **Step 4: Consolidate dark-theme handling at the container**

Replace the old dark-theme heading-border selector block with:

```css
[data-md-color-scheme="slate"] .taxonomy-categories {
  --taxonomy-accent: #7dafe9;
  --taxonomy-branch: color-mix(in srgb, var(--taxonomy-accent) 36%, transparent);
}
```

Keep the existing dark-theme `.tag-cloud a` rule immediately after it.

- [ ] **Step 5: Add responsive and reduced-motion tree rules**

Inside the existing `@media (max-width: 44rem)` block, after `.taxonomy-index`, add:

```css
  .taxonomy-categories {
    --taxonomy-indent: 0.72rem;
  }

  .taxonomy-categories h2 {
    font-size: 1.25em;
  }

  .taxonomy-categories ul {
    padding-left: 0.55rem;
  }

  .taxonomy-categories ul > li {
    grid-template-columns: 5.35rem minmax(0, 1fr);
    column-gap: 0.45rem;
    padding-inline: 0.35rem;
  }

  .taxonomy-categories ul > li::before {
    left: -0.55rem;
    width: 0.5rem;
  }

  .taxonomy-article__date {
    font-size: 0.72rem;
  }

  .taxonomy-article__separator {
    display: none;
  }
```

Extend the existing reduced-motion selector so it reads:

```css
@media (prefers-reduced-motion: reduce) {
  .taxonomy-index > p > a,
  .taxonomy-categories ul > li,
  .tag-cloud a {
    transition: none;
  }
}
```

- [ ] **Step 6: Run the CSS contract and source tests**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_site_contract tests.test_taxonomy -v
```

Expected: all tests pass; no taxonomy generator output or content order changes occur.

- [ ] **Step 7: Commit the connected-tree stylesheet**

```powershell
git add -- docs/resources/css/taxonomy.css tests/test_site_contract.py
git diff --cached --name-only
git commit -m "style: add connected taxonomy trees"
```

Expected staged files: exactly `docs/resources/css/taxonomy.css` and `tests/test_site_contract.py`.

### Task 3: Strict Build and Visual Acceptance

**Files:**
- Verify: `site/study/index.html`
- Verify: `site/ctf/index.html`
- Verify: `site/sth/index.html`
- Verify: `site/archive/categories/index.html`

**Interfaces:**
- Consumes: semantic row markup from Task 1 and connected-tree stylesheet from Task 2.
- Produces: a strict, fully tested build ready for the user's browser acceptance pass; no additional source interface.

- [ ] **Step 1: Verify generator idempotence and repository whitespace**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe hooks\taxonomy.py
git diff --check
```

Expected: `taxonomy: no changes`; `git diff --check` exits successfully without output.

- [ ] **Step 2: Run the full automated suite**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest discover -s tests -v
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_built_site -v
```

Expected: all source tests pass, strict MkDocs build exits `0`, and all built-site tests pass.

- [ ] **Step 3: Start the local preview without blocking the implementation session**

If port `8001` is not already serving this repository, run in a separate PowerShell window:

```powershell
cd D:\Project\new-blog
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8001
```

Expected: MkDocs reports `Serving on http://127.0.0.1:8001/` and remains available while pages are inspected.

- [ ] **Step 4: Perform the light/dark desktop acceptance pass**

Open these URLs at a desktop width:

```text
http://127.0.0.1:8001/study/?rev=20260805-taxonomy-tree
http://127.0.0.1:8001/ctf/?rev=20260805-taxonomy-tree
http://127.0.0.1:8001/sth/?rev=20260805-taxonomy-tree
http://127.0.0.1:8001/archive/categories/?rev=20260805-taxonomy-tree
```

Verify in both themes:

- First-level category rails are visibly stronger than deeper connectors.
- Light rails use `#6171F5`; dark rails use `#7DAFE9`.
- `笔记 → 高等数学 → 文章` and `WP → 赛事 → 文章` read as connected branches.
- Dates align in one column, titles align in the next column, and articles remain newest-first inside each leaf.
- Hover and keyboard focus produce the restrained theme-tinted row background.
- Category trees remain lightweight rather than appearing as stacked cards.

- [ ] **Step 5: Perform the narrow-width acceptance pass**

At widths `390px` and `768px`, revisit the same four URLs and verify:

- Every full `YYYY-MM-DD` remains visible.
- Long article titles wrap under their own title column.
- Connector indentation compresses without collapsing the hierarchy.
- No taxonomy container or page creates a horizontal scrollbar.
- Keyboard focus outlines remain visible.

- [ ] **Step 6: Record the final clean-state evidence**

Run:

```powershell
git status --short
git log -2 --oneline
```

Expected: no unexpected files are modified; the latest two commits are the semantic-row and connected-tree commits. If the user has unrelated drafts, report them explicitly and leave them untouched.
