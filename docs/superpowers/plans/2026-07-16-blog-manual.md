# Blog Operation Manual Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在仓库根目录创建一份与当前 MkDocs Material 博客完全一致、可长期查阅的中文操作手册 `BLOG_MANUAL.md`。

**Architecture:** 手册采用单文件、场景式结构，所有路径、命令和模板都从当前仓库配置与文章实例中提取。它不参与 MkDocs 导航或站点构建，只服务于维护者；自动生成内容、GitHub 分支和代理限制会被明确标注。

**Tech Stack:** Markdown、MkDocs Material、Python Hook、PowerShell、Git、GitHub Actions

## Global Constraints

- 只新增仓库根目录 `BLOG_MANUAL.md`；不得修改现有 `docs/index.md`。
- 所有命令以 Windows PowerShell 和 `D:\Project\new-blog` 为基准。
- 手册不得建议直接编辑 `site/`、篇章 `.nav.yml`、自动生成的分类页或标签页。
- 文章 Markdown 当前必须直接放在 `docs/study/`、`docs/ctf/`、`docs/sth/` 或新篇章根目录下。
- 正常发布分支为 `main`，构建产物分支为 `gh-pages`；旧博客备份分支不得删除。
- Git 需要代理时使用 `http://127.0.0.1:10808` 的单次命令参数，不把强制推送写成日常发布步骤。

---

### Task 1: 编写场景式博客操作手册

**Files:**
- Create: `BLOG_MANUAL.md`
- Read: `mkdocs.yml`
- Read: `docs/.nav.yml`
- Read: `hooks/taxonomy.py`
- Read: `.github/workflows/deploy.yml`
- Read: `docs/study/*.md`, `docs/ctf/*.md`, `docs/sth/*.md`

**Interfaces:**
- Consumes: MkDocs 配置、三个篇章目录、front matter 约定、taxonomy Hook 映射、GitHub Actions 与现有远程分支职责。
- Produces: 单文件中文维护手册 `BLOG_MANUAL.md`，不被 MkDocs 导航引用。

- [ ] **Step 1: 核对当前项目事实**

Run:

```powershell
cd D:\Project\new-blog
Get-Content -Raw mkdocs.yml
Get-Content -Raw docs\.nav.yml
Get-Content -Raw hooks\taxonomy.py
Get-Content -Raw .github\workflows\deploy.yml
git branch --show-current
git remote -v
```

Expected: 当前分支为 `main`，`origin` 指向 `TangentZX/TangentZX.github.io`；配置包含 `hooks/taxonomy.py`、Material 主题及文章扩展。

- [ ] **Step 2: 创建手册的项目概览和本地开发章节**

Create `BLOG_MANUAL.md` with these exact top-level sections:

```markdown
# TangentZX's Blog 操作手册

## 1. 项目概览
## 2. 本地启动与预览
## 3. 新建文章
## 4. 分类、标签、作者与排序
## 5. 文章图片
## 6. 修改固定页面
## 7. Markdown 常用语法
## 8. 修改样式与脚本
## 9. 新建一个完整篇章
## 10. 构建、测试与发布
## 11. GitHub 分支与旧博客备份
## 12. 常见问题
## 13. 发布检查清单
```

Include the local server commands:

```powershell
cd D:\Project\new-blog
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8001
```

State that `site/` is generated output and must not be edited. State that the server is stopped with `Ctrl+C`.

- [ ] **Step 3: 写入三类文章模板和自动生成规则**

Include complete front matter templates for:

```yaml
---
title: 操作系统笔记
author: Tangent丶ZX
date: 2026-07-16
categories:
  - [校内, 笔记, 操作系统]
tags:
  - 笔记
  - 操作系统
---
```

```yaml
---
title: 某某比赛 WP
author: 1so
date: 2026-07-16
categories:
  - [CTF, WP, 比赛名称]
tags:
  - CTF
  - WP
---
```

```yaml
---
title: 一篇随笔
author: Tangent丶ZX
date: 2026-07-16
categories:
  - [随笔, 游记]
tags:
  - 随笔
  - 游记
---
```

Explain that the Hook scans only `*.md` directly under each registered section, sorts newest to oldest, regenerates section `.nav.yml`, section indexes, `docs/archive/categories.md`, and `docs/archive/tags.md`. Explain that editable section introductions must remain outside `<!-- taxonomy:articles:start -->` and `<!-- taxonomy:articles:end -->`.

