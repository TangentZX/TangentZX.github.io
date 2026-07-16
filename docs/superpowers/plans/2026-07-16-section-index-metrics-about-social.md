# 入口页统计关闭与关于页社交按钮实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 关闭 7 个入口页的阅读统计，并在关于页加入带 GitHub、Bilibili 内置图标的品牌按钮。

**架构：** 所有入口页复用现有 `hide: read-metrics` 页面开关。Material 的 Emoji 扩展把 `simple` 图标短代码渲染为内联 SVG，关于页专属 CSS 负责按钮布局和品牌配色。

**技术栈：** MkDocs、Material for MkDocs、Python 标准库 `unittest`、Python Markdown、Pymdown Extensions、HTML、CSS。

## 全局约束

- 入口页范围固定为首页、校内篇、CTF 篇、杂篇、归档、友链、关于。
- 首页已有的 `toc` 和 `read-metrics` 配置必须保留。
- 归档页已有的 `title: 归档` 必须保留。
- 不修改分类 hook 自动生成块内的内容。
- 关于页当前未提交的个人信息修改必须保留。
- 删除列表形式的 GitHub 行，只保留下方社交按钮。
- GitHub 使用 `https://github.com/TangentZX`。
- Bilibili 使用 `https://space.bilibili.com/670950385`，不带跟踪参数。
- 两个按钮均在新标签页打开并设置 `rel="noopener noreferrer"`。
- 图标使用 Material 内置 `simple` 图标，不新增图片或手写 SVG。

---

### 任务 1：关闭全部入口页阅读统计

**文件：**

- 修改：`tests/test_read_metrics_integration.py`
- 修改：`docs/study/index.md:1`
- 修改：`docs/ctf/index.md:1`
- 修改：`docs/sth/index.md:1`
- 修改：`docs/archive/index.md:1-4`
- 修改：`docs/links/index.md:1`
- 修改：`docs/about/index.md:1`
- 验证：`docs/index.md:1-5`

**接口：**

- 使用：现有 `hooks/read_metrics.py` 支持的 `hide` 列表项 `read-metrics`。
- 产出：7 个入口页都在 Front Matter 中声明 `read-metrics`。

- [ ] **步骤 1：编写失败的入口页配置测试**

在 `tests/test_read_metrics_integration.py` 中加入常量：

```python
INDEX_PAGES = (
    "docs/index.md",
    "docs/study/index.md",
    "docs/ctf/index.md",
    "docs/sth/index.md",
    "docs/archive/index.md",
    "docs/links/index.md",
    "docs/about/index.md",
)
```

用下面的测试替换现有 `test_homepage_disables_metrics`：

```python
    def test_section_index_pages_disable_metrics(self):
        for relative_path in INDEX_PAGES:
            with self.subTest(path=relative_path):
                source = self.read(relative_path)
                self.assertTrue(source.startswith("---\n"))
                front_matter = source.split("---", 2)[1]
                self.assertIn("- read-metrics", front_matter)
```

- [ ] **步骤 2：运行测试并确认红灯**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_read_metrics_integration -v
```

预期：`test_section_index_pages_disable_metrics` 对尚未配置的 6 个入口页失败；首页子测试通过。

- [ ] **步骤 3：为没有 Front Matter 的入口页添加配置**

在 `docs/study/index.md`、`docs/ctf/index.md`、`docs/sth/index.md`、`docs/links/index.md`、`docs/about/index.md` 顶部加入：

```yaml
---
hide:
  - read-metrics
---

```

不得改动这些文件后续已有内容；尤其不要改写 `taxonomy:articles` 标记之间的自动生成内容。

- [ ] **步骤 4：更新归档页 Front Matter**

把 `docs/archive/index.md` 的 Front Matter 改为：

```yaml
---
title: 归档
hide:
  - read-metrics
---
```

- [ ] **步骤 5：运行入口页配置测试并确认绿灯**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_read_metrics_integration -v
```

预期：该文件中的全部测试通过。

---

### 任务 2：内置图标与关于页社交按钮

**文件：**

- 新建：`tests/test_about_social.py`
- 修改：`mkdocs.yml:47-83`
- 修改：`docs/about/index.md`
- 新建：`docs/resources/css/about.css`

**接口：**

- 使用：`:simple-github:` 和 `:simple-bilibili:` 图标短代码。
- 产出：`.about-actions`、`.about-button`、`.about-button--github`、`.about-button--bilibili` CSS 类。
- 产出：Material Emoji 扩展与 `about.css` 配置。

- [ ] **步骤 1：编写失败的社交按钮契约测试**

