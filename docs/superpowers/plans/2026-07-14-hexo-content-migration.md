# Hexo Content Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Copy all 9 existing Hexo posts and all 131 legacy images into the MkDocs blog, preserving content while applying only the compatibility fixes required for navigation and strict builds.

**Architecture:** A focused Python migration script owns deterministic article mapping, Markdown normalization, image copying, and section-index generation. Unit tests cover transformation rules; repository contract tests compare migrated content with the read-only Hexo source; built-site tests verify every migrated page and copied asset is emitted by MkDocs.

**Tech Stack:** Python 3.10, `pathlib`, `shutil`, `re`, `unittest`, MkDocs 1.6.1, Material 9.6.20, mkdocs-awesome-nav 3.3.0

## Global Constraints

- Treat `D:\Project\my-blog` as read-only.
- Do not push or deploy to GitHub.
- Preserve all 9 original article filenames and all original image paths.
- Copy every file under `my-blog/source/images`; do not replace `docs/images/avatar.png`.
- Only normalize `catagories`, article-level H1 headings, and Markdown image-target syntax.
- Do not edit article facts, code, prose, dates, authors, categories, or tags.
- Keep root navigation `首页 / 校内 / CTF / 随笔 / 友链 / 关于` unchanged.

---

## File Structure

- Create `scripts/migrate_hexo_content.py`: deterministic migration and validation entry point.
- Create `tests/test_content_migration.py`: transformation-unit and migrated-repository contract tests.
- Modify `tests/test_built_site.py`: verify all migrated article pages and legacy images are built.
- Modify `docs/ctf/index.md`: newest-first links to the two migrated CTF posts.
- Modify `docs/study/index.md`: newest-first links to the four migrated school posts.
- Modify `docs/sth/index.md`: newest-first links to the three migrated essay posts.
- Create 9 article files under `docs/ctf`, `docs/study`, and `docs/sth`.
- Create the copied legacy image tree under `docs/images` while preserving `avatar.png`.

---

### Task 1: Markdown Compatibility Transformer

**Files:**
- Create: `scripts/migrate_hexo_content.py`
- Create: `tests/test_content_migration.py`

**Interfaces:**
- Consumes: UTF-8 Hexo Markdown text.
- Produces: `normalize_article(text: str) -> str` with normalized Front Matter, one matching article H1, and safe `/images/...` destinations.

- [ ] **Step 1: Write the failing transformation tests**

```python
from pathlib import Path
import re
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.migrate_hexo_content import normalize_article


class MarkdownTransformationTests(unittest.TestCase):
    def test_normalizes_front_matter_title_and_image_destination(self):
        source = """---
title: Demo
catagories:
- [随便写写]
---
正文
![图片](/images/程序设计(A)(C)/示例.png)
"""
        result = normalize_article(source)
        self.assertNotIn("catagories:", result)
        self.assertIn("categories:", result)
        self.assertIn("\n# Demo\n", result)
        self.assertIn("![图片](</images/程序设计(A)(C)/示例.png>)", result)

    def test_does_not_duplicate_matching_h1_or_rewrite_plain_urls(self):
        source = """---
title: Demo
---
# Demo
http://127.0.0.1:12961/images/flag.txt
"""
        result = normalize_article(source)
        self.assertEqual(result.count("# Demo"), 1)
        self.assertIn("http://127.0.0.1:12961/images/flag.txt", result)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_content_migration -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.migrate_hexo_content'`.

- [ ] **Step 3: Implement the minimal transformer**

