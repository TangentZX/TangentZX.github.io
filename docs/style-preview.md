---
hide:
  - navigation
  - toc
---

# 代码块样式候选

下面三个候选使用相同代码内容。请重点比较背景、边框、圆角、层次感和长时间阅读是否舒服。

<style>
.style-preview-grid {
  display: grid;
  gap: 1.4rem;
}
.style-option {
  padding: 1rem;
  border: 1px solid color-mix(in srgb, var(--md-default-fg-color) 14%, transparent);
  border-radius: 14px;
}
.style-option > h2 { margin-top: 0; }
.style-option pre {
  position: relative;
  margin: .7rem 0 0;
  padding: 1.1rem 1.2rem;
  overflow-x: auto;
  font: .78rem/1.65 "JetBrains Mono", "Cascadia Code", Consolas, monospace;
}
.style-option code { color: inherit; background: none; }
.style-option .kw { color: #c678dd; }
.style-option .fn { color: #61afef; }
.style-option .str { color: #98c379; }
.style-option .cm { color: #7f848e; font-style: italic; }
.style-option .num { color: #d19a66; }

.style-a pre {
  border: 1px solid #3a404b;
  border-top: 3px solid #5c6bc0;
  border-radius: 9px;
  background: #282c34;
  color: #abb2bf;
  box-shadow: 0 8px 22px rgba(15, 23, 42, .16);
}

.style-b pre {
  border: 1px solid color-mix(in srgb, #5c6bc0 30%, transparent);
  border-radius: 14px;
  background: linear-gradient(145deg, rgba(63,81,181,.10), rgba(255,255,255,.82));
  color: #303545;
  box-shadow: 0 10px 26px rgba(63, 81, 181, .12);
  backdrop-filter: blur(8px);
}
[data-md-color-scheme="slate"] .style-b pre {
  background: linear-gradient(145deg, rgba(63,81,181,.18), rgba(33,37,43,.92));
  color: #c8ccd4;
}

.style-c pre {
  padding-top: 2.35rem;
  border: 1px solid #424857;
  border-radius: 11px;
  background: #20242b;
  color: #d6dae3;
  box-shadow: 0 12px 28px rgba(0,0,0,.22);
}
.style-c pre::before {
  content: "●  ●  ●    python";
  position: absolute;
  inset: 0 0 auto;
  padding: .48rem .75rem;
  border-bottom: 1px solid #3a404b;
  color: #e06c75;
  background: #2b3039;
  font-size: .68rem;
  letter-spacing: .12em;
}
</style>

<div class="style-preview-grid">
  <section class="style-option style-a">
    <h2>A · Maple / One Dark</h2>
    <p>稳重、清晰，和当前深色主题最一致；顶部 Indigo 线条提供识别度。</p>
    <pre><code><span class="kw">def</span> <span class="fn">solve</span>(values):
    <span class="cm"># 保留偶数并计算平方</span>
    result = [x ** <span class="num">2</span> <span class="kw">for</span> x <span class="kw">in</span> values <span class="kw">if</span> x % <span class="num">2</span> == <span class="num">0</span>]
    <span class="kw">return</span> <span class="str">"flag{"</span> + <span class="str">","</span>.join(map(str, result)) + <span class="str">"}"</span></code></pre>
  </section>

  <section class="style-option style-b">
    <h2>B · Indigo 玻璃卡片</h2>
    <p>更轻、更柔和，浅色模式融合度高；视觉装饰比 A 明显。</p>
    <pre><code><span class="kw">def</span> <span class="fn">solve</span>(values):
    <span class="cm"># 保留偶数并计算平方</span>
    result = [x ** <span class="num">2</span> <span class="kw">for</span> x <span class="kw">in</span> values <span class="kw">if</span> x % <span class="num">2</span> == <span class="num">0</span>]
    <span class="kw">return</span> <span class="str">"flag{"</span> + <span class="str">","</span>.join(map(str, result)) + <span class="str">"}"</span></code></pre>
  </section>

  <section class="style-option style-c">
    <h2>C · 终端窗口</h2>
    <p>CTF 氛围最强，带窗口栏和语言标识；装饰最多，占用纵向空间也最多。</p>
    <pre><code><span class="kw">def</span> <span class="fn">solve</span>(values):
    <span class="cm"># 保留偶数并计算平方</span>
    result = [x ** <span class="num">2</span> <span class="kw">for</span> x <span class="kw">in</span> values <span class="kw">if</span> x % <span class="num">2</span> == <span class="num">0</span>]
    <span class="kw">return</span> <span class="str">"flag{"</span> + <span class="str">","</span>.join(map(str, result)) + <span class="str">"}"</span></code></pre>
  </section>
</div>
