# TangentZX's Blog MkDocs First Version Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a locally verifiable first version of `TangentZX's Blog` in `D:\Project\new-blog`, modeled on Maple's MkDocs Material structure while keeping `my-blog` unchanged.

**Architecture:** The site uses MkDocs Material with content under `docs/`, theme extensions under `overrides/`, and custom presentation/behavior under `docs/resources/`. Awesome Nav v3 derives navigation from the filesystem and a root `.nav.yml`, so new articles do not require editing `mkdocs.yml`.

**Tech Stack:** Python 3.10+, MkDocs 1.6.1, Material for MkDocs 9.6.20, mkdocs-awesome-nav 3.3.0, Markdown, CSS, vanilla JavaScript, GitHub Actions.

## Global Constraints

- Work only in `D:\Project\new-blog`; treat `D:\Project\my-blog` as read-only.
- Site name is exactly `TangentZX's Blog`; homepage description is exactly `暂无`.
- Top navigation order is exactly `首页 / 校内 / CTF / 随笔 / 友链 / 关于`.
- Use the reference site's Indigo light/dark palette and a One Dark Pro-inspired dark presentation.
- Copy `D:\Project\my-blog\source\头像.png` to `docs/images/avatar.png`; do not rename or modify the source.
- Future article images retain the old `docs/images/<对应分支目录>/` layout and root-relative `/images/...` references.
- First version contains placeholders only; do not migrate old posts, PDFs, or the rest of `source/images`.
- Do not push, deploy, or change the existing GitHub Pages repository.

---

### Task 1: Core MkDocs project, navigation, pages, and avatar

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `mkdocs.yml`
- Create: `docs/.nav.yml`
- Create: `docs/index.md`
- Create: `docs/study/index.md`
- Create: `docs/ctf/index.md`
- Create: `docs/sth/index.md`
- Create: `docs/links/index.md`
- Create: `docs/about/index.md`
- Create: `docs/images/avatar.png`
- Create: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: `D:\Project\my-blog\source\头像.png` as a read-only binary asset.
- Produces: a valid MkDocs source tree; later tasks rely on the CSS/JS paths declared in `mkdocs.yml`.

- [ ] **Step 1: Create the pinned dependency list and write the failing site-contract test**

Create `requirements.txt`:

```text
mkdocs==1.6.1
mkdocs-material==9.6.20
mkdocs-awesome-nav==3.3.0
```

Create `tests/test_site_contract.py`:

```python
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class SiteContractTests(unittest.TestCase):
    def test_dependencies_are_pinned(self):
        self.assertEqual(
            (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines(),
            [
                "mkdocs==1.6.1",
                "mkdocs-material==9.6.20",
                "mkdocs-awesome-nav==3.3.0",
            ],
        )

    def test_mkdocs_identity_and_plugins(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.assertEqual(config["site_name"], "TangentZX's Blog")
        self.assertEqual(config["theme"]["name"], "material")
        self.assertEqual(config["theme"]["custom_dir"], "overrides")
        self.assertEqual(config["plugins"], ["search", "awesome-nav"])
        self.assertTrue(config["strict"])

    def test_root_navigation_order(self):
        nav = yaml.safe_load((ROOT / "docs" / ".nav.yml").read_text(encoding="utf-8"))
        self.assertEqual(
            nav["nav"],
            [
                {"首页": "index.md"},
                {"校内": "study"},
                {"CTF": "ctf"},
                {"随笔": "sth"},
                {"友链": "links"},
                {"关于": "about"},
            ],
        )

    def test_required_pages_exist(self):
        for relative in (
            "docs/index.md",
            "docs/study/index.md",
            "docs/ctf/index.md",
            "docs/sth/index.md",
            "docs/links/index.md",
            "docs/about/index.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_homepage_identity(self):
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", home)
        self.assertIn("暂无", home)
        self.assertIn("images/avatar.png", home)
        self.assertIn("https://github.com/TangentZX", home)

    def test_avatar_is_png(self):
        avatar = ROOT / "docs" / "images" / "avatar.png"
        self.assertGreater(avatar.stat().st_size, 1000)
        self.assertEqual(avatar.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Install dependencies, then run the contract test and verify it fails**

Run:

```powershell
python -m pip install -r requirements.txt
python -m unittest tests.test_site_contract -v
```

Expected: `ERROR` or `FAIL` because `mkdocs.yml`, pages, and avatar do not exist.

- [ ] **Step 3: Create the ignore rules**

Create `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
site/
.cache/
```

- [ ] **Step 4: Create the MkDocs configuration**

Create `mkdocs.yml`:

```yaml
site_name: TangentZX's Blog
site_url: https://tangentzx.github.io/
repo_url: https://github.com/TangentZX/TangentZX.github.io
docs_dir: docs
site_dir: site
use_directory_urls: true
strict: true

