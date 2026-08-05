(() => {
  const mountCodeFolding = () => {
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

  if (window.document$?.subscribe) window.document$.subscribe(mountCodeFolding);
  else document.addEventListener("DOMContentLoaded", mountCodeFolding);
})();
