(() => {
  let observer;
  let frame;

  const revealActiveLink = () => {
    const scrollwrap = document.querySelector(
      ".md-sidebar--secondary .md-sidebar__scrollwrap"
    );
    if (!scrollwrap) return;

    const pageTop = document.scrollingElement?.scrollTop ?? window.scrollY;
    if (pageTop <= 64) {
      scrollwrap.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    const activeLinks = scrollwrap.querySelectorAll(".md-nav__link--active");
    const active = activeLinks[activeLinks.length - 1];
    if (!active) return;

    const viewport = scrollwrap.getBoundingClientRect();
    const item = active.getBoundingClientRect();
    const padding = 12;
    const outside =
      item.top < viewport.top + padding || item.bottom > viewport.bottom - padding;

    if (outside) {
      active.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" });
    }
  };

  const scheduleReveal = () => {
    if (frame) cancelAnimationFrame(frame);
    frame = requestAnimationFrame(revealActiveLink);
  };

  const initialize = () => {
    observer?.disconnect();
    if (frame) cancelAnimationFrame(frame);

    const scrollwrap = document.querySelector(
      ".md-sidebar--secondary .md-sidebar__scrollwrap"
    );
    if (!scrollwrap) return;

    observer = new MutationObserver(scheduleReveal);
    observer.observe(scrollwrap, {
      attributes: true,
      attributeFilter: ["class"],
      subtree: true,
    });
    scheduleReveal();
  };

  window.addEventListener("hashchange", scheduleReveal);
  window.addEventListener("scroll", scheduleReveal, { passive: true });
  if (window.document$?.subscribe) window.document$.subscribe(initialize);
  else document.addEventListener("DOMContentLoaded", initialize);
})();
