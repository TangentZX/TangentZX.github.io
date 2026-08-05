from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from html import escape
from pathlib import Path
import posixpath
import re

from pymdownx.slugs import slugify
import yaml


SECTION_TITLES = {"study": "校内篇", "ctf": "CTF篇", "sth": "杂篇"}
SECTION_CATEGORY_ROOTS = {"study": "校内", "ctf": "CTF", "sth": "杂篇"}
START = "<!-- taxonomy:articles:start -->"
END = "<!-- taxonomy:articles:end -->"


@dataclass(frozen=True)
class Article:
    path: Path
    title: str
    date_text: str
    date_key: tuple[int, int, int]
    categories: tuple[tuple[str, ...], ...]
    tags: tuple[str, ...]
    section: str


def _front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def _normalize_date(value: object) -> tuple[str, tuple[int, int, int]]:
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value.isoformat(), (value.year, value.month, value.day)

    match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", str(value or ""))
    if not match:
        return "", (0, 0, 0)
    year, month, day = map(int, match.groups())
    try:
        normalized = date(year, month, day)
    except ValueError:
        return "", (0, 0, 0)
    return normalized.isoformat(), (year, month, day)


def _normalize_categories(value: object) -> tuple[tuple[str, ...], ...]:
    if isinstance(value, str):
        return ((value.strip(),),) if value.strip() else ()
    if not isinstance(value, list):
        return ()

    paths: list[tuple[str, ...]] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            paths.append((item.strip(),))
        elif isinstance(item, list):
            path = tuple(str(part).strip() for part in item if str(part).strip())
            if path:
                paths.append(path)
    return tuple(dict.fromkeys(paths))


def _normalize_tags(value: object) -> tuple[str, ...]:
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, list):
        return ()
    tags = [str(tag).strip() for tag in values if str(tag).strip()]
    return tuple(dict.fromkeys(tags))


def collect_articles(docs_dir: Path) -> list[Article]:
    articles: list[Article] = []
    for section in SECTION_TITLES:
        directory = docs_dir / section
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
            if path.name == "index.md":
                continue
            metadata = _front_matter(path)
            date_text, date_key = _normalize_date(metadata.get("date"))
            articles.append(
                Article(
                    path=path.relative_to(docs_dir),
                    title=str(metadata.get("title") or path.stem),
                    date_text=date_text,
                    date_key=date_key,
                    categories=_normalize_categories(metadata.get("categories")),
                    tags=_normalize_tags(metadata.get("tags")),
                    section=section,
                )
            )

    articles.sort(key=lambda article: article.title.casefold())
    articles.sort(key=lambda article: article.date_key, reverse=True)
    return articles


def _relative_link(article: Article, base_dir: Path) -> str:
    return posixpath.relpath(article.path.as_posix(), base_dir.as_posix())


def render_article_list(articles: list[Article], base_dir: Path) -> str:
    lines = []
    for article in articles:
        date_markup = (
            f'<time class="taxonomy-article__date" datetime="{escape(article.date_text)}">'
            f'{escape(article.date_text)}</time>'
            if article.date_text
            else '<span class="taxonomy-article__date">未注明日期</span>'
        )
        link = _relative_link(article, base_dir)
        lines.append(
            f'- {date_markup}'
            '<span class="taxonomy-article__separator" aria-hidden="true">·</span>'
            f'[{article.title}](<{link}>)'
        )
    return "\n".join(lines)


def _build_category_tree(articles: list[Article], select_path) -> dict:
    tree: dict = {}
    for article in articles:
        for path in article.categories:
            selected = select_path(path)
            if selected is None:
                continue
            node = tree
            for part in selected:
                node = node.setdefault(part, {})
            node.setdefault("__articles__", []).append(article)
    return tree


def _render_category_tree(tree: dict, base_dir: Path) -> str:
    lines: list[str] = []

    if tree.get("__articles__"):
        lines.append(render_article_list(tree["__articles__"], base_dir))

    def visit(node: dict, depth: int) -> None:
        for name in (key for key in node if key != "__articles__"):
            child = node[name]
            lines.extend(("", f"{'#' * min(depth + 2, 6)} {name}", ""))
            if child.get("__articles__"):
                lines.append(render_article_list(child["__articles__"], base_dir))
            visit(child, depth + 1)

    visit(tree, 0)
    return "\n".join(lines).strip()


def _wrap_category_tree(tree: dict, base_dir: Path) -> str:
    content = _render_category_tree(tree, base_dir) or "暂无分类文章。"
    return f'<div class="taxonomy-categories" markdown>\n\n{content}\n\n</div>'


