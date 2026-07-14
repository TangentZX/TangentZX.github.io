from __future__ import annotations

import re

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
