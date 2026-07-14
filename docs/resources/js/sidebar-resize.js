(() => {
  const MIN_WIDTH = 240;
  const MAX_WIDTH = 480;
  const isDesktop = () =>
    window.matchMedia("(pointer: fine)").matches &&
    window.matchMedia("(min-width: 60em)").matches;

  const setup = (sidebar, direction) => {
    const handle = document.createElement("div");
    handle.className = "sidebar-resize-handle";
    sidebar.appendChild(handle);

    handle.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      const startX = event.clientX;
      const startWidth = sidebar.getBoundingClientRect().width;
      document.body.style.userSelect = "none";

      const move = (moveEvent) => {
        const delta = moveEvent.clientX - startX;
        const requested = startWidth + (direction === "left" ? delta : -delta);
        const width = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, requested));
        sidebar.style.width = `${width}px`;
        sidebar.style.flexBasis = `${width}px`;
      };
      const stop = () => {
        document.removeEventListener("pointermove", move);
        document.removeEventListener("pointerup", stop);
        document.body.style.userSelect = "";
      };
      document.addEventListener("pointermove", move);
      document.addEventListener("pointerup", stop);
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    if (!isDesktop()) return;
    const primary = document.querySelector(".md-sidebar--primary");
    const secondary = document.querySelector(".md-sidebar--secondary");
    if (primary) setup(primary, "left");
    if (secondary) setup(secondary, "right");
  });
})();
