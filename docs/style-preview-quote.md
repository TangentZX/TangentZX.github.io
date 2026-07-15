---
hide:
  - navigation
  - toc
---

# 引用块样式候选

三个候选使用相同内容，请比较正文层次、长时间阅读舒适度，以及与彩色玻璃代码块是否协调。

<style>
.quote-options { display: grid; gap: 1.35rem; }
.quote-option {
  padding: 1rem 1rem .35rem;
  border: 1px solid color-mix(in srgb, var(--md-default-fg-color) 12%, transparent);
  border-radius: 14px;
}
.quote-option > h2 { margin-top: 0; }
.quote-option blockquote {
  margin: .7rem 0 1rem;
  padding: 1rem 1.15rem;
  color: var(--md-default-fg-color);
}
.quote-option blockquote p:first-child { margin-top: 0; }
.quote-option blockquote p:last-child { margin-bottom: 0; }
.quote-option blockquote strong { color: var(--md-primary-fg-color); }

.quote-a blockquote {
  border-left: 4px solid #5c6bc0;
  border-radius: 0 8px 8px 0;
  background: rgba(92, 107, 192, .055);
  box-shadow: none;
}

.md-typeset .quote-b > blockquote {
  border: 1px solid color-mix(in srgb, #5c6bc0 20%, transparent);
  border-left-width: 4px;
  border-left-style: solid;
  border-left-color: #4a54af;
  border-radius: 11px;
  background:
    radial-gradient(circle at 8% 0%, rgba(99, 102, 241, .14), transparent 34%),
    radial-gradient(circle at 92% 18%, rgba(56, 189, 248, .10), transparent 38%),
    radial-gradient(circle at 62% 110%, rgba(192, 132, 252, .09), transparent 40%),
    rgba(255, 255, 255, .58);
  box-shadow: 0 7px 22px rgba(63, 81, 181, .07);
  backdrop-filter: blur(12px);
}
[data-md-color-scheme="slate"] .md-typeset .quote-b > blockquote {
  border-left-color: #6171f5;
  background:
    radial-gradient(circle at 8% 0%, rgba(99, 102, 241, .17), transparent 34%),
    radial-gradient(circle at 92% 18%, rgba(56, 189, 248, .10), transparent 38%),
    radial-gradient(circle at 62% 110%, rgba(192, 132, 252, .09), transparent 40%),
    rgba(33, 37, 43, .64);
}

.quote-c blockquote {
  position: relative;
  overflow: hidden;
  padding: 1.35rem 1.3rem 1.1rem 3.3rem;
  border: 1px solid color-mix(in srgb, #5c6bc0 18%, transparent);
  border-left: 0;
  border-radius: 12px;
  background: color-mix(in srgb, var(--md-default-bg-color) 88%, #5c6bc0 12%);
  box-shadow: 0 8px 22px rgba(15, 23, 42, .07);
}
.quote-c blockquote::before {
  content: "“";
  position: absolute;
  top: -.25rem;
  left: .65rem;
  color: rgba(92, 107, 192, .28);
  font: 700 4.6rem/1 Georgia, serif;
}
</style>

<div class="quote-options">
  <section class="quote-option quote-a">
    <h2>A · 极简 Indigo 左线</h2>
    <p>结构最克制，适合技术文章中的高频引用。</p>
    <blockquote>
      <p><strong>提示：</strong>迁移文章时应保留原始路径，避免图片链接失效。</p>
      <p>引用块也可能包含多段文字、<code>inline code</code> 和补充说明，因此需要保持足够的正文对比度。</p>
    </blockquote>
  </section>

  <section class="quote-option quote-b">
    <h2>B · 彩色玻璃</h2>
    <p>延续代码块的 Indigo、青、紫渐变，整体语言最统一。</p>
    <blockquote>
      <p><strong>提示：</strong>迁移文章时应保留原始路径，避免图片链接失效。</p>
      <p>引用块也可能包含多段文字、<code>inline code</code> 和补充说明，因此需要保持足够的正文对比度。</p>
    </blockquote>
  </section>

  <section class="quote-option quote-c">
    <h2>C · 引号卡片</h2>
    <p>更像传统文章引用，装饰性最强，但占用空间也更多。</p>
    <blockquote>
      <p><strong>提示：</strong>迁移文章时应保留原始路径，避免图片链接失效。</p>
      <p>引用块也可能包含多段文字、<code>inline code</code> 和补充说明，因此需要保持足够的正文对比度。</p>
    </blockquote>
  </section>
</div>