```python
from __future__ import annotations

import re

IMAGE_LINK = re.compile(
    r"(!\[[^\]]*\]\()(/images/.+?\.(?:png|jpe?g|gif|webp|svg))(\))",
    re.IGNORECASE,
)


def _split_front_matter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("article is missing YAML Front Matter")
    end = normalized.find("\n---\n", 4)
    if end == -1:
        raise ValueError("article has unterminated YAML Front Matter")
    return normalized[4:end], normalized[end + 5 :]


def _title_from_front_matter(front_matter: str) -> str:
    match = re.search(r"(?m)^title:\s*(.+?)\s*$", front_matter)
    if not match:
        raise ValueError("article Front Matter is missing title")
    return match.group(1).strip().strip("\"'")


def _has_matching_h1(body: str, title: str) -> bool:
    fenced = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced and stripped.startswith("# "):
            if stripped[2:].strip() == title:
                return True
    return False


def normalize_article(text: str) -> str:
    front_matter, body = _split_front_matter(text)
    front_matter = re.sub(
        r"(?m)^catagories:", "categories:", front_matter
    )
    title = _title_from_front_matter(front_matter)
    body = IMAGE_LINK.sub(r"\1<\2>\3", body)
    body = body.lstrip("\n")
    if not _has_matching_h1(body, title):
        body = f"# {title}\n\n{body}"
    return f"---\n{front_matter}\n---\n\n{body.rstrip()}\n"
```

- [ ] **Step 4: Run the transformation tests**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_content_migration -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Commit the transformer**

```powershell
git add scripts/migrate_hexo_content.py tests/test_content_migration.py
git commit -m "test: define Hexo migration transformations"
```

---

### Task 2: Deterministic Article and Image Migration

**Files:**
- Modify: `scripts/migrate_hexo_content.py`
- Modify: `tests/test_content_migration.py`
- Modify: `docs/ctf/index.md`
- Modify: `docs/study/index.md`
- Modify: `docs/sth/index.md`
- Create: `docs/ctf/Tzxy's WHUCTF2025新生赛WP.md`
- Create: `docs/ctf/WHUCTF2026_WP.md`
- Create: `docs/study/程序设计(A)(C)作业.md`
- Create: `docs/study/线性代数-矩阵笔记.md`
- Create: `docs/study/数据结构复习整理.md`
- Create: `docs/study/数据结构实验复习.md`
- Create: `docs/sth/ArchLinux 折腾心得.md`
- Create: `docs/sth/流光协奏之梦.md`
- Create: `docs/sth/郑州强网论坛 学习心得.md`
- Create: copied files below `docs/images/CTF`, `docs/images/reward`, `docs/images/程序设计(A)(C)`, `docs/images/笔记`, and `docs/images/随便写写`

**Interfaces:**
- Consumes: `migrate(source_blog: Path, target_blog: Path) -> None` with a Hexo root and MkDocs root.
- Produces: nine normalized posts, three deterministic section indexes, and a byte-identical copy of every legacy image.

- [ ] **Step 1: Add failing repository-contract tests**

Append to `tests/test_content_migration.py`:

```python
from scripts.migrate_hexo_content import ARTICLE_MAP


class MigratedRepositoryTests(unittest.TestCase):
    source_blog = Path(r"D:\Project\my-blog")
    target_blog = ROOT

    def test_all_mapped_articles_exist_and_are_normalized(self):
        self.assertEqual(len(ARTICLE_MAP), 9)
        for source_relative, target_relative in ARTICLE_MAP:
            self.assertTrue((self.source_blog / source_relative).is_file())
            target = self.target_blog / target_relative
            self.assertTrue(target.is_file(), target_relative)
            text = target.read_text(encoding="utf-8")
            self.assertNotIn("catagories:", text)
            self.assertNotRegex(text, r"!\[[^\]]*\]\(/images/")
            front_matter = text.split("---", 2)[1]
            metadata = yaml.safe_load(front_matter)
            self.assertIn("title", metadata)
            self.assertIn(f"# {metadata['title']}", text)

            image_refs = re.findall(
                r"!\[[^\]]*\]\(<(/images/.+?\.(?:png|jpe?g|gif|webp|svg))>\)",
                text,
                flags=re.IGNORECASE,
            )
            for image_ref in image_refs:
                image_target = self.target_blog / "docs" / image_ref.lstrip("/")
                self.assertTrue(image_target.is_file(), image_ref)

    def test_every_legacy_image_is_copied_byte_for_byte(self):
        source_root = self.source_blog / "source" / "images"
        target_root = self.target_blog / "docs" / "images"
        source_files = sorted(p for p in source_root.rglob("*") if p.is_file())
        self.assertEqual(len(source_files), 131)
        for source in source_files:
            target = target_root / source.relative_to(source_root)
            self.assertTrue(target.is_file(), target)
            self.assertEqual(source.read_bytes(), target.read_bytes(), target)
        self.assertTrue((target_root / "avatar.png").is_file())

    def test_section_indexes_link_every_migrated_article(self):
        for _, target_relative in ARTICLE_MAP:
            target = Path(target_relative)
            index = self.target_blog / target.parent / "index.md"
            self.assertIn(target.name, index.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run the contract tests and verify that migration output is absent**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_content_migration.MigratedRepositoryTests -v
```

