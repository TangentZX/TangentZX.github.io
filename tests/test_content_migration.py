from pathlib import Path
import re
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.migrate_hexo_content import ARTICLE_MAP, normalize_article
from hooks import taxonomy


class MarkdownTransformationTests(unittest.TestCase):
    def test_normalizes_front_matter_title_and_image_destination(self):
        source = """---
title: Demo
catagories:
- [随便写写]
---
正文
![图片](/images/程序设计(A)(C)/示例.png)
"""
        result = normalize_article(source)
        self.assertNotIn("catagories:", result)
        self.assertIn("categories:", result)
        self.assertIn("\n# Demo\n", result)
        self.assertIn("![图片](</images/程序设计(A)(C)/示例.png>)", result)

    def test_does_not_duplicate_matching_h1_or_rewrite_plain_urls(self):
        source = """---
title: Demo
---
# Demo
http://127.0.0.1:12961/images/flag.txt
"""
        result = normalize_article(source)
        self.assertEqual(result.count("# Demo"), 1)
        self.assertIn("http://127.0.0.1:12961/images/flag.txt", result)


class MigratedRepositoryTests(unittest.TestCase):
    source_blog = Path(r"D:\Project\my-blog")
    target_blog = ROOT

    def test_all_mapped_articles_exist_and_are_normalized(self):
        self.assertEqual(len(ARTICLE_MAP), 9)
        for source_relative, target_relative in ARTICLE_MAP:
            self.assertTrue((self.source_blog / source_relative).is_file())
            target = self.target_blog / target_relative
            self.assertTrue(target.is_file(), target_relative)
            text = target.read_text(encoding="utf-8")
            self.assertNotIn("catagories:", text)
            self.assertNotRegex(text, r"!\[[^\]]*\]\(/images/")
            front_matter = text.split("---", 2)[1]
            metadata = yaml.safe_load(front_matter)
            self.assertIn("title", metadata)
            self.assertIn(f"# {metadata['title']}", text)

            image_refs = re.findall(
                r"!\[[^\]]*\]\(<(/images/.+?\.(?:png|jpe?g|gif|webp|svg))>\)",
                text,
                flags=re.IGNORECASE,
            )
            for image_ref in image_refs:
                image_target = self.target_blog / "docs" / image_ref.lstrip("/")
                self.assertTrue(image_target.is_file(), image_ref)

    def test_article_authors_and_category_paths(self):
        expected = {
            "docs/study/程序设计(A)(C)作业.md": (
                "Tangent丶ZX",
                [["校内", "笔记", "程序设计(A)(C)"]],
            ),
            "docs/study/线性代数-矩阵笔记.md": (
                "Tangent丶ZX",
                [["校内", "笔记", "线性代数"]],
            ),
            "docs/study/数据结构复习整理.md": (
                "Tangent丶ZX",
                [["校内", "笔记", "数据结构"]],
            ),
            "docs/study/数据结构实验复习.md": (
                "Tangent丶ZX",
                [["校内", "笔记", "数据结构"]],
            ),
            "docs/ctf/Tzxy's WHUCTF2025新生赛WP.md": (
                "1so",
                [["CTF", "WP", "WHUCTF2025新生赛"]],
            ),
            "docs/ctf/WHUCTF2026_WP.md": (
                "1so",
                [["CTF", "WP", "WHUCTF2026校赛"]],
            ),
            "docs/sth/ArchLinux 折腾心得.md": (
                "Tangent丶ZX",
                [["杂篇", "Linux"]],
            ),
            "docs/sth/流光协奏之梦.md": (
                "Tangent丶ZX",
                [["杂篇", "流光协奏"]],
            ),
            "docs/sth/郑州强网论坛 学习心得.md": (
                "Tangent丶ZX",
                [["杂篇", "游记"]],
            ),
        }

        self.assertEqual(len(expected), 9)
        for relative, (author, categories) in expected.items():
            text = (self.target_blog / relative).read_text(encoding="utf-8")
            metadata = yaml.safe_load(text.split("---", 2)[1])
            self.assertEqual(metadata.get("author"), author, relative)
            self.assertEqual(metadata.get("categories"), categories, relative)

    def test_every_legacy_image_is_copied_byte_for_byte(self):
        source_root = self.source_blog / "source" / "images"
        target_root = self.target_blog / "docs" / "images"
        source_files = sorted(p for p in source_root.rglob("*") if p.is_file())
        self.assertEqual(len(source_files), 131)
        for source in source_files:
            target = target_root / source.relative_to(source_root)
            self.assertTrue(target.is_file(), target)
            self.assertEqual(source.read_bytes(), target.read_bytes(), target)
        self.assertTrue((target_root / "avatar.png").is_file())

    def test_section_indexes_link_every_migrated_article(self):
        for _, target_relative in ARTICLE_MAP:
            target = Path(target_relative)
            index = self.target_blog / target.parent / "index.md"
            self.assertIn(target.name, index.read_text(encoding="utf-8"))

    def test_section_navigation_is_newest_first(self):
        articles = taxonomy.collect_articles(self.target_blog / "docs")
        for section in taxonomy.SECTION_TITLES:
            nav_path = self.target_blog / "docs" / section / ".nav.yml"
            navigation = yaml.safe_load(nav_path.read_text(encoding="utf-8"))
            expected_navigation = taxonomy.render_section_navigation(
                [article for article in articles if article.section == section],
                section,
            )
            self.assertEqual(navigation, expected_navigation)


if __name__ == "__main__":
    unittest.main()
