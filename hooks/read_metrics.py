from __future__ import annotations


MARKER = '<span data-read-metrics="hidden" hidden></span>'


def _hidden_features(page) -> set[str]:
    value = (getattr(page, "meta", None) or {}).get("hide", [])
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {str(item) for item in value}
    return set()


def on_page_content(html, page, config, files, **kwargs):
    if "read-metrics" not in _hidden_features(page):
        return html
    return f"{MARKER}\n{html}"