Expected: FAIL because `ARTICLE_MAP` or migrated target files do not yet exist.

- [ ] **Step 3: Add the deterministic mappings and migration operations**

Append to `scripts/migrate_hexo_content.py`, moving the `if __name__` block to the end if one exists:

```python
import argparse
from pathlib import Path
import shutil

ARTICLE_MAP = (
    ("source/_posts/Tzxy's WHUCTF2025新生赛WP.md", "docs/ctf/Tzxy's WHUCTF2025新生赛WP.md"),
    ("source/_posts/WHUCTF2026_WP.md", "docs/ctf/WHUCTF2026_WP.md"),
    ("source/_posts/程序设计(A)(C)作业.md", "docs/study/程序设计(A)(C)作业.md"),
    ("source/_posts/线性代数-矩阵笔记.md", "docs/study/线性代数-矩阵笔记.md"),
    ("source/_posts/数据结构复习整理.md", "docs/study/数据结构复习整理.md"),
    ("source/_posts/数据结构实验复习.md", "docs/study/数据结构实验复习.md"),
    ("source/_posts/ArchLinux 折腾心得.md", "docs/sth/ArchLinux 折腾心得.md"),
    ("source/_posts/流光协奏之梦.md", "docs/sth/流光协奏之梦.md"),
    ("source/_posts/郑州强网论坛 学习心得.md", "docs/sth/郑州强网论坛 学习心得.md"),
)

SECTION_INDEXES = {
    "docs/ctf/index.md": """# CTF

- 2026-04-20 · [CTF辞のWHUCTF2026校赛WP](<WHUCTF2026_WP.md>)
- 2025-10-24 · [Tzxy's WHUCTF2025新生赛WP](<Tzxy's WHUCTF2025新生赛WP.md>)
""",
    "docs/study/index.md": """# 校内

- 2026-07-02 · [数据结构实验复习整理](<数据结构实验复习.md>)
- 2026-06-26 · [数据结构复习整理](<数据结构复习整理.md>)
- 2025-10-09 · [程序设计(A)(C)作业](<程序设计(A)(C)作业.md>)
- 2025-10-02 · [线性代数_矩阵笔记](<线性代数-矩阵笔记.md>)
""",
    "docs/sth/index.md": """# 随笔

- 2025-12-27 · [流光协奏之梦](<流光协奏之梦.md>)
- 2025-11-28 · [ArchLinux 折腾心得](<ArchLinux 折腾心得.md>)
- 2025-11-23 · [郑州游记](<郑州强网论坛 学习心得.md>)
""",
}


def migrate(source_blog: Path, target_blog: Path) -> None:
    for source_relative, target_relative in ARTICLE_MAP:
        source = source_blog / source_relative
        if not source.is_file():
            raise FileNotFoundError(source)
        target = target_blog / target_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            normalize_article(source.read_text(encoding="utf-8")),
            encoding="utf-8",
            newline="\n",
        )

    source_images = source_blog / "source" / "images"
    target_images = target_blog / "docs" / "images"
    for source in source_images.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(source_images)
        if relative == Path("avatar.png"):
            continue
        target = target_images / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    for relative, content in SECTION_INDEXES.items():
        (target_blog / relative).write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_blog", type=Path)
    parser.add_argument("target_blog", type=Path)
    args = parser.parse_args()
    migrate(args.source_blog.resolve(), args.target_blog.resolve())


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the migration once from the MkDocs root**

Run:

```powershell
.\.venv\Scripts\python.exe scripts\migrate_hexo_content.py D:\Project\my-blog D:\Project\new-blog
```

Expected: exit code 0; nine article files, three updated indexes, and the copied image directories appear under `docs`.

- [ ] **Step 5: Run the full migration tests**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_content_migration -v
```

