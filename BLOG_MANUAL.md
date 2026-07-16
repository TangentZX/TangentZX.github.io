# TangentZX's Blog 操作手册

本文档用于维护 `D:\Project\new-blog` 下的 MkDocs Material 博客。

线上地址：<https://tangentzx.github.io/>

仓库地址：<https://github.com/TangentZX/TangentZX.github.io>

> [!IMPORTANT]
> 所有源文件都在 `D:\Project\new-blog` 中维护。不要直接修改 `site/` 或远程 `gh-pages` 分支中的文件，它们都是构建产物。

## 1. 项目概览

### 1.1 关键目录

```text
D:\Project\new-blog
├─ docs/                         # 博客正文和静态资源
│  ├─ index.md                   # 首页
│  ├─ about/index.md             # 关于页
│  ├─ links/index.md             # 友链页
│  ├─ study/                     # 校内篇文章
│  ├─ ctf/                       # CTF 篇文章
│  ├─ sth/                       # 杂篇文章
│  ├─ archive/                   # 分类、标签和归档页面
│  ├─ images/                    # 头像、文章图片等静态资源
│  └─ resources/                 # CSS 和 JavaScript
├─ hooks/taxonomy.py             # 分类树、标签与篇章导航生成逻辑
├─ tests/                        # 项目测试
├─ .github/workflows/deploy.yml  # GitHub Actions 部署流程
├─ mkdocs.yml                    # MkDocs 全站配置
├─ requirements.txt              # Python 依赖
└─ site/                         # 构建产物，禁止手动修改
```

### 1.2 三个现有篇章

| 顶部篇章 | 文章目录 | `categories` 根节点 |
| --- | --- | --- |
| 校内篇 | `docs/study/` | `校内` |
| CTF篇 | `docs/ctf/` | `CTF` |
| 杂篇 | `docs/sth/` | `随笔` |

### 1.3 自动生成的内容

启动或构建 MkDocs 时，`hooks/taxonomy.py` 会读取文章 front matter，并自动更新：

- `docs/study/.nav.yml`
- `docs/ctf/.nav.yml`
- `docs/sth/.nav.yml`
- 三个篇章 `index.md` 中的文章分类树
- `docs/archive/categories.md`
- `docs/archive/tags.md`

因此不要直接维护上述 `.nav.yml`、分类页、标签页或篇章首页的自动生成区域。

自动生成区域由下面两个标记包围：

```html
<!-- taxonomy:articles:start -->
这里的内容由 Hook 生成
<!-- taxonomy:articles:end -->
```

篇章简介应写在标记之外。

## 2. 本地启动与预览

### 2.1 启动本地服务

在 PowerShell 中执行：

```powershell
cd D:\Project\new-blog
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8001
```

浏览器访问：

<http://127.0.0.1:8001/>

保存 Markdown、CSS 或 JavaScript 后，MkDocs 通常会自动重新构建并刷新页面。

### 2.2 停止本地服务

回到运行 MkDocs 的终端，按：

```text
Ctrl+C
```

不要直接关闭正在写文件的终端。停止后如需确认端口，可重新访问 `http://127.0.0.1:8001/`。

### 2.3 在新电脑恢复环境

如果 `.venv` 不存在：

```powershell
cd D:\Project\new-blog
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`.venv/` 已被 Git 忽略，不需要提交。

## 3. 新建文章

### 3.1 基本规则

目前 Hook 使用 `directory.glob("*.md")` 收集文章，因此文章 Markdown 必须直接位于篇章目录中。

正确：

```text
docs/study/操作系统笔记.md
```

错误：

```text
docs/study/笔记/操作系统/操作系统笔记.md
```

分类层级写在 front matter 的 `categories` 中，不通过 Markdown 子目录表达。

每篇文章建议采用以下正文结构：

```markdown
# 文章标题

文章简介。

## 一级正文标题

### 二级正文标题
```

### 3.2 校内篇模板

在 `docs/study/` 下新建 Markdown，例如 `操作系统笔记.md`：

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

### 3.3 CTF 篇模板

在 `docs/ctf/` 下新建 Markdown，例如 `某某比赛WP.md`：

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
  - Pwn
---
```

