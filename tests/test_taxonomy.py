from pathlib import Path
import tempfile
import unittest

import yaml

from hooks import taxonomy


ROOT = Path(__file__).resolve().parents[1]


class TaxonomyCollectorTests(unittest.TestCase):
    def test_section_labels_and_category_roots(self):
        self.assertEqual(
            taxonomy.SECTION_TITLES,
            {"study": "校内篇", "ctf": "CTF篇", "sth": "杂篇"},
        )
        self.assertEqual(
            taxonomy.SECTION_CATEGORY_ROOTS,
            {"study": "校内", "ctf": "CTF", "sth": "杂篇"},
        )

    def test_collects_all_migrated_taxonomy(self):
        articles = taxonomy.collect_articles(ROOT / "docs")

        self.assertGreaterEqual(len(articles), 9)
        self.assertGreaterEqual(len({path for article in articles for path in article.categories}), 8)
        self.assertGreaterEqual(len({tag for article in articles for tag in article.tags}), 18)
        self.assertEqual(
            [article.date_key for article in articles],
            sorted((article.date_key for article in articles), reverse=True),
        )

    def test_normalizes_supported_metadata_shapes(self):
        with tempfile.TemporaryDirectory() as temporary:
            docs = Path(temporary)
            study = docs / "study"
            study.mkdir()
            (study / "nested.md").write_text(
                "---\n"
                "title: Nested\n"
                "date: 2026-4-2 12:00:00\n"
                "categories: [[CTF, WP, Event]]\n"
                "tags: [CTF, WP, CTF]\n"
                "---\n",
                encoding="utf-8",
            )
            (study / "scalar.md").write_text(
                "---\n"
                "categories: Notes\n"
                "tags: Linux\n"
                "---\n",
                encoding="utf-8",
            )
            (study / "flat.md").write_text(
                "---\n"
                "title: Flat\n"
                "categories: [Notes, Python]\n"
                "tags: []\n"
                "---\n",
                encoding="utf-8",
            )

            articles = taxonomy.collect_articles(docs)
            by_title = {article.title: article for article in articles}

            self.assertEqual(by_title["Nested"].date_text, "2026-04-02")
            self.assertEqual(by_title["Nested"].categories, (("CTF", "WP", "Event"),))
            self.assertEqual(by_title["Nested"].tags, ("CTF", "WP"))
            self.assertEqual(by_title["scalar"].categories, (("Notes",),))
            self.assertEqual(by_title["scalar"].tags, ("Linux",))
            self.assertEqual(by_title["Flat"].categories, (("Notes",), ("Python",)))
            self.assertEqual(by_title["scalar"].date_key, (0, 0, 0))

    def test_renderers_emit_links_hierarchy_and_tag_cloud(self):
        articles = taxonomy.collect_articles(ROOT / "docs")

        section = taxonomy.render_article_list(
            [article for article in articles if article.section == "ctf"],
            Path("ctf"),
        )
        categories = taxonomy.render_categories(articles)
        study_tree = taxonomy.render_section_categories(articles, "study")
        tags = taxonomy.render_tags(articles)

        self.assertIn("2026-04-20", section)
        self.assertIn("WHUCTF2026_WP.md", section)
        self.assertIn('<div class="taxonomy-categories" markdown>', categories)
        self.assertIn("## CTF", categories)
        self.assertIn("### WP", categories)
        self.assertIn("## 笔记", study_tree)
        self.assertIn("### 数据结构", study_tree)
        self.assertIn("### 程序设计(A)(C)", study_tree)
        self.assertNotIn("## 校内", study_tree)
        self.assertIn('<div class="tag-cloud">', tags)
        self.assertIn('href="#tag:ctf"', tags)
        self.assertIn("<!-- material/tags -->", tags)

    def test_renders_material_native_nested_navigation(self):
        articles = taxonomy.collect_articles(ROOT / "docs")
        expected_tokens = {
            "study": ("笔记", "数据结构", "程序设计(A)(C)", "线性代数"),
            "ctf": ("WP", "WHUCTF2025新生赛", "WHUCTF2026校赛"),
            "sth": ("Linux", "流光协奏", "游记"),
        }

        for section, tokens in expected_tokens.items():
            navigation = taxonomy.render_section_navigation(articles, section)
            self.assertEqual(navigation["nav"][0], "index.md")
            rendered = yaml.safe_dump(navigation, allow_unicode=True, sort_keys=False)
            for token in tokens:
                self.assertIn(token, rendered)

    def test_category_branches_follow_their_newest_article(self):
        with tempfile.TemporaryDirectory() as temporary:
            docs = Path(temporary)
            study = docs / "study"
            study.mkdir()
            (study / "older.md").write_text(
                "---\n"
                "title: Older\n"
                "date: 2025-01-01\n"
                "categories: [[校内, A旧分类]]\n"
                "---\n",
                encoding="utf-8",
            )
            (study / "newer.md").write_text(
                "---\n"
                "title: Newer\n"
                "date: 2026-01-01\n"
                "categories: [[校内, Z新分类]]\n"
                "---\n",
                encoding="utf-8",
            )

            articles = taxonomy.collect_articles(docs)
            navigation = taxonomy.render_section_navigation(articles, "study")
            archive = taxonomy.render_categories(articles)

            self.assertEqual(
                navigation,
                {
                    "nav": [
                        "index.md",
                        {"Z新分类": ["newer.md"]},
                        {"A旧分类": ["older.md"]},
                    ]
                },
            )
            self.assertLess(archive.index("### Z新分类"), archive.index("### A旧分类"))


class TaxonomySyncTests(unittest.TestCase):
    def test_sync_is_complete_preserving_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            docs = Path(temporary)
            titles = {"study": "校内篇", "ctf": "CTF篇", "sth": "杂篇"}
            roots = {"study": "校内", "ctf": "CTF", "sth": "杂篇"}
            for section, title in titles.items():
                directory = docs / section
                directory.mkdir(parents=True)
                (directory / "index.md").write_text(
                    f"# {title}\n\n作者自定义说明。\n\n"
                    f"{taxonomy.START}\n旧列表\n{taxonomy.END}\n",
                    encoding="utf-8",
                )
                (directory / f"{section}-article.md").write_text(
                    "---\n"
                    f"title: {title}文章\n"
                    "date: 2026-7-3\n"
                    f"categories: [[{roots[section]}, 示例]]\n"
                    f"tags: [{title}, 示例]\n"
                    "---\n",
                    encoding="utf-8",
                )

            first = taxonomy.sync_taxonomy(docs)
            second = taxonomy.sync_taxonomy(docs)

            self.assertEqual(second, [])
            self.assertEqual(len(first), 8)
            for section, title in titles.items():
                index = (docs / section / "index.md").read_text(encoding="utf-8")
                nav = (docs / section / ".nav.yml").read_text(encoding="utf-8")
                self.assertIn("作者自定义说明。", index)
                self.assertIn("## 示例", index)
                self.assertIn(f"[{title}文章]", index)
                self.assertIn(f"{section}-article.md", nav)
            self.assertIn("## CTF", (docs / "archive/categories.md").read_text(encoding="utf-8"))
            self.assertIn("material/tags", (docs / "archive/tags.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
