# 页面阅读统计开关实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 让任意 Markdown 页面可以在 Front Matter 的 `hide` 列表中加入 `read-metrics`，从而关闭该页的阅读时长和字数统计。

**架构：** 独立 MkDocs hook 把页面元数据转换为正文中的隐藏标记，前端统计脚本识别标记后退出。Python 单元测试验证元数据转换，集成契约测试验证 hook 注册、首页配置和脚本守卫均已接通。

**技术栈：** Python 3.10、MkDocs hooks、标准库 `unittest`、JavaScript、Material for MkDocs。

## 全局约束

- 页面开关写法固定为 `hide` 列表中的 `read-metrics`。
- `hide` 缺失、为空或不包含 `read-metrics` 时继续显示统计。
- 兼容 `hide: read-metrics` 字符串形式。
- 禁用页面在首次加载和 Material 即时导航后都不得残留统计节点。
- 不修改 Material 主题模板，不根据 URL 判断页面，不新增第三方依赖。
- 首页保留已有的 `toc` 隐藏项。

---

### 任务 1：页面元数据转换 hook

**文件：**

- 新建：`hooks/read_metrics.py`
- 新建：`tests/test_read_metrics_hook.py`

**接口：**

- 产出：`on_page_content(html, page, config, files, **kwargs) -> str`。
- 产出：禁用标记常量 `MARKER = '<span data-read-metrics="hidden" hidden></span>'`。
- 使用：MkDocs 页面对象的 `page.meta["hide"]`。

- [ ] **步骤 1：编写失败的 hook 单元测试**

新建 `tests/test_read_metrics_hook.py`：

```python
from types import SimpleNamespace
import unittest

from hooks.read_metrics import MARKER, on_page_content


class ReadMetricsHookTests(unittest.TestCase):
    def render(self, hide=None):
        meta = {} if hide is None else {"hide": hide}
        page = SimpleNamespace(meta=meta)
        return on_page_content("<p>正文</p>", page, None, None)

    def test_keeps_html_unchanged_without_switch(self):
        self.assertEqual(self.render(), "<p>正文</p>")
        self.assertEqual(self.render(["toc"]), "<p>正文</p>")

    def test_prepends_marker_for_list_switch(self):
        self.assertEqual(
            self.render(["toc", "read-metrics"]),
            f"{MARKER}\n<p>正文</p>",
        )

    def test_accepts_string_switch(self):
        self.assertEqual(
            self.render("read-metrics"),
            f"{MARKER}\n<p>正文</p>",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **步骤 2：运行测试并确认因模块缺失而失败**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_read_metrics_hook -v
```

预期：`ERROR`，错误包含 `No module named 'hooks.read_metrics'`。

- [ ] **步骤 3：实现最小 hook**

新建 `hooks/read_metrics.py`：

```python
from __future__ import annotations


MARKER = '<span data-read-metrics="hidden" hidden></span>'


def _hidden_features(page) -> set[str]:
    value = (getattr(page, "meta", None) or {}).get("hide", [])
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    return set()


def on_page_content(html, page, config, files, **kwargs):
    if "read-metrics" not in _hidden_features(page):
        return html
    return f"{MARKER}\n{html}"
```

- [ ] **步骤 4：运行 hook 测试并确认通过**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_read_metrics_hook -v
```

预期：运行 3 个测试，结果为 `OK`。

---

### 任务 2：接通页面配置与前端脚本

**文件：**

- 新建：`tests/test_read_metrics_integration.py`
- 修改：`mkdocs.yml:43-45`
- 修改：`docs/resources/js/read-metrics.js:4-9`
- 修改：`docs/index.md:1-4`

**接口：**

- 使用：任务 1 生成的 `[data-read-metrics="hidden"]` 标记。
- 产出：注册到 MkDocs 的 `hooks/read_metrics.py`。
- 产出：`read-metrics.js` 中在统计计算前执行的页面级守卫。

- [ ] **步骤 1：编写失败的集成契约测试**

新建 `tests/test_read_metrics_integration.py`：

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadMetricsIntegrationTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_hook_is_registered(self):
        self.assertIn("- hooks/read_metrics.py", self.read("mkdocs.yml"))

    def test_homepage_disables_metrics(self):
        front_matter = self.read("docs/index.md").split("---", 2)[1]
        self.assertIn("- read-metrics", front_matter)

    def test_script_honors_hidden_marker(self):
        script = self.read("docs/resources/js/read-metrics.js")
        self.assertIn(
            'article.querySelector(\'[data-read-metrics="hidden"]\')',
            script,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **步骤 2：运行集成契约测试并确认失败**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest tests.test_read_metrics_integration -v
```

预期：3 个测试均失败，分别指出 hook 未注册、首页缺少开关和脚本缺少守卫。

- [ ] **步骤 3：注册 hook**

把 `mkdocs.yml` 的 hooks 配置改为：

```yaml
hooks:
  - hooks/taxonomy.py
  - hooks/read_metrics.py
```

- [ ] **步骤 4：让前端脚本识别禁用标记**

在 `docs/resources/js/read-metrics.js` 删除旧 `.reading-metrics` 节点之后、读取正文文本之前加入：

```javascript
    if (article.querySelector('[data-read-metrics="hidden"]')) return;
```

- [ ] **步骤 5：在首页启用开关**

把 `docs/index.md` 的 Front Matter 改为：

```yaml
---
hide:
  - toc
  - read-metrics
---
```

不要改动该文件现有的壁纸、标题、简介或 GitHub 按钮。

- [ ] **步骤 6：运行全部阅读统计测试**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_read_metrics*.py" -v
```

预期：运行 6 个测试，结果为 `OK`。

---

### 任务 3：构建与浏览器验收

**文件：**

- 验证：`site/index.html`
- 验证：本地实时预览 `http://127.0.0.1:8001/`

**接口：**

- 使用：任务 1 的 hook 和任务 2 的页面配置、前端守卫。
- 产出：可构建、可在即时导航中正确切换的页面统计行为。

- [ ] **步骤 1：执行严格构建**

运行：

```powershell
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict
```

预期：命令状态码为 `0`，输出包含 `Documentation built`。

- [ ] **步骤 2：检查生成的首页标记**

运行：

```powershell
rg -n "data-read-metrics=.hidden.|reading-metrics" site/index.html
```

预期：找到 `data-read-metrics="hidden"`，生成的静态 HTML 中没有 `.reading-metrics` 节点；后者由 JavaScript 运行时生成。

- [ ] **步骤 3：实时浏览器验收**

在 `http://127.0.0.1:8001/` 检查首页，确认没有“阅读时长”和“字数”。再打开任一未配置 `read-metrics` 的普通文章，确认仍显示两项统计；通过站内即时导航在两页间往返，确认统计不会残留或错误消失。

- [ ] **步骤 4：检查改动质量**

运行：

```powershell
git diff --check
git status --short
```

预期：`git diff --check` 状态码为 `0`；`git status --short` 只列出本功能文件、之前已知的首页壁纸文件和计划文档，不出现无关改动。
