# TangentZX's Blog：MkDocs 首版设计

## 目标

在 `D:\Project\new-blog` 中建立独立的 MkDocs Material 博客首版。站点借鉴 Maple 博客的文档式三栏布局、Indigo 明暗配色和内容组织方式，但使用 TangentZX 自己的名称、头像、栏目与内容。

本阶段只搭建站点框架和首页，不迁移旧博客文章，不部署或覆盖现有 GitHub Pages。

## 已确认的站点信息

- 站点名：`TangentZX's Blog`
- 首页简介：`暂无`
- 顶部导航：`首页 / 校内 / CTF / 随笔 / 友链 / 关于`
- 主题：Material for MkDocs
- 配色：沿用 Maple 博客的 Indigo 主色与强调色，支持浅色和深色模式切换
- 头像来源：`D:\Project\my-blog\source\头像.png`
- 头像目标：`docs/images/avatar.png`

## 实现方案

采用“Maple 风格目录与视觉定制 + 自动导航”的方案。

站点保留 Maple 项目使用的 `docs/resources/css`、`docs/resources/js`、`overrides` 和按栏目分目录的组织方式。与 Maple 手工维护完整 `nav` 不同，新站使用 `mkdocs-awesome-nav`，根据文件结构自动发现文章，并用根级 `.nav.yml` 固定顶栏顺序和中文栏目名。

该方案在外观上接近参考站点，同时避免每新增一篇文章都修改 `mkdocs.yml`。

## 目录结构

```text
new-blog/
├── .gitignore
├── mkdocs.yml
├── requirements.txt
├── overrides/
│   └── main.html
├── docs/
│   ├── .nav.yml
│   ├── index.md
│   ├── images/
│   │   └── avatar.png
│   ├── resources/
│   │   ├── css/
│   │   │   ├── extra.css
│   │   │   ├── tittle.css
│   │   │   ├── read-metrics.css
│   │   │   └── leftsidebar.css
│   │   └── js/
│   │       ├── mathjax-config.js
│   │       ├── read-metrics.js
│   │       └── sidebar-resize.js
│   ├── study/
│   │   └── index.md
│   ├── ctf/
│   │   └── index.md
│   ├── sth/
│   │   └── index.md
│   ├── links/
│   │   └── index.md
│   └── about/
│       └── index.md
└── .github/
    └── workflows/
        └── deploy.yml
```

栏目映射：

| 导航名称 | 内容目录 |
| --- | --- |
| 首页 | `docs/index.md` |
| 校内 | `docs/study/` |
| CTF | `docs/ctf/` |
| 随笔 | `docs/sth/` |
| 友链 | `docs/links/` |
| 关于 | `docs/about/` |

## 页面与视觉组件

首页展示圆形头像、站点名称、简介“暂无”和 GitHub 入口。其余五个栏目在首版中提供简洁占位页，后续迁移内容时再逐步扩展。

首版保留或重新实现以下参考站点特征：

- Material 三栏布局与顶部标签导航
- Indigo 浅色/深色配色
- One Dark Pro 风格的深色内容区域与代码展示
- 中文正文字体和卡片式内容区域
- 左右侧栏的层级、悬停与当前项样式
- 桌面端可拖动调整侧栏宽度
- 文章阅读时长与字数统计
- MathJax 公式支持
- 搜索和代码复制
- `overrides/main.html` 模板扩展入口

自定义实现只借鉴参考站点的视觉行为并按本站需求整理，不复制参考站点的文章、身份信息或个人资源。

## 图片与静态资源规则

旧博客的文章配图结构保持不变。后续迁移时：

```text
D:\Project\my-blog\source\images\<对应分支目录>\配图.png
```

复制为：

```text
D:\Project\new-blog\docs\images\<对应分支目录>\配图.png
```

文章继续使用根路径引用，例如：

```markdown
![说明](/images/CTF/WP/WHUCTF2026/配图.png)
```

头像是例外：从旧站根目录复制后统一命名为 `docs/images/avatar.png`。PDF 后续迁移时使用 `docs/pdfs/` 并保留原有子目录结构。

## 新增文章流程

自动导航根据目录发现页面。新增 CTF 文章时，只需创建：

```text
docs/ctf/<分支>/<文章名>/index.md
docs/images/CTF/<分支>/<相关图片>.png
```

通常不需要修改 `mkdocs.yml`。只有需要调整显示名称、顺序或隐藏页面时，才修改对应目录的 `.nav.yml`。

## 配置与依赖

`requirements.txt` 固定 MkDocs、Material for MkDocs 和 `mkdocs-awesome-nav` 的兼容版本，避免依赖自动升级造成样式或行为变化。

`mkdocs.yml` 负责：

- 站点名称与基础 URL
- Material 主题及 `overrides` 路径
- Indigo 明暗调色板
- 导航标签、返回顶部、代码复制等主题功能
- Markdown 扩展与 MathJax
- 搜索、自动导航插件
- 自定义 CSS 和 JavaScript 资源

## 错误处理与兼容性

- 构建时启用严格检查，尽早发现无效配置、缺失页面和链接警告。
- CSS 和 JavaScript 功能采用渐进增强；脚本未加载时，正文、导航与基本阅读仍可使用。
- 侧栏拖动仅在具备精确指针且屏幕足够宽的桌面环境启用。
- 移动端使用 Material 原生抽屉式导航，不强制应用桌面侧栏宽度。
- 根路径图片引用以用户主页域名部署为目标；若未来改为项目子路径部署，需要统一调整资源 URL 策略。

## 验证

首版完成后执行以下检查：

1. 安装锁定依赖并执行严格构建。
2. 确认六个顶栏入口均能访问。
3. 确认 `avatar.png` 正常显示。
4. 确认浅色和深色模式正确切换。
5. 确认左右侧栏、阅读统计、搜索、代码复制与 MathJax 正常。
6. 本地预览桌面端和移动端布局，检查溢出、遮挡和导航可用性。
7. 确认 `my-blog` 未发生任何修改。

## 部署边界

首版提供 `.github/workflows/deploy.yml` 模板，用于未来从源码分支构建并发布到 `gh-pages`。本阶段不连接远程仓库、不推送、不部署，也不覆盖现有 Hexo 博客。

