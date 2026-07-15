# Automatic Taxonomy Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing article `date`, `categories`, and `tags` front matter into automatically maintained section indexes, navigation order, category archives, and a tag cloud/listing.

**Architecture:** A local MkDocs hook runs during `on_config`, scans the three article directories, normalizes metadata, and writes deterministic generated blocks before MkDocs discovers files. Material's bundled `material/tags` plugin renders tag-to-article listings; the hook supplies the frequency-scaled cloud and independent hierarchical category page.

**Tech Stack:** Python 3.10+, MkDocs 1.6.1 hooks, Material for MkDocs 9.6.20 `material/tags`, PyYAML, Markdown, CSS, Python `unittest`.

## Global Constraints

- Existing article bodies and front matter values must not be rewritten.
- Scan only `docs/study`, `docs/ctf`, and `docs/sth`; ignore each `index.md`.
- Keep existing root navigation entries and add “归档” between “随笔” and “友链”.
- Preserve author-written text outside `<!-- taxonomy:articles:start/end -->` markers.
- Accept string, flat-list, and nested-list forms for `categories`; accept string or list for `tags`.
- Normalize displayed dates to `YYYY-MM-DD`; missing or invalid dates sort last without failing the build.
- Generated files are written only when bytes change.
- Do not add third-party dependencies or use deprecated `tags_file`.

---

### Task 1: Metadata Collector and Renderers

**Files:**
- Create: `hooks/__init__.py`
- Create: `hooks/taxonomy.py`
- Create: `tests/test_taxonomy.py`

**Interfaces:**
- Produces: `Article(path, title, date_text, date_key, categories, tags, section)`.
- Produces: `collect_articles(docs_dir: Path) -> list[Article]`.
- Produces: `render_article_list(articles, base_dir) -> str`, `render_categories(articles) -> str`, and `render_tags(articles) -> str`.

- [ ] **Step 1: Write failing metadata tests**

Create tests that import `hooks.taxonomy`, collect the real migrated documents, and assert:

```python
articles = taxonomy.collect_articles(ROOT / "docs")
self.assertEqual(len(articles), 9)
self.assertEqual(len({path for a in articles for path in a.categories}), 8)
self.assertEqual(len({tag for a in articles for tag in a.tags}), 18)
self.assertEqual(sum(len(a.tags) for a in articles), 24)
self.assertEqual(articles[0].date_text, "2026-07-02")
```

Add focused temporary-file cases for `categories: [[CTF, WP, Event]]`, `categories: Notes`, a flat category list, string tags, missing dates, and a filename fallback title.

- [ ] **Step 2: Run tests and verify the module is missing**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy
```

Expected: import failure for `hooks.taxonomy`.

- [ ] **Step 3: Implement front matter parsing and normalization**

Implement an immutable `Article` dataclass and helpers that:

```python
SECTION_TITLES = {"study": "校内", "ctf": "CTF", "sth": "随笔"}

def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    _, raw, _ = text.split("---", 2)
    return yaml.safe_load(raw) or {}

def _normalize_date(value) -> tuple[str, tuple[int, int, int]]:
    if isinstance(value, (date, datetime)):
        value = value.date() if isinstance(value, datetime) else value
        return value.isoformat(), (value.year, value.month, value.day)
    match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", str(value or ""))
    if not match:
        return "", (0, 0, 0)
    year, month, day = map(int, match.groups())
    return f"{year:04d}-{month:02d}-{day:02d}", (year, month, day)
```

Normalize category paths to `tuple[str, ...]`, tags to de-duplicated `tuple[str, ...]`, and sort collected articles descending by `date_key`, then by title.

- [ ] **Step 4: Implement deterministic renderers**

- `render_article_list` emits `- YYYY-MM-DD · [Title](<relative/path.md>)`.
- `render_categories` builds a nested dictionary from category tuples and emits headings from `##` downward plus each leaf's date-sorted article list inside `<div class="taxonomy-categories" markdown>`.
- `render_tags` counts each tag with `Counter`, maps counts to integer weights 1–5, uses `pymdownx.slugs.slugify(case="lower")`, and emits `.tag-cloud` links followed by `<!-- material/tags -->`.

- [ ] **Step 5: Run Task 1 tests**

Run the same unittest command. Expected: all metadata and renderer tests pass.

---

### Task 2: Idempotent Build Synchronization

**Files:**
- Modify: `hooks/taxonomy.py`
- Modify: `tests/test_taxonomy.py`
- Modify: `docs/study/index.md`
- Modify: `docs/ctf/index.md`
- Modify: `docs/sth/index.md`