如果文章作者不是 `1so`，按实际作者修改 `author`。

### 3.4 杂篇模板

在 `docs/sth/` 下新建 Markdown，例如 `一篇随笔.md`：

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

### 3.5 保存后的自动流程

当本地服务正在运行时，保存文章后会自动：

1. 读取 `title`、`date`、`categories` 和 `tags`；
2. 将文章加入对应篇章的分类树；
3. 生成或更新该篇章 `.nav.yml`；
4. 更新全站分类页和标签词云；
5. 按日期从最近到最远排序文章。

如果页面没有自动更新，先查看运行 MkDocs 的终端是否报错，再手动刷新浏览器。

## 4. 分类、标签、作者与排序

### 4.1 嵌套分类

`categories` 是分类路径列表。下面的写法表示：

```text
校内
└─ 笔记
   └─ 计算机网络
      └─ 实验
```

```yaml
categories:
  - [校内, 笔记, 计算机网络, 实验]
```

分类路径的第一个元素必须与篇章根节点一致：

- `docs/study/` 使用 `校内`
- `docs/ctf/` 使用 `CTF`
- `docs/sth/` 使用 `随笔`

否则该文章可能出现在文章收集中，却不会进入该篇章的左侧分类树。

### 4.2 标签

标签不表达父子关系，适合记录文章主题、技术方向或比赛类型：

```yaml
tags:
  - CTF
  - Reverse
  - Android
```

标签会出现在文章顶部和全站标签词云中。重复标签会自动去重。

### 4.3 作者

当前约定：

- 普通文章：`Tangent丶ZX`
- 当前两篇 CTF WP：`1so`

示例：

```yaml
author: Tangent丶ZX
```

### 4.4 日期与排序

推荐使用：

```yaml
date: 2026-07-16
```

系统按 `date` 从最近到最远排序。日期无效或缺失时，文章会排在有有效日期的文章之后。

## 5. 文章图片

### 5.1 存放位置

图片统一放在 `docs/images/` 下，并延续当前分类目录：

```text
docs/images/笔记/操作系统/进程状态图.png
docs/images/CTF/WP/比赛名称/题目截图.png
docs/images/随便写写/游记/照片.png
```

不要把文章图片放进 `site/`，因为下一次构建会清理该目录。

### 5.2 Markdown 引用

使用从网站根目录开始的路径：

```markdown
![进程状态图](</images/笔记/操作系统/进程状态图.png>)
```

路径中包含中文、空格或括号时，保留 `< >` 可以减少解析歧义。

### 5.3 图片更新建议

- 文件名应能说明内容，避免大量使用 `1.png`、`2.png`。
- 同一篇文章的图片放在同一子目录。
- 修改图片后检查浅色和深色模式下的可读性。
- 提交前确认 Markdown 路径与磁盘文件名大小写一致。

## 6. 修改固定页面

| 要修改的内容 | 文件 |
| --- | --- |
| 首页 | `docs/index.md` |
| 关于页 | `docs/about/index.md` |
| 友链页 | `docs/links/index.md` |
| 校内篇简介 | `docs/study/index.md` |
| CTF 篇简介 | `docs/ctf/index.md` |
| 杂篇简介 | `docs/sth/index.md` |
| 顶部导航 | `docs/.nav.yml` |
| 站名、主题、扩展、资源 | `mkdocs.yml` |

### 6.1 修改篇章简介

只修改自动生成标记之前或之后的手写内容：

```markdown
# 校内篇

这里是可编辑的篇章简介。

<!-- taxonomy:articles:start -->
不要手动编辑这里
<!-- taxonomy:articles:end -->
```

### 6.2 添加友链

1. 把友链头像放入 `docs/images/`；
2. 打开 `docs/links/index.md`；
3. 复制一张现有 `.friend-card`；
4. 修改链接、头像、名称、账号和简介；
5. 在桌面双列和移动端单列布局下检查。

示例：

