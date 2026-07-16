# 首页主题壁纸实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**目标：** 在首页上方显示响应式大图，亮色主题使用 `洛天依壁纸.png`，暗色主题使用 `洛天依壁纸_夜.png`，并保留下方现有文字与 GitHub 按钮。

**架构：** 在首页卡片内同时放置亮色和暗色两张图片，由 Material 主题根元素上的 `data-md-color-scheme` 属性配合 CSS 控制显隐。图片使用统一的响应式样式，宽度填满正文区域、保持原始比例且不裁切。

**技术栈：** MkDocs、Material for MkDocs、Python Markdown 的 `md_in_html` 扩展、HTML、CSS。

## 全局约束

- 亮色主题必须显示 `docs/images/洛天依壁纸.png`。
- 暗色主题必须显示 `docs/images/洛天依壁纸_夜.png`。
- 任一主题下只能显示一张壁纸。
- 图片不得拉伸或裁切，移动端继续按原始宽高比缩放。
- 标题、简介和 GitHub 按钮保留在图片下方。
- 不新增 JavaScript 或第三方依赖。

---

### 任务 1：首页主题壁纸

**文件：**

- 修改：`docs/index.md:6-14`
- 修改：`docs/resources/css/extra.css:25-50`
- 修改：`docs/resources/css/extra.css:59-62`

**接口：**

- 使用：Material 在根元素上提供的 `data-md-color-scheme="slate"` 暗色主题标记。
- 产出：`.profile-wallpaper` 公共图片样式，以及 `.profile-wallpaper--light`、`.profile-wallpaper--dark` 两个主题变体。

- [ ] **步骤 1：确认修改前基线**

运行：

```powershell
rg -n "profile-avatar|profile-wallpaper" docs/index.md docs/resources/css/extra.css
```

预期：能找到 `profile-avatar` 的 HTML 和 CSS；找不到 `profile-wallpaper`。

- [ ] **步骤 2：替换首页头像标记**

将 `docs/index.md` 中原来的头像：

```html
  <img class="profile-avatar" src="images/avatar.png" alt="TangentZX avatar">
```

替换为：

```html
  <img class="profile-wallpaper profile-wallpaper--light" src="images/洛天依壁纸.png" alt="洛天依壁纸">
  <img class="profile-wallpaper profile-wallpaper--dark" src="images/洛天依壁纸_夜.png" alt="洛天依夜间壁纸">
```

不要改动该文件中现有的标题文本、简介或 GitHub 链接。

- [ ] **步骤 3：把圆形头像样式替换为响应式壁纸样式**

从 `docs/resources/css/extra.css` 删除完整的 `.profile-avatar` 规则和 `[data-md-color-scheme="slate"] .profile-avatar` 规则，加入：

```css
.profile-wallpaper {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 14px 35px rgba(63, 81, 181, 0.18);
}

.profile-wallpaper--dark { display: none; }

[data-md-color-scheme="slate"] .profile-wallpaper--light { display: none; }
[data-md-color-scheme="slate"] .profile-wallpaper--dark { display: block; }
```

在现有暗色主题规则之后加入暗色阴影规则：

```css
[data-md-color-scheme="slate"] .profile-wallpaper {
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.35);
}
```

- [ ] **步骤 4：执行静态检查和站点构建**

运行：

```powershell
rg -n "profile-avatar" docs/index.md docs/resources/css/extra.css
D:\Project\new-blog\.venv\Scripts\python.exe -m mkdocs build --strict
```

预期：第一条命令没有匹配；MkDocs 输出 `Documentation built` 并以状态码 `0` 结束。

- [ ] **步骤 5：浏览器验收**

启动本地预览并打开首页。依次切换亮色和暗色主题，确认：

- 亮色主题只显示 `洛天依壁纸.png`。
- 暗色主题只显示 `洛天依壁纸_夜.png`。
- 两种主题下图片均不变形、不裁切。
- 标题、简介和 GitHub 按钮位于图片下方。
- 将视口缩窄至手机宽度后，图片仍完整显示且没有横向滚动条。

- [ ] **步骤 6：提交实现**

```powershell
git add docs/index.md docs/resources/css/extra.css
git commit -m "feat: add theme-aware homepage wallpaper"
```
