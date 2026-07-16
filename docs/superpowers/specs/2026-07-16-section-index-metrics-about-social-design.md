# 入口页统计关闭与关于页社交按钮设计

## 目标

关闭站点 7 个入口页的阅读时长和字数统计，并在“关于”页加入带品牌图标的 GitHub、Bilibili 按钮。

## 入口页阅读统计

以下页面在 Front Matter 的 `hide` 列表中加入 `read-metrics`：

- `docs/index.md`
- `docs/study/index.md`
- `docs/ctf/index.md`
- `docs/sth/index.md`
- `docs/archive/index.md`
- `docs/links/index.md`
- `docs/about/index.md`

首页已经包含该配置，只验证并保留。其余页面若没有 Front Matter，则在文件顶部新增；已有 Front Matter 的归档页保留 `title`。自动生成的分类内容块不做改动。

## 图标支持

在 `mkdocs.yml` 中启用 `pymdownx.emoji`，使用 Material for MkDocs 提供的 Twemoji 索引和 SVG 生成器。按钮直接使用内置的 `:simple-github:` 与 `:simple-bilibili:` 图标，不新增图片或手写 SVG。

## 关于页按钮

删除个人信息列表中原有的 GitHub 文本链接，避免重复。列表下方新增一个按钮容器，其中包含：

- GitHub：链接到 `https://github.com/TangentZX`，使用 GitHub 图标和深色品牌样式。
- Bilibili：链接到 `https://space.bilibili.com/670950385`，使用 Bilibili 图标和粉色品牌样式。

两个按钮均显示“图标 + 文字”，在新标签页打开，并设置 `rel="noopener noreferrer"`。桌面端横向排列，空间不足时自动换行；图标尺寸与文字协调，亮暗主题下保持足够对比度。

## 样式组织

新增 `docs/resources/css/about.css`，只负责关于页社交按钮的布局和品牌样式，并在 `mkdocs.yml` 的 `extra_css` 中注册。现有全局样式文件不混入页面专属规则。

## 验证

- 自动化测试检查 7 个入口页均包含 `read-metrics`。
- 自动化测试检查 Emoji 扩展与 `about.css` 已注册。
- 自动化测试检查关于页不再包含列表形式的 GitHub 行，并包含两个正确、安全的社交链接及图标。
- MkDocs 严格构建必须通过。
- 在 `http://127.0.0.1:8001/` 验证入口页不显示统计；关于页两个图标正常渲染、按钮可见、链接属性正确，移动端布局无横向溢出。