```html
<a class="friend-card"
   href="https://example.com/"
   target="_blank"
   rel="noopener noreferrer">
  <img src="../images/avatar_example.png"
       alt="Example 的头像"
       loading="lazy">
  <span class="friend-copy">
    <strong>Example's Blog</strong>
    <small>@Example</small>
    <span class="friend-desc">个人简介</span>
  </span>
</a>
```

## 7. Markdown 常用语法

### 7.1 代码块

````markdown
```python
def hello():
    print("Hello")
```
````

代码语言会显示在代码块顶部。代码块支持复制按钮，长代码会根据当前脚本规则折叠。

### 7.2 行内代码

```markdown
使用 `printf()` 输出内容。
```

### 7.3 引用块

```markdown
> 这里是一段引用。
>
> 可以包含多个段落。
```

### 7.4 表格

```markdown
| 名称 | 状态 | 分数 |
| --- | --- | ---: |
| Web | 完成 | 100 |
| Pwn | 进行中 | 200 |
```

表格过宽时会出现横向滚动，不要用空白列人为撑宽。

### 7.5 高亮与删除线

```markdown
==需要高亮的内容==

~~已经删除的内容~~
```

### 7.6 提示块

```markdown
!!! warning "注意"
    这里填写警告内容。
```

常用类型包括 `note`、`tip`、`warning`、`danger` 和 `info`。

### 7.7 折叠块

默认折叠：

```markdown
??? note "点击展开"
    这里是折叠内容。
```

默认展开：

```markdown
???+ note "默认展开"
    这里是展开内容。
```

### 7.8 数学公式

行内公式：

```markdown
\(a^2+b^2=c^2\)
```

块级公式：

```markdown
\[
E = mc^2
\]
```

数学公式由 MathJax 渲染。

## 8. 修改样式与脚本

### 8.1 CSS 文件职责

| 文件 | 主要职责 |
| --- | --- |
| `docs/resources/css/extra.css` | 全站基础补充样式 |
| `docs/resources/css/tittle.css` | 标题相关样式 |
| `docs/resources/css/read-metrics.css` | 阅读时长、字数等信息 |
| `docs/resources/css/leftsidebar.css` | 左侧分类树、激活项和竖条 |
| `docs/resources/css/article-content.css` | 代码、行内代码、引用、表格等正文样式 |
| `docs/resources/css/friend-links.css` | 友链卡片布局和响应式样式 |
| `docs/resources/css/taxonomy.css` | 分类树、归档和标签词云 |

### 8.2 JavaScript 文件职责

| 文件 | 主要职责 |
| --- | --- |
| `docs/resources/js/read-metrics.js` | 计算阅读时长和字数 |
| `docs/resources/js/sidebar-resize.js` | 侧栏尺寸行为 |
| `docs/resources/js/toc-follow.js` | 右侧目录跟随、回到顶部后的同步 |
| `docs/resources/js/code-fold.js` | 长代码自动折叠 |
| `docs/resources/js/mathjax-config.js` | MathJax 配置 |

修改样式后至少检查：

- 浅色模式；
- 深色模式；
- 桌面三栏布局；
- 窄屏或移动端布局；
- 长标题、长代码和宽表格。

## 9. 新建一个完整篇章

下面以新增“阅读篇”为例。新增篇章不只是新建目录，还必须登记导航、篇章显示名和分类根节点。

### 9.1 创建目录与首页

```text
docs/reading/
├─ index.md
└─ 某篇读书笔记.md
```

`docs/reading/index.md` 可以先写：

```markdown
# 阅读篇

这里记录读书笔记和阅读随想。
```

文章仍应直接放在 `docs/reading/` 下，不要再建 Markdown 子目录。

### 9.2 加入顶部导航

编辑 `docs/.nav.yml`，在合适位置增加：

```yaml
- 阅读篇: reading
```

完整结构示意：

```yaml
nav:
  - 首页: index.md
  - 校内篇: study
  - CTF篇: ctf
  - 杂篇: sth
  - 阅读篇: reading
  - 归档: archive
  - 友链: links
  - 关于: about
```

### 9.3 登记 taxonomy Hook

编辑 `hooks/taxonomy.py`。

