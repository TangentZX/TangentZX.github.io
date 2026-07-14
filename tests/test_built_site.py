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
            "links/index.html",
            "about/index.html",
        ):
            self.assertTrue((SITE / relative).is_file(), relative)

    def test_homepage_contains_identity_and_assets(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", html)
        self.assertIn("暂无", html)
        self.assertIn("images/avatar.png", html)
        self.assertIn("resources/css/extra.css", html)
        self.assertIn("resources/js/read-metrics.js", html)

    def test_navigation_labels_are_rendered(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        for label in ("首页", "校内", "CTF", "随笔", "友链", "关于"):
            self.assertIn(label, html)

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
