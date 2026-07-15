# Friend Links Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one temporary MkDocs page that compares three responsive friend-link card styles using all 10 entries migrated from the old Hexo blog.

**Architecture:** Keep the experiment isolated in `docs/style-preview-links.md`: semantic links provide the content and page-scoped CSS provides A/B/C layouts. Contract tests verify the complete migrated dataset, safe external-link attributes, local avatars, and the three style markers before the user selects a final design.

**Tech Stack:** MkDocs Material, Markdown with `md_in_html`, semantic HTML, page-scoped CSS, Python `unittest`.

## Global Constraints

- Do not replace `docs/links/index.md` until the user selects one style.
- Use the 10 existing avatars under `docs/images/`; do not copy, convert, or fetch images.
- Ignore every legacy `color` value and use one unified new visual system.
- Support light theme, dark theme, keyboard focus, reduced motion, and one-column mobile layout.
- Do not add JavaScript, dependencies, filtering, random ordering, or link-health checks.

---

### Task 1: Preview Contract

**Files:**
- Create: `tests/test_friend_links_preview.py`
- Test: `tests/test_friend_links_preview.py`

**Interfaces:**
- Consumes: Old friend-link fields already identified in `D:/Project/my-blog/source/links/index.md`.
- Produces: `test_friend_link_preview_contains_migrated_data`, the contract for the temporary preview page.

- [ ] **Step 1: Write the failing test**

Add a test that reads `docs/style-preview-links.md`, asserts the markers `friends-a`, `friends-b`, and `friends-c`, and verifies all of these URLs and avatar filenames occur exactly three times:

```python
entries = {
    "https://www.zt2misay2.cn/": "eveonecat1.jpg",
    "https://lunereal.1kal0vic.top/": "avatar_ika.jpg",
    "https://0n3-0.github.io/": "avatar_one.jpg",
    "https://kuri.jwmc.top/": "avatar_Kuri.jpg",
    "https://oldmaple.top/": "avatar_M4ple.jpg",
    "https://b1ank799.github.io/": "avatar_Blank.jpg",
    "https://lightcloveyou.github.io/": "avatar_lightc.jpg",
    "https://crisq.top/": "avatar_Crisq.jpg",
    "https://huangoxygen.github.io/": "oxygen.jpg",
    "https://dicaeopolis.github.io/": "avatar_Dicaeopolis.png",
}
for url, avatar in entries.items():
    self.assertEqual(preview.count(f'href="{url}"'), 3)
    self.assertEqual(preview.count(f'src="../images/{avatar}"'), 3)
    self.assertTrue((ROOT / "docs/images" / avatar).is_file())
self.assertEqual(preview.count('target="_blank" rel="noopener noreferrer"'), 30)
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_friend_links_preview
```

Expected: `FileNotFoundError` for `docs/style-preview-links.md`.

- [ ] **Step 3: Commit the failing contract together with Task 2 implementation**

Do not make a red-only commit; proceed directly to Task 2 after recording the expected failure.

---

### Task 2: A/B/C Friend-Link Preview

**Files:**
- Create: `docs/style-preview-links.md`
- Test: `tests/test_friend_links_preview.py`

**Interfaces:**
- Consumes: The contract and exact URL/avatar mapping from Task 1.
- Produces: A user-facing comparison page at `/style-preview-links/` with `.friends-a`, `.friends-b`, and `.friends-c` sections.

- [ ] **Step 1: Add page metadata and scoped design tokens**

Create a page with `hide: [navigation, toc]`, a single heading, explanatory copy, and a `.friend-preview` root. Define unified light tokens for surface, border, text, muted text, accent, accent-soft, and shadow; override them under `[data-md-color-scheme="slate"]`.

- [ ] **Step 2: Implement shared semantic cards**

Render the same 10 entries in each section as:

```html
<a class="friend-card" href="https://example.com/" target="_blank" rel="noopener noreferrer">
  <img src="../images/avatar.jpg" alt="Name 的头像" loading="lazy">
  <span class="friend-copy">
    <strong>Blog Name</strong>
    <small>@Name</small>
    <span class="friend-desc">Description</span>
  </span>
</a>
```

Use the exact legacy names, blog titles, and descriptions from the design source. Do not include inline `style`, legacy colors, or scripts.

- [ ] **Step 3: Implement A, B, and C layouts**

- `.friends-a`: three-column centered cards, circular avatar overlapping the upper card edge, generous top padding.
- `.friends-b`: two-column horizontal cards, 72px circular avatar on the left, flexible text on the right.
- `.friends-c`: three-column compact cards with a 44px avatar; keep the full description in the DOM and reveal its emphasis through hover/focus styling without making it inaccessible on touch.
- At `max-width: 44rem`, make all grids one column and remove A's large top offset.
- Add `:focus-visible` outlines and disable transforms under `prefers-reduced-motion: reduce`.

- [ ] **Step 4: Run the focused contract**

Run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_friend_links_preview
```

Expected: one passing test.

- [ ] **Step 5: Verify the live page and strict build**

Request `http://127.0.0.1:8001/style-preview-links/?rev=20260715-1` and verify HTTP 200. Then run:

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict --site-dir $env:TEMP\new-blog-site-verify
```

Expected: exit code 0; existing absolute-image-link messages remain informational.

- [ ] **Step 6: Commit the preview checkpoint**

```powershell
git add tests/test_friend_links_preview.py docs/style-preview-links.md docs/superpowers/plans/2026-07-15-friend-links-preview.md
git commit -m "feat: preview friend link card styles"
```