把 `reading` 加入 `SECTION_TITLES`：

```python
SECTION_TITLES = {
    "study": "校内篇",
    "ctf": "CTF篇",
    "sth": "杂篇",
    "reading": "阅读篇",
}
```

把分类根节点加入 `SECTION_CATEGORY_ROOTS`：

```python
SECTION_CATEGORY_ROOTS = {
    "study": "校内",
    "ctf": "CTF",
    "sth": "随笔",
    "reading": "阅读",
}
```

三者职责不同：

| 值 | 含义 |
| --- | --- |
| `reading` | 磁盘目录和内部篇章键 |
| `阅读篇` | 页面和导航中显示的篇章名称 |
| `阅读` | 文章 `categories` 的第一个元素 |

### 9.4 新篇章文章模板

`docs/reading/某篇读书笔记.md`：

```yaml
---
title: 某篇读书笔记
author: Tangent丶ZX
date: 2026-07-16
categories:
  - [阅读, 小说]
tags:
  - 阅读
  - 小说
---
```

保存并启动 MkDocs 后，Hook 会生成：

```text
docs/reading/.nav.yml
```

同时在阅读篇首页生成分类树，并更新全站分类和标签页面。

### 9.5 为新篇章补充测试

新增篇章会改变文章收集范围和导航契约，因此发布前需要更新：

- `tests/test_taxonomy.py`：验证 `reading` 的分类树和 `.nav.yml`；
- `tests/test_content_migration.py`：验证篇章目录和导航结构；
- `tests/test_built_site.py`：验证构建后阅读篇页面和左侧导航。

测试至少应覆盖：

1. `categories: [阅读, 小说]` 能进入阅读篇分类树；
2. 文章出现在 `docs/reading/.nav.yml`；
3. 当前分类路径展开，其他分类保持折叠；
4. 严格构建没有未导航页面或无效链接警告。

### 9.6 新篇章常见错误

- 创建了 `docs/reading/`，但忘记加入 `SECTION_TITLES`；
- 加入了篇章标题，却忘记设置 `SECTION_CATEGORY_ROOTS`；
- 文章写成 `[读书, 小说]`，但根节点配置为 `阅读`；
- 把文章放进 `docs/reading/小说/`，导致当前 Hook 扫描不到；
- 手动编写 `.nav.yml`，随后又被 Hook 覆盖；
- 没有更新测试，直到 GitHub Actions 才发现构建失败。

## 10. 构建、测试与发布

### 10.1 发布前严格构建

