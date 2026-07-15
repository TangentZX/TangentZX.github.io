# Chapter Trees and Article Authors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the three content tabs, normalize every article's nested category path, render each chapter's category subtree after its editable introduction, and normalize article authors.

**Architecture:** Keep article files and URLs in `study`, `ctf`, and `sth`. Extend the existing taxonomy hook with separate display-title and category-root mappings, reuse one deterministic tree renderer for both chapter indexes and the global category archive, and preserve all author-written index text outside generated markers.

**Tech Stack:** Python 3.10+, MkDocs 1.6.1 hooks, Material for MkDocs 9.6.20, PyYAML, Python `unittest`.

## Global Constraints

- Root navigation labels become `校内篇 / CTF篇 / 杂篇`; directory names and article URLs do not change.
- Category roots remain `校内 / CTF / 随笔`.
- `程序设计(A)(C)作业` uses `[校内, 笔记, 程序设计(A)(C)]`.
- All non-CTF articles use author `Tangent丶ZX`; both CTF WP articles use author `1so`.
- Existing tags, dates, titles, bodies, and image links remain unchanged.
- Chapter introductions remain editable outside generated taxonomy markers.
- Article lists at every category leaf remain newest-to-oldest.

---

### Task 1: Normalize Article Metadata

**Files:**
- Modify: `tests/test_content_migration.py`
- Modify: all nine article Markdown files under `docs/study`, `docs/ctf`, and `docs/sth`

**Interfaces:**
- Consumes: YAML front matter already read by PyYAML.
- Produces: exact `author` and one nested `categories` path for every migrated article.

- [ ] **Step 1: Add a failing metadata contract**

Add an expected mapping keyed by article path and assert exact values:

```python
expected = {
    "docs/study/程序设计(A)(C)作业.md": ("Tangent丶ZX", [["校内", "笔记", "程序设计(A)(C)"]]),
    "docs/ctf/WHUCTF2026_WP.md": ("1so", [["CTF", "WP", "WHUCTF2026校赛"]]),
}
self.assertEqual(metadata["author"], author)
self.assertEqual(metadata["categories"], categories)
```

The complete mapping in the test must cover all nine files.

- [ ] **Step 2: Run the focused test and verify failure**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_content_migration.MigratedRepositoryTests.test_article_authors_and_category_paths
```

Expected: failure on the first legacy author or category path.

- [ ] **Step 3: Update only article front matter**

Use these exact YAML shapes:

```yaml
author: Tangent丶ZX
categories:
  - [校内, 笔记, 数据结构]
```

and for both CTF files:

```yaml
author: 1so
categories:
  - [CTF, WP, WHUCTF2026校赛]
```

- [ ] **Step 4: Run the focused metadata test**

Expected: pass for all nine mappings.

---

### Task 2: Render Chapter Category Subtrees

**Files:**
- Modify: `hooks/taxonomy.py`
- Modify: `tests/test_taxonomy.py`
- Modify: `docs/study/index.md`
- Modify: `docs/ctf/index.md`
- Modify: `docs/sth/index.md`

**Interfaces:**
- Produces: `SECTION_TITLES = {"study": "校内篇", "ctf": "CTF篇", "sth": "杂篇"}`.
- Produces: `SECTION_CATEGORY_ROOTS = {"study": "校内", "ctf": "CTF", "sth": "随笔"}`.
- Produces: `render_section_categories(articles: list[Article], section: str) -> str`.

- [ ] **Step 1: Add failing renderer and synchronization tests**

Assert the real study subtree contains:

```python
section = taxonomy.render_section_categories(articles, "study")
self.assertIn("## 笔记", section)
self.assertIn("### 数据结构", section)
self.assertIn("### 程序设计(A)(C)", section)
self.assertNotIn("## 校内", section)
```

Update the temporary sync test so its article category starts with `SECTION_CATEGORY_ROOTS[section]`, and assert the generated chapter index contains its child heading and article link.

- [ ] **Step 2: Run taxonomy tests and verify failure**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy
```

Expected: failure because `render_section_categories` is absent.

- [ ] **Step 3: Implement one reusable tree renderer**

Refactor category tree construction so the global archive renders full paths from heading level 2 and the chapter renderer filters by its configured root, strips that first component, and renders the remaining path from heading level 2. Both use `render_article_list`, with `Path("archive")` or `Path(section)` as appropriate.

- [ ] **Step 4: Generate subtrees inside existing markers**

In `sync_taxonomy`, replace:

```python
generated = render_article_list(section_articles, Path(section))
```

with:

```python
generated = render_section_categories(section_articles, section)
```

Update each index heading and add one editable introduction before `taxonomy:articles:start`.

- [ ] **Step 5: Run synchronization twice**

Run `hooks/taxonomy.py` twice. Expected: first run updates three indexes and the category archive; second run prints `taxonomy: no changes`.

- [ ] **Step 6: Run taxonomy and migration tests**

Expected: all focused tests pass and `.nav.yml` remains newest-to-oldest.

---

### Task 3: Rename Navigation and Verify the Built Site

**Files:**
- Modify: `docs/.nav.yml`
- Modify: `tests/test_site_contract.py`
- Modify: `tests/test_built_site.py`

**Interfaces:**
- Produces: top navigation `首页 / 校内篇 / CTF篇 / 杂篇 / 归档 / 友链 / 关于`.

- [ ] **Step 1: Change navigation expectations first**

Update root-navigation and built-navigation tests to require `校内篇`, `CTF篇`, and `杂篇` while keeping the same target directories.

- [ ] **Step 2: Run focused contracts and verify failure**

Run the two navigation tests. Expected: old `校内 / CTF / 随笔` labels fail.

- [ ] **Step 3: Update `docs/.nav.yml`**

Use:

```yaml
- 校内篇: study
- CTF篇: ctf
- 杂篇: sth
```

- [ ] **Step 4: Regenerate, strictly build, and run all tests**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe hooks\taxonomy.py
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict --quiet
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest discover -s tests
git diff --check
```

Expected: strict build exit 0, all tests pass, and no whitespace errors.

- [ ] **Step 5: Browser checkpoint**

Inspect `/study/`, `/ctf/`, `/sth/`, and `/archive/categories/` in light and dark modes. Verify introductions remain above the generated trees, leaf articles are date-sorted, navigation labels are updated, and no horizontal overflow appears.
