# 页面阅读统计开关设计

## 目标

允许任意 Markdown 页面通过 Front Matter 关闭“阅读时长”和“字数”统计。页面作者只需在 `hide` 列表中加入 `read-metrics`：

```yaml
---
hide:
  - read-metrics
---
```

首页同时保留已有的 `toc` 隐藏项。

## 方案

新增独立的 MkDocs hook `hooks/read_metrics.py`。构建每个页面正文时，hook 检查 `page.meta.hide`：包含 `read-metrics` 时，在生成的正文 HTML 前加入无可见内容的 `data-read-metrics="hidden"` 标记；未配置时保持正文不变。

`docs/resources/js/read-metrics.js` 在删除旧统计节点后检查该标记。标记存在时立即结束，不计算字数，也不插入统计节点。这样同时兼容首次加载和 Material 的即时导航重新渲染。

这一方案不修改 Material 主题模板，不依赖页面 URL，也不把阅读统计职责混入现有分类 hook。

## 文件职责

- `hooks/read_metrics.py`：把页面级 Front Matter 配置转换为生成 HTML 中的机器可读标记。
- `mkdocs.yml`：注册新的阅读统计 hook。
- `docs/resources/js/read-metrics.js`：识别禁用标记并跳过统计生成。
- `docs/index.md`：为首页添加 `read-metrics` 隐藏项。
- `tests/test_read_metrics_hook.py`：验证配置存在和不存在时 hook 的输出。

## 边界行为

- `hide` 缺失、为空或不包含 `read-metrics`：继续显示统计。
- `hide` 包含 `read-metrics`：不显示阅读时长和字数。
- hook 接受列表形式，也兼容字符串形式的 `hide: read-metrics`。
- 页面切换后脚本先删除可能残留的旧统计节点，再判断当前页面是否禁用，避免即时导航残留。

## 验证

先用单元测试验证 hook 的标记注入行为，再运行 MkDocs 严格构建。检查生成的首页包含禁用标记且没有 `.reading-metrics`；再检查一个未禁用页面仍由脚本正常生成统计。最后在本地实时预览中确认首页不显示统计，普通文章仍显示统计。