```powershell
cd D:\Project\new-blog
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

成功时命令退出码为 0。`--strict` 会把警告视为错误。

### 10.2 运行完整测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

必须看到：

```text
OK
```

### 10.3 检查改动

```powershell
git status
git diff --check
git diff
```

确认没有把以下内容提交进去：

- `.venv/`
- `site/`
- 临时日志
- 与本次更新无关的文件

### 10.4 提交

```powershell
git add -A
git commit -m "docs: update blog"
```

更具体的提交信息更容易回溯，例如：

```powershell
git commit -m "docs: add operating system notes"
```

### 10.5 推送

当前 Windows 浏览器使用本地代理 `127.0.0.1:10808`，Git 没有永久代理配置时使用：

```powershell
git -c http.proxy=http://127.0.0.1:10808 push
```

如果不需要代理：

```powershell
git push
```

不要为了日常发布使用 `--force` 或 `--force-with-lease`。

推送 `main` 后，`.github/workflows/deploy.yml` 会自动：

1. 检出源码；
2. 安装 `requirements.txt`；
3. 执行严格 MkDocs 部署；
4. 更新 `gh-pages`；
5. 发布到 GitHub Pages。

在仓库的 Actions 页面确认 `deploy` 变为绿色后，再访问线上页面检查。

## 11. GitHub 分支与旧博客备份

### 11.1 当前分支职责

| 分支 | 职责 | 是否日常编辑 |
| --- | --- | --- |
| `main` | 新 MkDocs 博客源码 | 是 |
| `gh-pages` | MkDocs 自动生成的网站 | 否 |
| `legacy-hexo-source` | 旧 Hexo 源码备份 | 否 |
| `legacy-hexo-site` | 旧 Hexo 静态网站备份 | 否 |

### 11.2 日常原则

- 只在 `main` 上维护源码；
- 不手动修改 `gh-pages`；
- 不删除两个 `legacy-*` 分支；
- 不把 `legacy-*` 合并回 `main`；
- 发布异常时先检查 Actions 日志，不要立即强推。

### 11.3 回滚旧博客的安全思路

回滚属于恢复操作，不是日常命令。需要时按以下顺序处理：

1. 在 GitHub 确认 `legacy-hexo-site` 仍指向旧站完整提交；
2. 确认 `legacy-hexo-source` 仍保留旧源码；
3. 记录当前 `main` 和 `gh-pages` 的 SHA，必要时再建恢复前备份；
4. 在仓库 `Settings → Pages` 核对当前发布方式；
5. 决定是临时切换 Pages 发布源，还是恢复 `gh-pages`；
6. 恢复后访问线上站点并检查静态资源路径。

不要在没有核对 SHA 和备份分支的情况下复制一条强制推送命令执行。需要回滚时，优先根据当时的远程状态制定一次性命令。

## 12. 常见问题

### 12.1 `gh` 已安装但 PowerShell 找不到

关闭并重新打开 PowerShell，或者使用完整路径：

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

### 12.2 浏览器能访问 GitHub，但 `git push` 超时

Git 可能没有继承 Windows 系统代理。使用：

```powershell
git -c http.proxy=http://127.0.0.1:10808 push
```

如果代理端口改变，相应修改 `10808`。

### 12.3 新文章没有出现在左侧分类树

依次检查：

1. Markdown 是否直接放在篇章目录下；
2. front matter 是否由两行 `---` 包围；
3. `categories` 第一个元素是否匹配篇章根节点；
4. `date` 格式是否有效；
5. MkDocs 终端是否有 YAML 或 Hook 报错。

### 12.4 图片本地不显示

检查：

- 图片是否位于 `docs/images/`；
- Markdown 是否使用 `/images/...`；
- 文件名、扩展名和大小写是否一致；
- 中文或空格路径是否使用 `< >` 包裹。

### 12.5 修改篇章首页后内容消失

很可能修改了自动生成标记之间的内容。把手写简介移动到：

```html
<!-- taxonomy:articles:start -->
```

之前或结束标记之后。

### 12.6 构建时提示文件被占用

可能有另一个 `mkdocs serve` 正在使用 `site/`。先在对应终端按 `Ctrl+C`，再重新执行严格构建。

### 12.7 GitHub Actions 成功但线上仍是旧页面

1. 使用带查询参数的 URL 避免浏览器缓存，例如 `?rev=时间戳`；
2. 检查 `gh-pages` 是否产生新提交；
3. 检查 `Settings → Pages` 的发布配置；
4. 等待 GitHub Pages CDN 完成刷新。

## 13. 发布检查清单

每次发布前按顺序检查：

- [ ] 文章 front matter 包含正确的 `title`、`author`、`date`、`categories` 和 `tags`
- [ ] 文章 Markdown 直接位于对应篇章目录
- [ ] `categories` 根节点与篇章配置一致
- [ ] 图片位于 `docs/images/` 且路径可以打开
- [ ] 浅色与深色模式显示正常
- [ ] 桌面和窄屏布局没有明显溢出
- [ ] 代码块、引用块和表格显示正常
- [ ] 本地 MkDocs 预览正常
- [ ] `mkdocs build --strict` 通过
- [ ] `python -m unittest discover -s tests` 显示 `OK`
- [ ] `git diff --check` 没有空白错误
- [ ] `git status` 中没有临时文件或构建产物
- [ ] 提交信息能说明本次改动
- [ ] 推送到 `main`，没有使用强制推送
- [ ] GitHub Actions 的 `deploy` 工作流成功
- [ ] 线上 <https://tangentzx.github.io/> 已更新
- [ ] `legacy-hexo-source` 和 `legacy-hexo-site` 仍保留

