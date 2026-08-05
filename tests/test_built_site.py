from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class BuiltSiteTests(unittest.TestCase):
    def test_expected_pages_are_built(self):
        for relative in (
            "index.html",
            "study/index.html",
            "ctf/index.html",
            "sth/index.html",
            "archive/index.html",
            "archive/categories/index.html",
            "archive/tags/index.html",
            "links/index.html",
            "about/index.html",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

    def test_homepage_contains_identity_and_assets(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", html)
        self.assertIn("images/洛天依壁纸.png", html)
        self.assertIn("images/洛天依壁纸_夜.png", html)
        self.assertIn("resources/css/extra.css", html)
        self.assertIn("resources/js/read-metrics.js", html)
        self.assertNotIn('class="md-source"', html)

    def test_about_contains_github_profile(self):
        html = (SITE / "about/index.html").read_text(encoding="utf-8")
        self.assertIn("https://github.com/TangentZX", html)

    def test_material_expands_only_the_active_category_path(self):
        html = (SITE / "study/数据结构复习整理/index.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(html.count('aria-expanded="true"'), 3)
        self.assertIn('aria-expanded="false"', html)
        self.assertIn("程序设计(A)(C)", html)

    def test_navigation_labels_are_rendered(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        for label in ("首页", "校内篇", "CTF篇", "杂篇", "归档", "友链", "关于"):
            self.assertIn(label, html)

    def test_chapter_indexes_render_category_subtrees(self):
        expected = {
            "study/index.html": ("课程学习、作业与笔记", "笔记", "程序设计(A)(C)"),
            "ctf/index.html": ("比赛记录、题解与复盘", "WP", "WHUCTF2026校赛"),
            "sth/index.html": ("技术折腾、游记与一些随手记录", "Linux", "流光协奏"),
        }
        for relative, labels in expected.items():
            html = (SITE / relative).read_text(encoding="utf-8")
            self.assertIn("taxonomy-categories", html)
            for label in labels:
                self.assertIn(label, html)

    def test_taxonomy_article_rows_keep_semantic_dates_in_built_html(self):
        for relative in (
            "study/index.html",
            "ctf/index.html",
            "sth/index.html",
            "archive/categories/index.html",
        ):
            html = (SITE / relative).read_text(encoding="utf-8")
            self.assertIn('class="taxonomy-article__date"', html, relative)
            self.assertIn('class="taxonomy-article__separator"', html, relative)
            self.assertRegex(
                html,
                r'<time class="taxonomy-article__date" datetime="\d{4}-\d{2}-\d{2}">',
            )

    def test_taxonomy_archive_is_rendered(self):
        categories = (SITE / "archive/categories/index.html").read_text(encoding="utf-8")
        tags = (SITE / "archive/tags/index.html").read_text(encoding="utf-8")

        self.assertIn("taxonomy-categories", categories)
        for label in ("校内", "笔记", "数据结构", "CTF", "WP", "杂篇"):
            self.assertIn(label, categories)

        self.assertIn("tag-cloud", tags)
        self.assertIn('id="tag:ctf"', tags)
        self.assertIn('class="md-tag"', tags)
        self.assertNotIn("<!-- material/tags -->", tags)
        for label in (
            "AI",
            "ArchLinux",
            "CTF",
            "C语言",
            "Hyprland",
            "Niri",
            "WHUCTF2025新生赛",
            "WHUCTF2026校赛",
            "WP",
            "作业",
            "强网论坛",
            "数据结构",
            "洛天依",
            "流光协奏",
            "矩阵",
            "程序设计",
            "笔记",
            "线性代数",
        ):
            self.assertIn(label, tags)

    def test_article_tags_link_back_to_the_archive(self):
        html = (SITE / "study/数据结构复习整理/index.html").read_text(encoding="utf-8")
        self.assertIn('<nav class="md-tags"', html)
        self.assertIn("archive/tags/#tag:数据结构", html)

    def test_migrated_article_pages_are_built(self):
        article_paths = (
            "ctf/Tzxy's WHUCTF2025新生赛WP/index.html",
            "ctf/WHUCTF2026_WP/index.html",
            "study/程序设计(A)(C)作业/index.html",
            "study/线性代数-矩阵笔记/index.html",
            "study/数据结构复习整理/index.html",
            "study/数据结构实验复习/index.html",
            "sth/ArchLinux 折腾心得/index.html",
            "sth/流光协奏之梦/index.html",
            "sth/郑州强网论坛 学习心得/index.html",
        )
        for relative in article_paths:
            self.assertTrue((SITE / relative).is_file(), relative)

    def test_every_legacy_image_is_emitted(self):
        source_images = Path(r"D:\Project\my-blog\source\images")
        built_images = SITE / "images"
        for source in source_images.rglob("*"):
            if source.is_file():
                relative = source.relative_to(source_images)
                self.assertTrue((built_images / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