**Interfaces:**
- Produces: `sync_taxonomy(docs_dir: Path) -> list[Path]`, returning only changed paths.
- Produces: MkDocs hook `on_config(config, **kwargs)` that calls `sync_taxonomy(Path(config.docs_dir))` and returns `config`.

- [ ] **Step 1: Write failing synchronization tests**

In a temporary docs tree, create one article per section plus section indexes containing author text and markers. Assert that the first sync changes `.nav.yml`, section indexes, `archive/categories.md`, and `archive/tags.md`; assert the second sync returns an empty list and preserves author text outside markers.

- [ ] **Step 2: Run the focused test and verify failure**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy.TaxonomySyncTests
```

Expected: failure because `sync_taxonomy` is absent.

- [ ] **Step 3: Implement generated-block and write-if-changed helpers**

Use exact markers:

```python
START = "<!-- taxonomy:articles:start -->"
END = "<!-- taxonomy:articles:end -->"

def _replace_block(source: str, generated: str) -> str:
    block = f"{START}\n{generated.rstrip()}\n{END}"
    if START in source and END in source:
        prefix, rest = source.split(START, 1)
        _, suffix = rest.split(END, 1)
        return f"{prefix.rstrip()}\n\n{block}{suffix}"
    return f"{source.rstrip()}\n\n{block}\n"

def _write_if_changed(path: Path, content: str) -> bool:
    content = content.rstrip() + "\n"
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True
```

- [ ] **Step 4: Implement synchronization**

For each section, update the marker block with its date-sorted articles and write `.nav.yml` as `index.md` followed by filenames in the same order. Write generated archive pages with YAML metadata, a generated-file warning comment, renderer output, and stable trailing newlines. Return changed paths.

- [ ] **Step 5: Add markers to existing section indexes and run sync**

Replace the current handwritten lists with empty start/end marker pairs, retain each `#` heading, then run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe hooks\taxonomy.py
```

Expected: three section lists/nav files and two archive pages are populated.

- [ ] **Step 6: Verify idempotence**

Run the script a second time. Expected output: `taxonomy: no changes`.

- [ ] **Step 7: Run Task 2 and existing migration tests**

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy tests.test_content_migration
```

Expected: all tests pass and newest-to-oldest ordering remains intact.

---

### Task 3: Archive Navigation, Material Tags, and Styling

**Files:**
- Modify: `mkdocs.yml`
- Modify: `docs/.nav.yml`
- Create: `docs/archive/index.md`
- Create: `docs/archive/.nav.yml`
- Create: `docs/resources/css/taxonomy.css`
- Modify: `tests/test_site_contract.py`
- Modify: `tests/test_built_site.py`

**Interfaces:**
- Consumes: generated `docs/archive/categories.md` and `docs/archive/tags.md` from Task 2.
- Produces: `/archive/`, `/archive/categories/`, and `/archive/tags/` plus tag links on article pages.

- [ ] **Step 1: Write failing site contracts**

Assert that:

```python
self.assertIn("material/tags", config["plugins"])
self.assertIn("hooks/taxonomy.py", config["hooks"])
self.assertIn("resources/css/taxonomy.css", config["extra_css"])
self.assertEqual(root_nav[4], {"归档": "archive"})
```

Add built-site checks for the three archive HTML files, `.tag-cloud`, `tag:` anchors, all 18 tag labels, and representative category paths.

- [ ] **Step 2: Run contracts and verify failure**

Run the focused site contract tests. Expected: missing plugin, hook, CSS, nav entry, and built pages.

- [ ] **Step 3: Register framework and navigation**

In `mkdocs.yml`, add `material/tags` after `search`, add:

```yaml
hooks:
  - hooks/taxonomy.py
```

and append `resources/css/taxonomy.css`. Add root “归档” navigation and an archive `.nav.yml` ordered as index, categories, tags.

- [ ] **Step 4: Create archive landing page and styles**

The landing page links to 分类 and 标签. CSS styles `.taxonomy-categories`, `.tag-cloud`, `.tag-weight-1` through `.tag-weight-5`, focus states, dark mode, a one-column narrow layout, and reduced-motion behavior. Keep word-cloud sizes between `0.72rem` and `1.3rem`.

- [ ] **Step 5: Build and inspect output contracts**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict --site-dir $env:TEMP\new-blog-site-verify
```

Expected: exit code 0; existing absolute-image messages remain informational. Then run all tests with `unittest discover` and expect all pass.

- [ ] **Step 6: Browser checkpoint**

Open `/archive/categories/?rev=20260715-taxonomy1` and `/archive/tags/?rev=20260715-taxonomy1`. Verify hierarchy, cloud scaling, tag jumps, deep/light modes, and no horizontal overflow before committing implementation.