theme:
  name: material
  language: zh
  custom_dir: overrides
  logo: images/avatar.png
  favicon: images/avatar.png
  features:
    - content.code.copy
    - content.code.select
    - content.code.annotate
    - navigation.indexes
    - navigation.tabs
    - navigation.top
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: 切换到深色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: 切换到浅色模式

plugins:
  - search
  - awesome-nav

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - pymdownx.details
  - pymdownx.inlinehilite
  - pymdownx.mark
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight:
      anchor_linenums: true
      auto_title: false
      guess_lang: true
      linenums: false
      pygments_lang_class: true
      use_pygments: true

extra_css:
  - resources/css/extra.css
  - resources/css/tittle.css
  - resources/css/read-metrics.css
  - resources/css/leftsidebar.css

extra_javascript:
  - resources/js/mathjax-config.js
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
  - resources/js/read-metrics.js
  - resources/js/sidebar-resize.js
```

- [ ] **Step 5: Create automatic navigation and placeholder pages**

Create `docs/.nav.yml`:

```yaml
nav:
  - 首页: index.md
  - 校内: study
  - CTF: ctf
  - 随笔: sth
  - 友链: links
  - 关于: about
```

Create `docs/index.md`:

```markdown
---
hide:
  - toc
---

<div class="profile-card" markdown>
  <img class="profile-avatar" src="images/avatar.png" alt="TangentZX avatar">

  # TangentZX's Blog

  <p class="profile-description">暂无</p>

  [GitHub](https://github.com/TangentZX){ .md-button .md-button--primary }
</div>
```

Create `docs/study/index.md`:

```markdown
# 校内

校内课程与学习笔记将在这里整理。
```

Create `docs/ctf/index.md`:

```markdown
# CTF

CTF 学习记录与 Writeup 将在这里整理。
```

Create `docs/sth/index.md`:

```markdown
# 随笔

日常记录与思考将在这里整理。
```

Create `docs/links/index.md`:

```markdown
# 友链

友链内容稍后补充。
```

Create `docs/about/index.md`:

```markdown
# 关于

暂无。
```

- [ ] **Step 6: Copy and rename the avatar**

Run:

```powershell
New-Item -ItemType Directory -Force 'D:\Project\new-blog\docs\images'
Copy-Item -LiteralPath 'D:\Project\my-blog\source\头像.png' -Destination 'D:\Project\new-blog\docs\images\avatar.png'
```

Expected: `docs/images/avatar.png` exists and the source file remains unchanged.

- [ ] **Step 7: Rerun the contract test**

Run:

```powershell
python -m unittest tests.test_site_contract -v
```

Expected: all Task 1 tests pass.

- [ ] **Step 8: Commit the core project**

```powershell
git -c safe.directory='D:/Project/new-blog' add .gitignore requirements.txt mkdocs.yml docs tests/test_site_contract.py
git -c safe.directory='D:/Project/new-blog' commit -m "feat: scaffold MkDocs blog"
```

---

### Task 2: Maple-inspired visual layer and progressive JavaScript

**Files:**
- Create: `overrides/main.html`
- Create: `docs/resources/css/extra.css`
- Create: `docs/resources/css/tittle.css`
- Create: `docs/resources/css/read-metrics.css`
- Create: `docs/resources/css/leftsidebar.css`
- Create: `docs/resources/js/mathjax-config.js`
- Create: `docs/resources/js/read-metrics.js`
- Create: `docs/resources/js/sidebar-resize.js`
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: paths already declared by `mkdocs.yml` and Material's `.md-*` DOM classes.
- Produces: readable styling without JavaScript plus optional reading metrics and resizable desktop sidebars.

- [ ] **Step 1: Extend the contract test for theme resources**

Add these methods to `SiteContractTests` in `tests/test_site_contract.py`:

```python
    def test_declared_theme_resources_exist(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        local_resources = [
            path
            for path in config["extra_css"] + config["extra_javascript"]
            if not path.startswith("https://")
        ]
        for relative in local_resources:
            self.assertTrue((ROOT / "docs" / relative).is_file(), relative)

    def test_theme_extension_is_minimal(self):
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
        self.assertIn('{% extends "base.html" %}', template)
        self.assertIn("{{ super() }}", template)

    def test_progressive_enhancement_markers(self):
        metrics = (ROOT / "docs/resources/js/read-metrics.js").read_text(encoding="utf-8")
        resize = (ROOT / "docs/resources/js/sidebar-resize.js").read_text(encoding="utf-8")
        self.assertIn("window.document$", metrics)
        self.assertIn("WORDS_PER_MINUTE = 300", metrics)
        self.assertIn('(pointer: fine)', resize)
        self.assertIn('(min-width: 60em)', resize)
```

- [ ] **Step 2: Run tests and verify the new cases fail**

Run:

```powershell
python -m unittest tests.test_site_contract -v
```

Expected: failures report missing `overrides/main.html`, CSS, and JavaScript files.

- [ ] **Step 3: Add the minimal Material override**

Create `overrides/main.html`:

```jinja
{% extends "base.html" %}

{% block content %}
  {{ super() }}
{% endblock %}
```

- [ ] **Step 4: Add the global and homepage styling**

Create `docs/resources/css/extra.css`:

```css
@import url("https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&display=swap");

:root {
  --page-bg-base: #fcfcfc;
  --content-bg: rgba(255, 255, 255, 0.88);
  --content-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

body {
  background: var(--page-bg-base);
  font-family: "Noto Serif SC", Georgia, "Times New Roman", serif;
}

.md-main { background: transparent; }
.md-grid { max-width: max(85%, 65rem); }

.md-content {
  margin: 0.5rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  background: var(--content-bg);
  box-shadow: var(--content-shadow);
}

.profile-card {
  display: flex;
  min-height: 24rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  text-align: center;
}

.profile-card h1 { margin: 0.2rem 0 0; }
.profile-description { margin: 0; color: var(--md-default-fg-color--light); }

.profile-avatar {
  width: min(12rem, 52vw);
  aspect-ratio: 1;
  border: 0.22rem solid rgba(63, 81, 181, 0.22);
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 14px 35px rgba(63, 81, 181, 0.22);
}

[data-md-color-scheme="slate"] {
  --odp-bg: #282c34;
  --odp-bg-light: #21252b;
  --odp-fg: #abb2bf;
  --odp-blue: #61afef;
  --page-bg-base: var(--odp-bg);
  --content-bg: rgba(33, 37, 43, 0.76);
  --content-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
  --md-default-bg-color: var(--odp-bg);
  --md-default-fg-color: var(--odp-fg);
}

[data-md-color-scheme="slate"] .profile-avatar {
  border-color: rgba(97, 175, 239, 0.35);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.35);
}

@media screen and (max-width: 44.984375em) {
  .md-content { margin: 0; padding: 0.75rem; border-radius: 0; box-shadow: none; }
  .profile-card { min-height: 20rem; }
}
```

- [ ] **Step 5: Add secondary and primary sidebar styling**

Create `docs/resources/css/tittle.css`:

```css
.md-sidebar--secondary .md-nav__link {
  position: relative;
  border-radius: 6px;
  transition: color 0.25s ease, background 0.25s ease, transform 0.2s ease;
}

.md-sidebar--secondary .md-nav__link:hover {
  background: rgba(63, 81, 181, 0.08);
  transform: translateX(3px);
}

.md-sidebar--secondary .md-nav__link--active::before,
.md-sidebar--secondary .md-nav__item--active > .md-nav__link::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: -0.55rem;
  width: 3px;
  border-radius: 2px;
  background: linear-gradient(180deg, #3f51b5, #7986cb);
  content: "";
}
```

Create `docs/resources/css/leftsidebar.css`:

```css
.md-sidebar--primary .md-nav__link {
  border-radius: 6px;
  transition: background 0.25s ease, transform 0.2s ease;
}

.md-sidebar--primary .md-nav__link:hover {
  background: rgba(63, 81, 181, 0.08);
  transform: translateX(4px);
}

.sidebar-resize-handle {
  position: absolute;
  top: 0;
  right: -4px;
  bottom: 0;
  z-index: 3;
  width: 8px;
  cursor: ew-resize;
}

.md-sidebar--secondary .sidebar-resize-handle { right: auto; left: -4px; }

@media screen and (min-width: 76.25em) {
  .md-sidebar--primary,
  .md-sidebar--secondary {
    min-width: 240px;
    max-width: 480px;
  }
}

[data-md-color-scheme="slate"] .md-sidebar .md-nav__link:hover {
  background: rgba(97, 175, 239, 0.08);
}
```

- [ ] **Step 6: Add reading-metrics styling and scripts**

Create `docs/resources/css/read-metrics.css`:

```css
.reading-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 0.75rem;
  margin: 0.45rem 0 1.1rem;
  padding: 0.45rem 0.7rem;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-left: 4px solid var(--md-accent-fg-color);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.7);
  font-size: 0.78rem;
}

