from pathlib import Path
import tempfile
import unittest

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
            {"study": "校内", "ctf": "CTF", "sth": "随笔"},
        )

    def test_collects_all_migrated_taxonomy(self):
        articles = taxonomy.collect_articles(ROOT / "docs")

        self.assertEqual(len(articles), 9)
        self.assertEqual(len({path for article in articles for path in article.categories}), 8)
        self.assertEqual(len({tag for article in articles for tag in article.tags}), 18)
        self.assertEqual(sum(len(article.tags) for article in articles), 24)
        self.assertEqual(articles[0].title, "数据结构实验复习整理")
        self.assertEqual(articles[0].date_text, "2026-07-02")

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

        self.assertEqual(
            taxonomy.render_section_navigation(articles, "study"),
            {
                "nav": [
                    "index.md",
                    {
                        "笔记": [
                            {
                                "数据结构": [
                                    "数据结构实验复习.md",
                                    "数据结构复习整理.md",
                                ]
                            },
                            {"程序设计(A)(C)": ["程序设计(A)(C)作业.md"]},
                            {"线性代数": ["线性代数-矩阵笔记.md"]},
                        ]
                    },
                ]
            },
        )
        self.assertEqual(
            taxonomy.render_section_navigation(articles, "ctf"),
            {
                "nav": [
                    "index.md",
                    {
                        "WP": [
                            {"WHUCTF2025新生赛": ["Tzxy's WHUCTF2025新生赛WP.md"]},
                            {"WHUCTF2026校赛": ["WHUCTF2026_WP.md"]},
                        ]
                    },
                ]
            },
        )
        self.assertEqual(
            taxonomy.render_section_navigation(articles, "sth"),
            {
                "nav": [
                    "index.md",
                    {"Linux": ["ArchLinux 折腾心得.md"]},
                    {"流光协奏": ["流光协奏之梦.md"]},
                    {"游记": ["郑州强网论坛 学习心得.md"]},
                ]
            },
        )


class TaxonomySyncTests(unittest.TestCase):
    def test_sync_is_complete_preserving_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            docs = Path(temporary)
            titles = {"study": "校内篇", "ctf": "CTF篇", "sth": "杂篇"}
            roots = {"study": "校内", "ctf": "CTF", "sth": "随笔"}
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
