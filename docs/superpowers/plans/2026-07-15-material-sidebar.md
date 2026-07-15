# Material Native Category Sidebar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate Material-native collapsible category navigation for the three chapter sidebars, add a theme-colored active rail, and move the GitHub link from the header to the About page.

**Architecture:** Extend `hooks/taxonomy.py` so the same normalized category tree feeds both chapter index Markdown and nested awesome-nav YAML. Keep Material 9.6.20's installed `nav-item.html` untouched; its native active-state checkbox logic handles expansion. Add only focused CSS for the active link and remove `repo_url` so Material no longer renders the header source block.

**Tech Stack:** Python 3.10+, MkDocs 1.6.1, Material for MkDocs 9.6.20, mkdocs-awesome-nav 3.3.0, PyYAML, CSS, Python `unittest`.

## Global Constraints

- Do not copy or override Material's `partials/nav-item.html`.
- Do not add custom sidebar JavaScript.
- Preserve `study / ctf / sth` paths and all article URLs.
- Strip only the chapter root (`校内 / CTF / 随笔`) from sidebar category paths.
- Keep leaf articles newest-to-oldest and category names in deterministic dictionary order.
- Light active rail is `#6171F5`; dark active rail is `#7DAFE9`.
- Remove the header repository entry and add `https://github.com/TangentZX` to About.

---

### Task 1: Generate Nested Chapter Navigation

**Files:**
- Modify: `hooks/taxonomy.py`
- Modify: `tests/test_taxonomy.py`
- Generated: `docs/study/.nav.yml`
- Generated: `docs/ctf/.nav.yml`
- Generated: `docs/sth/.nav.yml`
- Modify: `tests/test_content_migration.py`

**Interfaces:**
- Produces: `_build_section_category_tree(articles: list[Article], section: str) -> dict`.
- Produces: `render_section_navigation(articles: list[Article], section: str) -> dict`.
- Consumes: date-sorted `Article` objects and `SECTION_CATEGORY_ROOTS`.

- [ ] **Step 1: Write failing navigation-tree tests**

Assert the exact real navigation structures:

```python
self.assertEqual(
    taxonomy.render_section_navigation(articles, "study"),
    {
        "nav": [
            "index.md",
            {"笔记": [
                {"数据结构": ["数据结构实验复习.md", "数据结构复习整理.md"]},
                {"程序设计(A)(C)": ["程序设计(A)(C)作业.md"]},
                {"线性代数": ["线性代数-矩阵笔记.md"]},
            ]},
        ]
    },
)
```

Add equivalent exact expectations for `ctf` and `sth`. Update the migration test's `.nav.yml` expectations from flat filename lists to nested dictionaries.

- [ ] **Step 2: Run focused tests and verify failure**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_taxonomy tests.test_content_migration.MigratedRepositoryTests.test_section_navigation_is_newest_first
```

Expected: error because `render_section_navigation` does not exist and current generated YAML is flat.

- [ ] **Step 3: Implement one shared section tree**

Extract section filtering from `render_section_categories`:

```python
def _build_section_category_tree(articles, section):
    root = SECTION_CATEGORY_ROOTS[section]
    return _build_category_tree(
        articles,
        lambda path: path[1:] if path and path[0] == root else None,
    )
```

Convert the tree recursively to awesome-nav data. Emit direct leaf articles in their existing date order and child categories in sorted order:

```python
def _navigation_items(node):
    items = [article.path.name for article in node.get("__articles__", [])]
    for name in sorted(key for key in node if key != "__articles__"):
        items.append({name: _navigation_items(node[name])})
    return items

def render_section_navigation(articles, section):
    tree = _build_section_category_tree(articles, section)
    return {"nav": ["index.md", *_navigation_items(tree)]}
```

- [ ] **Step 4: Replace flat nav generation**

In `sync_taxonomy`, replace the flat filename list with:

```python
navigation = render_section_navigation(section_articles, section)
```

Keep `yaml.safe_dump(..., allow_unicode=True, sort_keys=False)`.

- [ ] **Step 5: Stop the existing 8001 server, run sync twice, and test**

The live server retains the old hook object, so stop only the verified 8001 listener before syncing. Run the generator twice; expect updates on the first run and `taxonomy: no changes` on the second. Run the focused tests and expect all pass.

---

### Task 2: Add the Screenshot-Like Active State

**Files:**
- Modify: `docs/resources/css/leftsidebar.css`
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: Material's existing `.md-nav__link--active` class.
- Produces: a short active rail without changing Material's nested-nav DOM.

- [ ] **Step 1: Add failing CSS contracts**

Require an active anchor pseudo-element, both colors, relative positioning, and reduced-motion support:

```python
self.assertIn("a.md-nav__link--active::before", css)
self.assertIn("#6171f5", css)
self.assertIn("#7dafe9", css)
self.assertIn("prefers-reduced-motion: reduce", css)
```

- [ ] **Step 2: Run the focused contract and verify failure**

Expected: missing active pseudo-element and colors.

- [ ] **Step 3: Implement minimal CSS**

Use `position: relative` on primary sidebar links. Add a rounded `3px` wide, `1.35rem` high `::before` rail on active anchors, centered vertically at `left: -0.65rem`. Use `#6171f5` in light mode and `#7dafe9` in slate mode. Preserve existing hover translation and disable transitions under reduced motion.

- [ ] **Step 4: Run the focused contract**

Expected: pass without altering secondary TOC styles.

---

### Task 3: Move GitHub to About and Verify Material Behavior

**Files:**
- Modify: `mkdocs.yml`
- Modify: `docs/about/index.md`
- Modify: `tests/test_site_contract.py`
- Modify: `tests/test_built_site.py`

**Interfaces:**
- Removes: Material header source block driven by `repo_url`.
- Produces: About-page profile link `https://github.com/TangentZX`.

- [ ] **Step 1: Add failing configuration and built-site contracts**

Assert `repo_url` is absent, About contains the profile URL, built homepage lacks `class="md-source"`, and built About contains the GitHub profile URL. Add a built article check that its active nested navigation inputs include `checked` while a sibling category input remains unchecked.

- [ ] **Step 2: Run focused tests and verify failure**

Expected: current configuration still contains `repo_url`, About lacks the profile URL, and built header contains `md-source`.

- [ ] **Step 3: Apply the content change**

Delete `repo_url` from `mkdocs.yml`. Add this profile item beside email:

```markdown
- **GitHub：** [TangentZX](https://github.com/TangentZX)
```

- [ ] **Step 4: Strictly build and run all tests**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict --quiet
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest discover -s tests
git diff --check
```

Expected: strict build exit 0, all tests pass, and no whitespace errors.

- [ ] **Step 5: Restart and inspect 8001**

Start MkDocs with the updated hook. In the browser inspect a data-structure article, a CTF article, a miscellaneous article, and About. Verify native arrows, current-branch expansion, collapsed siblings, active rail in both themes, no GitHub header block, About profile link, mobile drawer behavior, and no horizontal overflow.
