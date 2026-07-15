---
hide:
  - navigation
  - toc
---

# B 方案 · 字体、语言栏与长代码折叠

此页使用你本机安装的 Maple Mono。短代码正常展开；超过 32 行的代码默认折叠，复制按钮仍复制完整内容。

<style>
.md-typeset {
  --code-border: color-mix(in srgb, #5c6bc0 20%, transparent);
  --code-bg:
    radial-gradient(circle at 8% 0%, rgba(99, 102, 241, .18), transparent 34%),
    radial-gradient(circle at 92% 18%, rgba(56, 189, 248, .14), transparent 36%),
    radial-gradient(circle at 62% 110%, rgba(192, 132, 252, .12), transparent 38%),
    rgba(255, 255, 255, .72);
  --code-fg: #303545;
}
[data-md-color-scheme="slate"] .md-typeset {
  --code-border: rgba(121, 134, 203, .22);
  --code-bg:
    radial-gradient(circle at 8% 0%, rgba(99, 102, 241, .20), transparent 34%),
    radial-gradient(circle at 92% 18%, rgba(56, 189, 248, .13), transparent 36%),
    radial-gradient(circle at 62% 110%, rgba(192, 132, 252, .12), transparent 38%),
    rgba(33, 37, 43, .78);
  --code-fg: #d1d5df;
}
.md-typeset .highlight {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--code-border);
  border-radius: 14px;
  background: var(--code-bg);
  box-shadow: 0 8px 24px rgba(63, 81, 181, .08);
  backdrop-filter: blur(14px) saturate(115%);
}
.md-typeset .highlight > .filename {
  position: absolute;
  top: .62rem;
  left: .9rem;
  z-index: 2;
  margin: 0;
  padding: .12rem 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: var(--md-default-fg-color--light);
  font: 600 .64rem/1.2 "Maple Mono NF CN", "Maple Mono CN", "Maple Mono", monospace;
  letter-spacing: .025em;
  backdrop-filter: none;
}
.md-typeset .highlight pre,
.md-typeset .highlight code {
  font-family: "Maple Mono NF CN", "Maple Mono CN", "Maple Mono", "Cascadia Code", Consolas, monospace;
  background: transparent;
}
.md-typeset .highlight pre {
  margin: 0;
  border-radius: 0;
  background: transparent;
  color: var(--code-fg);
}
.md-typeset .highlight > .filename + pre > code {
  padding-top: 2.75rem;
}
.md-typeset .highlight.is-collapsed pre {
  max-height: 24rem;
  overflow: hidden;
  mask-image: linear-gradient(to bottom, #000 78%, transparent 100%);
}
.code-expand-button {
  display: block;
  width: 100%;
  padding: .62rem 1rem;
  border: 0;
  border-top: 1px solid color-mix(in srgb, #5c6bc0 12%, transparent);
  background: rgba(92, 107, 192, .055);
  color: var(--md-primary-fg-color);
  font: 600 .72rem/1.2 "Maple Mono CN", sans-serif;
  cursor: pointer;
}
.code-expand-button:hover { background: rgba(92, 107, 192, .11); }
</style>

## 短代码：保持完整显示

```python title="Python"
def greet(name: str) -> str:
    # 中文注释用于检查 CN 字形
    return f"Hello, {name}!"
```

## 长代码：32 行后自动折叠

```python title="Python · 长代码示例"
from dataclasses import dataclass

@dataclass
class Challenge:
    name: str
    category: str
    points: int

def normalize_name(value: str) -> str:
    return value.strip().lower().replace(" ", "-")

def score_bonus(category: str) -> int:
    bonuses = {
        "web": 20,
        "pwn": 30,
        "reverse": 25,
        "crypto": 15,
        "misc": 10,
    }
    return bonuses.get(category, 0)

def calculate(challenge: Challenge) -> int:
    # 中文注释：计算题目最终分数
    base = max(challenge.points, 0)
    bonus = score_bonus(challenge.category)
    return base + bonus

def render(challenges: list[Challenge]) -> list[str]:
    output = []
    for challenge in challenges:
        slug = normalize_name(challenge.name)
        score = calculate(challenge)
        output.append(f"{slug}: {score}")
    return output

items = [
    Challenge("First Web", "web", 100),
    Challenge("Heap Practice", "pwn", 200),
    Challenge("Tiny VM", "reverse", 150),
]

for line in render(items):
    print(line)
```

<script>
(() => {
  const mount = () => {
    document.querySelectorAll(".md-typeset .highlight").forEach((block) => {
      if (block.dataset.foldReady) return;
      const code = block.querySelector("code");
      if (!code) return;
      const lineCount = code.textContent.replace(/\n$/, "").split("\n").length;
      if (lineCount <= 32) return;
      block.dataset.foldReady = "true";
      block.classList.add("is-collapsed");
      const button = document.createElement("button");
      button.className = "code-expand-button";
      button.type = "button";
      button.textContent = `展开全部 · ${lineCount} 行`;
      button.addEventListener("click", () => {
        const collapsed = block.classList.toggle("is-collapsed");
        button.textContent = collapsed ? `展开全部 · ${lineCount} 行` : "收起代码";
      });
      block.appendChild(button);
    });
  };
  mount();
  if (typeof document$ !== "undefined") document$.subscribe(mount);
})();
</script>
