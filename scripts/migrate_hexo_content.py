from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil

IMAGE_LINK = re.compile(
    r"(!\[[^\]]*\]\()(/images/.+?\.(?:png|jpe?g|gif|webp|svg))(\))",
    re.IGNORECASE,
)


def _split_front_matter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("article is missing YAML Front Matter")
    end = normalized.find("\n---\n", 4)
    if end == -1:
        raise ValueError("article has unterminated YAML Front Matter")
    return normalized[4:end], normalized[end + 5 :]


def _title_from_front_matter(front_matter: str) -> str:
    match = re.search(r"(?m)^title:\s*(.+?)\s*$", front_matter)
    if not match:
        raise ValueError("article Front Matter is missing title")
    return match.group(1).strip().strip("\"'")


def _has_matching_h1(body: str, title: str) -> bool:
    fenced = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced and stripped.startswith("# "):
            if stripped[2:].strip() == title:
                return True
    return False


def normalize_article(text: str) -> str:
    front_matter, body = _split_front_matter(text)
    front_matter = re.sub(
        r"(?m)^catagories:", "categories:", front_matter
    )
    title = _title_from_front_matter(front_matter)
    body = IMAGE_LINK.sub(r"\1<\2>\3", body)
    body = body.lstrip("\n")
    if not _has_matching_h1(body, title):
        body = f"# {title}\n\n{body}"
    return f"---\n{front_matter}\n---\n\n{body.rstrip()}\n"


ARTICLE_MAP = (
    ("source/_posts/Tzxy's WHUCTF2025新生赛WP.md", "docs/ctf/Tzxy's WHUCTF2025新生赛WP.md"),
    ("source/_posts/WHUCTF2026_WP.md", "docs/ctf/WHUCTF2026_WP.md"),
    ("source/_posts/程序设计(A)(C)作业.md", "docs/study/程序设计(A)(C)作业.md"),
    ("source/_posts/线性代数-矩阵笔记.md", "docs/study/线性代数-矩阵笔记.md"),
    ("source/_posts/数据结构复习整理.md", "docs/study/数据结构复习整理.md"),
    ("source/_posts/数据结构实验复习.md", "docs/study/数据结构实验复习.md"),
    ("source/_posts/ArchLinux 折腾心得.md", "docs/sth/ArchLinux 折腾心得.md"),
    ("source/_posts/流光协奏之梦.md", "docs/sth/流光协奏之梦.md"),
    ("source/_posts/郑州强网论坛 学习心得.md", "docs/sth/郑州强网论坛 学习心得.md"),
)

SECTION_INDEXES = {
    "docs/ctf/index.md": """# CTF

- 2026-04-20 · [CTF辞のWHUCTF2026校赛WP](<WHUCTF2026_WP.md>)
- 2025-10-24 · [Tzxy's WHUCTF2025新生赛WP](<Tzxy's WHUCTF2025新生赛WP.md>)
""",
    "docs/study/index.md": """# 校内

- 2026-07-02 · [数据结构实验复习整理](<数据结构实验复习.md>)
- 2026-06-26 · [数据结构复习整理](<数据结构复习整理.md>)
- 2025-10-09 · [程序设计(A)(C)作业](<程序设计(A)(C)作业.md>)
- 2025-10-02 · [线性代数_矩阵笔记](<线性代数-矩阵笔记.md>)
""",
    "docs/sth/index.md": """# 随笔

- 2025-12-27 · [流光协奏之梦](<流光协奏之梦.md>)
- 2025-11-28 · [ArchLinux 折腾心得](<ArchLinux 折腾心得.md>)
- 2025-11-23 · [郑州游记](<郑州强网论坛 学习心得.md>)
""",
}


def migrate(source_blog: Path, target_blog: Path) -> None:
    for source_relative, target_relative in ARTICLE_MAP:
        source = source_blog / source_relative
        if not source.is_file():
            raise FileNotFoundError(source)
        target = target_blog / target_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            normalize_article(source.read_text(encoding="utf-8")),
            encoding="utf-8",
            newline="\n",
        )

    source_images = source_blog / "source" / "images"
    target_images = target_blog / "docs" / "images"
    for source in source_images.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(source_images)
        if relative == Path("avatar.png"):
            continue
        target = target_images / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    for relative, content in SECTION_INDEXES.items():
        (target_blog / relative).write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_blog", type=Path)
    parser.add_argument("target_blog", type=Path)
    args = parser.parse_args()
    migrate(args.source_blog.resolve(), args.target_blog.resolve())


if __name__ == "__main__":
    main()