Expected: 5 tests pass, including all 131 byte-for-byte image comparisons.

- [ ] **Step 6: Confirm the Hexo source remains untouched**

Run:

```powershell
git -C D:\Project\my-blog status --short
```

Expected: no new migration-created changes. If pre-existing user changes are listed, preserve them and confirm that none correspond to this migration run.

- [ ] **Step 7: Commit the migrated source content**

```powershell
git add scripts/migrate_hexo_content.py tests/test_content_migration.py docs/ctf docs/study docs/sth docs/images
git commit -m "feat: migrate legacy blog content"
```

---

### Task 3: Built-Site Coverage and Final Link Verification

**Files:**
- Modify: `tests/test_built_site.py`

**Interfaces:**
- Consumes: `site/` produced by `mkdocs build --strict`.
- Produces: regression coverage for all nine generated article pages and every copied image path.

- [ ] **Step 1: Add failing built-output assertions**

Append these methods to `BuiltSiteTests` in `tests/test_built_site.py`:

```python
    def test_migrated_article_pages_are_built(self):
        article_paths = (
            "ctf/Tzxy's WHUCTF2025新生赛WP/index.html",
            "ctf/WHUCTF2026_WP/index.html",
            "study/程序设计(A)(C)作业/index.html",
            "study/线性代数-矩阵笔记/index.html",
            "study/数据结构复习整理/index.html",
            "study/数据结构实验复习/index.html",
            "sth/ArchLinux 折腾心得/index.html",
            "sth/流光协奏之梦/index.html",
            "sth/郑州强网论坛 学习心得/index.html",
        )
        for relative in article_paths:
            self.assertTrue((self.site_dir / relative).is_file(), relative)

    def test_every_legacy_image_is_emitted(self):
        source_images = Path(r"D:\Project\my-blog\source\images")
        built_images = self.site_dir / "images"
        for source in source_images.rglob("*"):
            if source.is_file():
                relative = source.relative_to(source_images)
                self.assertTrue((built_images / relative).is_file(), relative)
```

- [ ] **Step 2: Run only the new built-output tests before rebuilding**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_built_site.BuiltSiteTests.test_migrated_article_pages_are_built tests.test_built_site.BuiltSiteTests.test_every_legacy_image_is_emitted -v
```

Expected: FAIL against the pre-migration `site/` output because migrated pages or image directories are absent.

- [ ] **Step 3: Run a fresh strict build**

Run:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

Expected: exit code 0 with `Documentation built`; no warnings are promoted to errors.

- [ ] **Step 4: Run every test**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: all existing and migration tests pass with `OK` and zero failures.

- [ ] **Step 5: Inspect repository scope and whitespace**

Run:

```powershell
git diff --check
git status --short
```

Expected: no whitespace errors; only the built-site test change remains uncommitted because `site/` and `.venv/` are ignored.

- [ ] **Step 6: Commit built-output verification**

```powershell
git add tests/test_built_site.py
git commit -m "test: verify migrated blog output"
```

- [ ] **Step 7: Perform browser smoke checks**

Run:

```powershell
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8000
```

Verify in the local browser:

- Each of the three section pages lists the expected articles newest-first.
- At least one CTF, school, and essay post opens.
- The long `程序设计(A)(C)作业` page renders images whose path contains parentheses.
- Desktop and 390px mobile layouts have no horizontal overflow introduced by article content.
- Browser console contains no site-generated errors.

- [ ] **Step 8: Final verification record**

Run:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
git status --short --branch
```

Expected: strict build exits 0, all tests pass, and `master` is clean. Do not push or deploy.
