---
hide:
  - navigation
  - toc
---

# 表格样式候选

三个候选使用相同数据。请比较扫描速度、边框强弱和手机端横向滚动时的可读性。

<style>
.table-options { display: grid; gap: 1.4rem; }
.table-option {
  padding: 1rem;
  border: 1px solid color-mix(in srgb, var(--md-default-fg-color) 12%, transparent);
  border-radius: 14px;
}
.table-option > h2 { margin-top: 0; }
.table-scroll { overflow-x: auto; border-radius: 10px; }
.md-typeset .table-option table:not([class]) {
  display: table;
  width: 100%;
  min-width: 34rem;
  max-width: none;
  margin: 0;
  overflow: visible;
  vertical-align: top;
  border-collapse: separate;
  border-spacing: 0;
  background: transparent;
  font-size: .8rem;
}
.table-option th,
.table-option td { padding: .72rem .85rem; text-align: left; }

.table-a table { border-top: 2px solid var(--md-primary-fg-color); }
.table-a th {
  border-bottom: 1px solid color-mix(in srgb, var(--md-primary-fg-color) 30%, transparent);
  color: var(--md-primary-fg-color);
  background: transparent;
}
.table-a td { border-bottom: 1px solid color-mix(in srgb, var(--md-default-fg-color) 10%, transparent); }

.table-b .table-scroll {
  border: 1px solid color-mix(in srgb, #5c6bc0 20%, transparent);
  background:
    radial-gradient(circle at 5% 0%, rgba(99, 102, 241, .12), transparent 34%),
    radial-gradient(circle at 95% 10%, rgba(56, 189, 248, .09), transparent 38%),
    rgba(255, 255, 255, .58);
  box-shadow: 0 7px 22px rgba(63, 81, 181, .07);
  backdrop-filter: blur(12px);
}
.table-b th {
  border-bottom: 1px solid color-mix(in srgb, var(--md-primary-fg-color) 28%, transparent);
  background: rgba(92, 107, 192, .09);
  color: var(--md-primary-fg-color);
}
.table-b td { border-bottom: 1px solid color-mix(in srgb, var(--md-default-fg-color) 8%, transparent); }
.table-b tbody tr:nth-child(even) { background: rgba(92, 107, 192, .045); }
.table-b tbody tr:last-child td { border-bottom: 0; }
[data-md-color-scheme="slate"] .table-b .table-scroll {
  background:
    radial-gradient(circle at 5% 0%, rgba(99, 102, 241, .15), transparent 34%),
    radial-gradient(circle at 95% 10%, rgba(56, 189, 248, .08), transparent 38%),
    rgba(33, 37, 43, .66);
}
[data-md-color-scheme="slate"] .table-b th {
  border-bottom-color: rgba(97, 113, 245, .34);
  background: rgba(74, 84, 175, .24);
  color: #eef0ff;
}
[data-md-color-scheme="slate"] .table-b tbody tr:nth-child(even) {
  background: rgba(97, 113, 245, .055);
}

.table-c .table-scroll { border: 1px solid color-mix(in srgb, var(--md-default-fg-color) 18%, transparent); }
.table-c th {
  border-right: 1px solid rgba(255,255,255,.15);
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
}
.table-c td {
  border-right: 1px solid color-mix(in srgb, var(--md-default-fg-color) 12%, transparent);
  border-bottom: 1px solid color-mix(in srgb, var(--md-default-fg-color) 12%, transparent);
}
.table-c th:last-child,
.table-c td:last-child { border-right: 0; }
.table-c tbody tr:last-child td { border-bottom: 0; }
</style>

<div class="table-options">
  <section class="table-option table-a">
    <h2>A · 极简横线</h2>
    <p>边框最少，正文感强，适合简单对照表。</p>
    <div class="table-scroll"><table><thead><tr><th>分类</th><th>题目</th><th>状态</th><th>分数</th></tr></thead><tbody><tr><td>Web</td><td>Login Again</td><td>已完成</td><td>100</td></tr><tr><td>Pwn</td><td>Heap Practice</td><td>进行中</td><td>200</td></tr><tr><td>Reverse</td><td>Tiny VM</td><td>已完成</td><td>150</td></tr><tr><td>Crypto</td><td>Simple RSA</td><td>待复盘</td><td>120</td></tr></tbody></table></div>
  </section>

  <section class="table-option table-b">
    <h2>B · 彩色玻璃表格</h2>
    <p>延续代码块与引用块的渐变，使用轻量斑马纹辅助逐行阅读。</p>
    <div class="table-scroll"><table><thead><tr><th>分类</th><th>题目</th><th>状态</th><th>分数</th></tr></thead><tbody><tr><td>Web</td><td>Login Again</td><td>已完成</td><td>100</td></tr><tr><td>Pwn</td><td>Heap Practice</td><td>进行中</td><td>200</td></tr><tr><td>Reverse</td><td>Tiny VM</td><td>已完成</td><td>150</td></tr><tr><td>Crypto</td><td>Simple RSA</td><td>待复盘</td><td>120</td></tr></tbody></table></div>
  </section>

  <section class="table-option table-c">
    <h2>C · 数据网格</h2>
    <p>表头和单元格边界最明确，适合高密度数据，但视觉重量最大。</p>
    <div class="table-scroll"><table><thead><tr><th>分类</th><th>题目</th><th>状态</th><th>分数</th></tr></thead><tbody><tr><td>Web</td><td>Login Again</td><td>已完成</td><td>100</td></tr><tr><td>Pwn</td><td>Heap Practice</td><td>进行中</td><td>200</td></tr><tr><td>Reverse</td><td>Tiny VM</td><td>已完成</td><td>150</td></tr><tr><td>Crypto</td><td>Simple RSA</td><td>待复盘</td><td>120</td></tr></tbody></table></div>
  </section>
</div>
