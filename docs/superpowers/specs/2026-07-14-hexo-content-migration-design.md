# Hexo 内容迁移到 MkDocs 设计

## 目标

将 `D:\Project\my-blog` 中现有的 9 篇 Hexo 文章及 `source/images` 下的 131 张图片复制到 `D:\Project\new-blog`，使文章自然归入“校内 / CTF / 随笔”栏目，并能由 MkDocs Material 严格构建。旧博客目录保持不变，本阶段不推送 GitHub。

## 迁移策略

采用“忠实迁移并做兼容修正”：保留文章标题、原 Markdown 正文、发布日期、作者、分类、标签、中文文件名以及图片目录结构，只修改 MkDocs 解析所必需的内容。

不进行英文 slug 重命名，不重新压缩或转换图片，不改写文章内容，不引入新的发布插件。

## 文章映射

### CTF

- `source/_posts/Tzxy's WHUCTF2025新生赛WP.md` → `docs/ctf/Tzxy's WHUCTF2025新生赛WP.md`
- `source/_posts/WHUCTF2026_WP.md` → `docs/ctf/WHUCTF2026_WP.md`

### 校内

- `source/_posts/程序设计(A)(C)作业.md` → `docs/study/程序设计(A)(C)作业.md`
- `source/_posts/线性代数-矩阵笔记.md` → `docs/study/线性代数-矩阵笔记.md`
- `source/_posts/数据结构复习整理.md` → `docs/study/数据结构复习整理.md`
- `source/_posts/数据结构实验复习.md` → `docs/study/数据结构实验复习.md`

### 随笔

- `source/_posts/ArchLinux 折腾心得.md` → `docs/sth/ArchLinux 折腾心得.md`
- `source/_posts/流光协奏之梦.md` → `docs/sth/流光协奏之梦.md`
- `source/_posts/郑州强网论坛 学习心得.md` → `docs/sth/郑州强网论坛 学习心得.md`

## 图片迁移

将 `my-blog/source/images` 的所有子目录和文件复制到 `new-blog/docs/images`，保留 `CTF`、`reward`、`程序设计(A)(C)`、`笔记`、`随便写写` 等原始层级。现有 `docs/images/avatar.png` 保持不变。

文章继续使用站点根路径 `/images/...` 引用图片。对于包含空格、中文或括号的 Markdown 图片目标，统一改写为尖括号包裹的目标形式，例如：

```markdown
![图片](</images/程序设计(A)(C)/示例.png>)
```

该改写只改变 Markdown 链接语法，不改变图片实际路径。

## Markdown 兼容处理

每篇文章执行以下最小转换：

1. 保留 YAML Front Matter 中的 `title`、`date`、`author`、`categories` 和 `tags`。
2. 将两篇文章中误写的 `catagories` 修正为 `categories`。
3. 若正文没有文章级一级标题，则在 Front Matter 后补充与 `title` 相同的一级标题。
4. 若正文已有与文章标题对应的一级标题，则不重复添加。
5. 仅改写 Markdown 图片目标，不修改代码块、普通网址或正文措辞。

## 栏目入口与导航

保留根导航 `首页 / 校内 / CTF / 随笔 / 友链 / 关于` 不变。`mkdocs-awesome-nav` 自动发现新文章，因此新增文章不需要逐篇写入根 `.nav.yml`。

更新 `docs/study/index.md`、`docs/ctf/index.md` 和 `docs/sth/index.md`，按发布日期从新到旧列出本次迁移的文章，使读者可从栏目首页直接进入文章。

## 验证与错误处理

迁移检查应覆盖：

- 目标目录恰好新增 9 篇文章。
- 旧图片库中的 131 个文件均存在于目标图片库中，且原头像仍存在。
- 所有 Markdown 本地图片引用都能映射到 `docs/images` 中的真实文件。
- Front Matter 字段可解析，且不存在遗留的 `catagories`。
- 三个栏目首页包含各自全部迁移文章。
- `mkdocs build --strict` 成功。
- 生成后的文章页面存在，并且本地图片 URL 对应的生成文件存在。

若发现缺图、无法解析的 Front Matter 或严格构建错误，停止提交迁移结果并报告具体文章和路径；不从网络补图，也不改动旧博客来掩盖问题。

## 非目标

- 不删除、移动或编辑 `D:\Project\my-blog`。
- 不部署或推送 GitHub。
- 不统一英文文件名或 URL。
- 不新增评论、归档、标签页或日期展示插件。
- 不对文章事实内容、代码和措辞做编辑性修改。
