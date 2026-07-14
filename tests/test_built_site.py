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


if __name__ == "__main__":
    unittest.main()