- [ ] **Step 4: 写入图片、固定页面、语法和样式章节**

Document the image convention and exact syntax:

```markdown
![进程状态图](</images/笔记/操作系统/进程状态图.png>)
```

Map editable pages to exact paths:

- `docs/index.md`
- `docs/about/index.md`
- `docs/links/index.md`
- `docs/study/index.md`
- `docs/ctf/index.md`
- `docs/sth/index.md`
- `docs/.nav.yml`
- `mkdocs.yml`

Include working examples for fenced code, inline code, blockquote, table, `==高亮==`, `~~删除线~~`, admonition, details block and MathJax formula.

Map responsibilities for `article-content.css`, `leftsidebar.css`, `friend-links.css`, `taxonomy.css`, `toc-follow.js`, and `code-fold.js`.

- [ ] **Step 5: 写入新增完整篇章章节**

Use `阅读篇` as the concrete example. Require this directory layout:

```text
docs/reading/
├─ index.md
└─ 某篇读书笔记.md
```

Show these Hook changes:

```python
SECTION_TITLES = {
    "study": "校内篇",
    "ctf": "CTF篇",
    "sth": "杂篇",
    "reading": "阅读篇",
}

SECTION_CATEGORY_ROOTS = {
    "study": "校内",
    "ctf": "CTF",
    "sth": "随笔",
    "reading": "阅读",
}
```

Show the top navigation addition:

```yaml
- 阅读篇: reading
```

Show an article category:

```yaml
categories:
  - [阅读, 小说]
```

Explain that the directory key `reading`, displayed title `阅读篇`, and category root `阅读` serve different roles but must be consistently registered. Require adding taxonomy/content contract tests before publishing the new section.

- [ ] **Step 6: 写入发布、备份、回滚与检查清单**

Use these normal validation and publish commands:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe -m unittest discover -s tests
git status
git add -A
git commit -m "docs: update blog"
git -c http.proxy=http://127.0.0.1:10808 push
```

Document branch responsibilities exactly:

- `main`: MkDocs source
- `gh-pages`: generated site
- `legacy-hexo-source`: old Hexo source backup
- `legacy-hexo-site`: old Hexo generated site backup

State that ordinary updates never edit or force-push `gh-pages`. Describe rollback as a deliberate recovery operation that starts by verifying backup SHAs and Pages settings; do not present a destructive command as a one-line routine.

End with a checkbox list covering front matter, image paths, local preview, strict build, tests, `git status`, commit message, push, Actions result and online verification.

### Task 2: 验证手册准确性且不触碰用户改动

**Files:**
- Verify: `BLOG_MANUAL.md`
- Preserve: `docs/index.md`

**Interfaces:**
- Consumes: Task 1's complete manual.
- Produces: verified Markdown documentation with a clean diff limited to `BLOG_MANUAL.md` plus the user's pre-existing `docs/index.md` modification.

- [ ] **Step 1: 执行内容契约检查**

Run:

```powershell
rg -n "^## (1|2|3|4|5|6|7|8|9|10|11|12|13)\." BLOG_MANUAL.md
rg -n "SECTION_TITLES|SECTION_CATEGORY_ROOTS|legacy-hexo-source|legacy-hexo-site|mkdocs build --strict|unittest discover" BLOG_MANUAL.md
git diff --check -- BLOG_MANUAL.md
```

Expected: all 13 sections and all required operational markers are present; `git diff --check` exits 0.

- [ ] **Step 2: 运行站点验证**

Run:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict --quiet
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Expected: strict build exits 0 and the complete test suite reports `OK`.

- [ ] **Step 3: 验证改动边界**

Run:

```powershell
git status --short
git diff -- BLOG_MANUAL.md
git diff -- docs/index.md
```

Expected: `BLOG_MANUAL.md` is the only new implementation file. `docs/index.md` remains modified exactly as it was before the manual work and is not staged.

- [ ] **Step 4: 提交手册文件**

Run:

```powershell
git add -- BLOG_MANUAL.md
git commit -m "docs: add blog operation manual"
```

Expected: commit contains only `BLOG_MANUAL.md`; `docs/index.md` remains unstaged.

