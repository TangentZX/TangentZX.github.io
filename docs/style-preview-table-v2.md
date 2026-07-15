---
hide:
  - navigation
  - toc
---

# B · 彩色玻璃表格（真实 Markdown）

这一版直接使用博客文章中的 Markdown 表格语法，不再添加手写滚动容器。

<style>
.md-typeset .md-typeset__table {
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 1rem 0;
  padding: 0;
  overflow-x: auto;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
}
.md-typeset .md-typeset__table table:not([class]) {
  display: table;
  width: 100%;
  min-width: 100%;
  max-width: none;
  margin: 0;
  overflow: visible;
  border: 1px solid color-mix(in srgb, #5c6bc0 20%, transparent);
  border-radius: 10px;
  border-collapse: separate;
  border-spacing: 0;
  background:
    radial-gradient(circle at 5% 0%, rgba(99, 102, 241, .12), transparent 34%),
    radial-gradient(circle at 95% 10%, rgba(56, 189, 248, .09), transparent 38%),
    rgba(255, 255, 255, .58);
  box-shadow: 0 7px 22px rgba(63, 81, 181, .07);
  backdrop-filter: blur(12px);
  font-size: .8rem;
}
.md-typeset .md-typeset__table th,
.md-typeset .md-typeset__table td {
  padding: .72rem .85rem;
  text-align: left;
}
.md-typeset .md-typeset__table th {
  border-bottom: 1px solid color-mix(in srgb, #4a54af 30%, transparent);
  background: rgba(74, 84, 175, .09);
  color: #4a54af;
}
.md-typeset .md-typeset__table thead tr:first-child th:first-child {
  border-top-left-radius: 9px;
}
.md-typeset .md-typeset__table thead tr:first-child th:last-child {
  border-top-right-radius: 9px;
}
.md-typeset .md-typeset__table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 9px;
}
.md-typeset .md-typeset__table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 9px;
}
.md-typeset .md-typeset__table td {
  border-bottom: 1px solid color-mix(in srgb, var(--md-default-fg-color) 8%, transparent);
}
.md-typeset .md-typeset__table tbody tr:nth-child(even) {
  background: rgba(92, 107, 192, .045);
}
.md-typeset .md-typeset__table tbody tr:last-child td { border-bottom: 0; }
[data-md-color-scheme="slate"] .md-typeset .md-typeset__table table:not([class]) {
  background:
    radial-gradient(circle at 5% 0%, rgba(99, 102, 241, .15), transparent 34%),
    radial-gradient(circle at 95% 10%, rgba(56, 189, 248, .08), transparent 38%),
    rgba(33, 37, 43, .66);
}
[data-md-color-scheme="slate"] .md-typeset .md-typeset__table th {
  border-bottom-color: rgba(97, 113, 245, .34);
  background: rgba(74, 84, 175, .24);
  color: #eef0ff;
}
[data-md-color-scheme="slate"] .md-typeset .md-typeset__table tbody tr:nth-child(even) {
  background: rgba(97, 113, 245, .055);
}
</style>

| 分类 | 题目 | 状态 | 分数 |
| --- | --- | --- | ---: |
| Web | Login Again | 已完成 | 100 |
| Pwn | Heap Practice | 进行中 | 200 |
| Reverse | Tiny VM | 已完成 | 150 |
| Crypto | Simple RSA | 待复盘 | 120 |
