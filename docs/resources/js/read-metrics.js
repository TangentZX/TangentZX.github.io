(() => {
  const WORDS_PER_MINUTE = 300;

  const buildMetrics = () => {
    const article = document.querySelector("article.md-content__inner");
    if (!article) return;
    article.querySelector(".reading-metrics")?.remove();
    if (article.querySelector('[data-read-metrics="hidden"]')) return;

    const text = article.innerText || "";
    const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    const latin = (text.match(/[A-Za-z0-9]+/g) || []).length;
    const words = cjk + latin;
    if (!words) return;

    const metrics = document.createElement("div");
    metrics.className = "reading-metrics";
    metrics.innerHTML = `<span>阅读时长 ${Math.max(1, Math.ceil(words / WORDS_PER_MINUTE))} 分钟</span><span>字数 ${words}</span>`;
    const heading = article.querySelector("h1");
    heading?.insertAdjacentElement("afterend", metrics);
  };

  if (window.document$?.subscribe) window.document$.subscribe(buildMetrics);
  else document.addEventListener("DOMContentLoaded", buildMetrics);
})();