def render_categories(articles: list[Article]) -> str:
    tree = _build_category_tree(articles, lambda path: path)
    return _wrap_category_tree(tree, Path("archive"))


def _build_section_category_tree(articles: list[Article], section: str) -> dict:
    root = SECTION_CATEGORY_ROOTS[section]
    return _build_category_tree(
        articles,
        lambda path: path[1:] if path and path[0] == root else None,
    )


def render_section_categories(articles: list[Article], section: str) -> str:
    tree = _build_section_category_tree(articles, section)
    return _wrap_category_tree(tree, Path(section))


def _navigation_items(node: dict) -> list:
    items = [article.path.name for article in node.get("__articles__", [])]
    for name in (key for key in node if key != "__articles__"):
        items.append({name: _navigation_items(node[name])})
    return items


def render_section_navigation(articles: list[Article], section: str) -> dict:
    tree = _build_section_category_tree(articles, section)
    return {"nav": ["index.md", *_navigation_items(tree)]}


def render_tags(articles: list[Article]) -> str:
    counts = Counter(tag for article in articles for tag in article.tags)
    if not counts:
        return '<div class="tag-cloud"></div>\n\n<!-- material/tags -->'

    minimum, maximum = min(counts.values()), max(counts.values())
    make_slug = slugify(case="lower")
    links = []
    for tag in sorted(counts, key=str.casefold):
        count = counts[tag]
        weight = 3 if minimum == maximum else 1 + round((count - minimum) * 4 / (maximum - minimum))
        anchor = make_slug(tag, "-")
        links.append(
            f'  <a class="tag-weight-{weight}" href="#tag:{escape(anchor)}">'
            f'{escape(tag)}<span>{count}</span></a>'
        )
    return "\n".join(("<div class=\"tag-cloud\">", *links, "</div>", "", "<!-- material/tags -->"))


def _replace_block(source: str, generated: str) -> str:
    block = f"{START}\n{generated.rstrip()}\n{END}"
    if START in source and END in source:
        start = source.index(START)
        finish = source.index(END, start) + len(END)
        before = source[:start].rstrip()
        after = source[finish:].strip()
        parts = [part for part in (before, block, after) if part]
        return "\n\n".join(parts) + "\n"
    return f"{source.rstrip()}\n\n{block}\n"


def _write_if_changed(path: Path, content: str) -> bool:
    content = content.rstrip() + "\n"
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def _archive_page(title: str, introduction: str, content: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{introduction}\n\n"
        "<!-- 此页由 hooks/taxonomy.py 自动生成，请修改文章 front matter。 -->\n\n"
        f"{content.rstrip()}\n"
    )


def sync_taxonomy(docs_dir: Path) -> list[Path]:
    articles = collect_articles(docs_dir)
    changed: list[Path] = []

    for section in SECTION_TITLES:
        directory = docs_dir / section
        if not directory.is_dir():
            continue
        section_articles = [article for article in articles if article.section == section]
        index_path = directory / "index.md"
        source = index_path.read_text(encoding="utf-8") if index_path.is_file() else f"# {SECTION_TITLES[section]}\n"
        generated = render_section_categories(section_articles, section)
        if _write_if_changed(index_path, _replace_block(source, generated)):
            changed.append(index_path)

        navigation = render_section_navigation(section_articles, section)
        nav_text = yaml.safe_dump(navigation, allow_unicode=True, sort_keys=False)
        nav_path = directory / ".nav.yml"
        if _write_if_changed(nav_path, nav_text):
            changed.append(nav_path)

    categories_path = docs_dir / "archive" / "categories.md"
    categories_page = _archive_page(
        "分类",
        "按文章 front matter 中的分类路径整理。",
        render_categories(articles),
    )
    if _write_if_changed(categories_path, categories_page):
        changed.append(categories_path)

    tags_path = docs_dir / "archive" / "tags.md"
    tags_page = _archive_page(
        "标签",
        "标签字号根据其在文章中的出现次数调整。",
        render_tags(articles),
    )
    if _write_if_changed(tags_path, tags_page):
        changed.append(tags_path)

    return changed


def on_config(config, **kwargs):
    sync_taxonomy(Path(config.docs_dir))
    return config


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    updates = sync_taxonomy(root / "docs")
    if updates:
        for update in updates:
            print(f"taxonomy: updated {update.relative_to(root)}")
    else:
        print("taxonomy: no changes")