新建 `tests/test_about_social.py`：

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AboutSocialTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_material_emoji_and_about_css_are_registered(self):
        config = self.read("mkdocs.yml")
        self.assertIn("- pymdownx.emoji:", config)
        self.assertIn("material.extensions.emoji.twemoji", config)
        self.assertIn("material.extensions.emoji.to_svg", config)
        self.assertIn("- resources/css/about.css", config)

    def test_about_page_contains_social_buttons(self):
        page = self.read("docs/about/index.md")
        self.assertNotIn("- **GitHub：**", page)
        self.assertIn(":simple-github: GitHub", page)
        self.assertIn("https://github.com/TangentZX", page)
        self.assertIn(":simple-bilibili: Bilibili", page)
        self.assertIn("https://space.bilibili.com/670950385", page)
        self.assertNotIn("spm_id_from", page)
        self.assertEqual(page.count('target="_blank"'), 2)
        self.assertEqual(page.count('rel="noopener noreferrer"'), 2)

    def test_about_button_styles_exist(self):
        css = self.read("docs/resources/css/about.css")
        for class_name in (
            ".about-actions",
            ".about-button",
            ".about-button--github",
            ".about-button--bilibili",
        ):
            with self.subTest(class_name=class_name):
                self.assertIn(class_name, css)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **步骤 2：运行测试并确认红灯**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_about_social -v
```

预期：3 个测试因 Emoji/CSS 未注册、按钮不存在和 `about.css` 文件不存在而失败或报错。

- [ ] **步骤 3：启用 Material 内置图标并注册样式**

在 `mkdocs.yml` 的 `markdown_extensions` 中加入：

```yaml
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
```

在 `extra_css` 列表中加入：

```yaml
  - resources/css/about.css
```

- [ ] **步骤 4：在关于页加入按钮**

确认 `docs/about/index.md` 中不存在 `- **GitHub：**` 行。在现有个人信息列表后加入：

```markdown
<div class="about-actions" markdown>

[:simple-github: GitHub](https://github.com/TangentZX){ .md-button .about-button .about-button--github target="_blank" rel="noopener noreferrer" }
[:simple-bilibili: Bilibili](https://space.bilibili.com/670950385){ .md-button .about-button .about-button--bilibili target="_blank" rel="noopener noreferrer" }

</div>
```

保留关于页其余个人信息原样。

- [ ] **步骤 5：创建关于页专属样式**

新建 `docs/resources/css/about.css`：

```css
.about-actions {
  margin-top: 1.5rem;
}

.about-actions p {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin: 0;
}

.about-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  border: 0;
  color: #fff !important;
}

.about-button .twemoji {
  width: 1.1em;
  height: 1.1em;
}

.about-button--github {
  background: #24292f;
}

.about-button--github:hover,
.about-button--github:focus {
  background: #57606a;
}

.about-button--bilibili {
  background: #fb7299;
}

.about-button--bilibili:hover,
.about-button--bilibili:focus {
  background: #e85b88;
}
```

- [ ] **步骤 6：运行全部相关测试**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

预期：阅读统计与关于页社交按钮测试全部通过。

---

### 任务 3：构建与实时页面验收

**文件：**

- 验证：`site/index.html`
- 验证：`site/about/index.html`
- 验证：`http://127.0.0.1:8001/`

**接口：**

- 使用：任务 1 的入口页开关和任务 2 的图标、按钮、样式。
- 产出：7 个入口页不显示统计，关于页按钮在桌面和移动端正确渲染。

- [ ] **步骤 1：执行严格构建**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict
```

预期：状态码为 `0`，输出包含 `Documentation built`。

- [ ] **步骤 2：检查生成产物**

运行：

```powershell
rg -n "data-read-metrics=.hidden." site/index.html site/study/index.html site/ctf/index.html site/sth/index.html site/archive/index.html site/links/index.html site/about/index.html
rg -n "twemoji|github.com/TangentZX|space.bilibili.com/670950385|about-button" site/about/index.html
```

预期：第一条命令在 7 个文件中各找到禁用标记；第二条命令找到两个 SVG 图标、两个链接和按钮类。

- [ ] **步骤 3：实时浏览器验收**

在 `http://127.0.0.1:8001/` 依次检查 7 个入口页，确认没有 `.reading-metrics`。在关于页确认两个按钮均包含 SVG 图标和文字，链接地址、`target`、`rel` 正确；把视口缩到手机宽度，确认按钮自动换行且页面没有横向溢出。

- [ ] **步骤 4：检查工作区质量**

运行：

```powershell
git diff --check
git status --short
```

预期：差异检查状态码为 `0`；状态中仅包含本功能文件、用户已有的关于页修改和本实施计划，不出现无关文件。