.reading-metrics span {
  padding: 0.12rem 0.42rem;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.04);
}

[data-md-color-scheme="slate"] .reading-metrics {
  border-color: rgba(255, 255, 255, 0.08);
  border-left-color: var(--odp-blue);
  background: rgba(40, 44, 52, 0.85);
}
```

Create `docs/resources/js/mathjax-config.js`:

```javascript
window.MathJax = {
  tex: {
    packages: { "[+]": ["ams"] },
    inlineMath: [["$", "$"], ["\\(", "\\)"]],
    displayMath: [["$$", "$$"], ["\\[", "\\]"]]
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"]
  }
};
```

Create `docs/resources/js/read-metrics.js`:

```javascript
(() => {
  const WORDS_PER_MINUTE = 300;

  const buildMetrics = () => {
    const article = document.querySelector("article.md-content__inner");
    if (!article) return;
    article.querySelector(".reading-metrics")?.remove();

    const text = article.innerText || "";
    const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const latin = (text.match(/[A-Za-z0-9]+/g) || []).length;
    const words = cjk + latin;
    if (!words) return;

    const metrics = document.createElement("div");
    metrics.className = "reading-metrics";
    metrics.innerHTML = `<span>阅读时长 ${Math.max(1, Math.ceil(words / WORDS_PER_MINUTE))} 分钟</span><span>字数 ${words}</span>`;
    const heading = article.querySelector("h1");
    heading?.insertAdjacentElement("afterend", metrics);
  };

  if (window.document$?.subscribe) window.document$.subscribe(buildMetrics);
  else document.addEventListener("DOMContentLoaded", buildMetrics);
})();
```

Create `docs/resources/js/sidebar-resize.js`:

```javascript
(() => {
  const MIN_WIDTH = 240;
  const MAX_WIDTH = 480;
  const isDesktop = () =>
    window.matchMedia("(pointer: fine)").matches &&
    window.matchMedia("(min-width: 60em)").matches;

  const setup = (sidebar, direction) => {
    const handle = document.createElement("div");
    handle.className = "sidebar-resize-handle";
    sidebar.appendChild(handle);

    handle.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      const startX = event.clientX;
      const startWidth = sidebar.getBoundingClientRect().width;
      document.body.style.userSelect = "none";

      const move = (moveEvent) => {
        const delta = moveEvent.clientX - startX;
        const requested = startWidth + (direction === "left" ? delta : -delta);
        const width = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, requested));
        sidebar.style.width = `${width}px`;
        sidebar.style.flexBasis = `${width}px`;
      };
      const stop = () => {
        document.removeEventListener("pointermove", move);
        document.removeEventListener("pointerup", stop);
        document.body.style.userSelect = "";
      };
      document.addEventListener("pointermove", move);
      document.addEventListener("pointerup", stop);
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    if (!isDesktop()) return;
    const primary = document.querySelector(".md-sidebar--primary");
    const secondary = document.querySelector(".md-sidebar--secondary");
    if (primary) setup(primary, "left");
    if (secondary) setup(secondary, "right");
  });
})();
```

- [ ] **Step 7: Run the contract tests**

Run:

```powershell
python -m unittest tests.test_site_contract -v
```

Expected: all tests pass.

- [ ] **Step 8: Commit the visual layer**

```powershell
git -c safe.directory='D:/Project/new-blog' add overrides docs/resources tests/test_site_contract.py
git -c safe.directory='D:/Project/new-blog' commit -m "feat: add Maple-inspired theme customizations"
```

---

### Task 3: Strict build contract and deployment template

**Files:**
- Create: `.github/workflows/deploy.yml`
- Create: `tests/test_built_site.py`
- Modify: `tests/test_site_contract.py`

**Interfaces:**
- Consumes: complete source tree from Tasks 1–2.
- Produces: a strict `site/` build and a dormant deployment workflow that activates only after a future push to `main`.

- [ ] **Step 1: Add deployment-template assertions**

Add this method to `SiteContractTests`:

```python
    def test_deployment_template_is_safe_and_pinned(self):
        workflow = (ROOT / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
        self.assertIn("branches: [main]", workflow)
        self.assertIn('python-version: "3.13"', workflow)
        self.assertIn("pip install -r requirements.txt", workflow)
        self.assertIn("mkdocs gh-deploy --strict --force", workflow)
```

- [ ] **Step 2: Run the contract test and verify it fails**

Run:

```powershell
python -m unittest tests.test_site_contract.SiteContractTests.test_deployment_template_is_safe_and_pinned -v
```

Expected: `ERROR` because `.github/workflows/deploy.yml` does not exist.

- [ ] **Step 3: Create the deployment template**

Create `.github/workflows/deploy.yml`:

```yaml
name: deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Deploy
        run: mkdocs gh-deploy --strict --force
```

- [ ] **Step 4: Write a failing generated-site test**

Create `tests/test_built_site.py`:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class BuiltSiteTests(unittest.TestCase):
    def test_expected_pages_are_built(self):
        for relative in (
            "index.html",
            "study/index.html",
            "ctf/index.html",
            "sth/index.html",
            "links/index.html",
            "about/index.html",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

    def test_homepage_contains_identity_and_assets(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", html)
        self.assertIn("暂无", html)
        self.assertIn("images/avatar.png", html)
        self.assertIn("resources/css/extra.css", html)
        self.assertIn("resources/js/read-metrics.js", html)

    def test_navigation_labels_are_rendered(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        for label in ("首页", "校内", "CTF", "随笔", "友链", "关于"):
            self.assertIn(label, html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 5: Verify the generated-site test fails before building**

Run:

```powershell
Test-Path site
python -m unittest tests.test_built_site -v
```

Expected: `Test-Path` prints `False`, then tests fail because `site/` does not exist.

- [ ] **Step 6: Build strictly and rerun all tests**

Run:

```powershell
python -m mkdocs build --strict
python -m unittest discover -s tests -v
```

Expected: MkDocs reports `Documentation built` with exit code 0; all tests pass.

- [ ] **Step 7: Verify the old blog remained untouched**

Run:

```powershell
Get-Item 'D:\Project\my-blog\source\头像.png' | Select-Object FullName, Length, LastWriteTime
git -c safe.directory='D:/Project/new-blog' status --short --branch
```

Expected: only `new-blog` changes are reported; the source avatar still exists.

- [ ] **Step 8: Commit build checks and workflow**

```powershell
git -c safe.directory='D:/Project/new-blog' add .github/workflows/deploy.yml tests/test_site_contract.py tests/test_built_site.py
git -c safe.directory='D:/Project/new-blog' commit -m "ci: add strict build and deployment template"
```

---

### Task 4: Browser-based desktop and mobile visual verification

**Files:**
- Modify only if visual defects are found: `docs/resources/css/*.css`, `docs/resources/js/*.js`, `docs/index.md`
- Verify: generated pages under `site/`

**Interfaces:**
- Consumes: successful strict build from Task 3.
- Produces: verified desktop/mobile behavior; no new feature surface.

- [ ] **Step 1: Start the local preview server**

Run:

```powershell
python -m mkdocs serve --strict --dev-addr 127.0.0.1:8000
```

Expected: `Serving on http://127.0.0.1:8000/` and no build warnings.

- [ ] **Step 2: Verify the desktop layout at 1440×900**

Open `http://127.0.0.1:8000/` and verify:

- six navigation tabs appear in the approved order;
- avatar is circular and not distorted;
- content card does not overlap either sidebar;
- light/dark toggle changes palette;
- both sidebars can be resized between 240px and 480px;
- search opens and accepts input.

Expected: all checks pass without horizontal scrolling.

- [ ] **Step 3: Verify the mobile layout at 390×844**

Verify:

- navigation collapses into Material's drawer;
- resize handles are absent;
- avatar and buttons fit the viewport;
- content has no clipped text or horizontal overflow.

Expected: all checks pass.

- [ ] **Step 4: Verify progressive features on an inner page**

Open `/ctf/` and verify the reading metrics appear below the `h1`; inspect the page with JavaScript disabled and confirm the article and navigation remain readable.

Expected: JavaScript adds metrics when enabled, while core content remains usable when disabled.

- [ ] **Step 5: Apply only evidence-based visual fixes and rerun verification**

For each observed defect, make the smallest CSS/JS change, then run:

```powershell
python -m mkdocs build --strict
python -m unittest discover -s tests -v
```

Expected: build and tests pass after every fix.

- [ ] **Step 6: Commit visual QA fixes, if any**

```powershell
git -c safe.directory='D:/Project/new-blog' add docs/resources docs/index.md
git -c safe.directory='D:/Project/new-blog' diff --cached --quiet
```

If the previous command exits with code 1 because fixes are staged, run:

```powershell
git -c safe.directory='D:/Project/new-blog' commit -m "fix: polish responsive blog layout"
```

- [ ] **Step 7: Record final evidence**

Run:

```powershell
git -c safe.directory='D:/Project/new-blog' status --short --branch
git -c safe.directory='D:/Project/new-blog' log --oneline -5
python -m mkdocs build --strict
python -m unittest discover -s tests -v
```

Expected: clean working tree, strict build exit code 0, and all tests pass.
