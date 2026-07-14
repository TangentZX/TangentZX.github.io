from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class SiteContractTests(unittest.TestCase):
    def test_dependencies_are_pinned(self):
        self.assertEqual(
            (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines(),
            [
                "mkdocs==1.6.1",
                "mkdocs-material==9.6.20",
                "mkdocs-awesome-nav==3.3.0",
            ],
        )

    def test_mkdocs_identity_and_plugins(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.assertEqual(config["site_name"], "TangentZX's Blog")
        self.assertEqual(config["theme"]["name"], "material")
        self.assertEqual(config["theme"]["custom_dir"], "overrides")
        self.assertEqual(config["plugins"], ["search", "awesome-nav"])
        self.assertTrue(config["strict"])

    def test_root_navigation_order(self):
        nav = yaml.safe_load((ROOT / "docs" / ".nav.yml").read_text(encoding="utf-8"))
        self.assertEqual(
            nav["nav"],
            [
                {"首页": "index.md"},
                {"校内": "study"},
                {"CTF": "ctf"},
                {"随笔": "sth"},
                {"友链": "links"},
                {"关于": "about"},
            ],
        )

    def test_required_pages_exist(self):
        for relative in (
            "docs/index.md",
            "docs/study/index.md",
            "docs/ctf/index.md",
            "docs/sth/index.md",
            "docs/links/index.md",
            "docs/about/index.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_homepage_identity(self):
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", home)
        self.assertIn("暂无", home)
        self.assertIn("images/avatar.png", home)
        self.assertIn("https://github.com/TangentZX", home)

    def test_avatar_is_png(self):
        avatar = ROOT / "docs" / "images" / "avatar.png"
        self.assertGreater(avatar.stat().st_size, 1000)
        self.assertEqual(avatar.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_declared_theme_resources_exist(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        local_resources = [
            path
            for path in config["extra_css"] + config["extra_javascript"]
            if not path.startswith("https://")
        ]
        for relative in local_resources:
            self.assertTrue((ROOT / "docs" / relative).is_file(), relative)

    def test_theme_extension_is_minimal(self):
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
        self.assertIn('{% extends "base.html" %}', template)
        self.assertIn("{{ super() }}", template)

    def test_progressive_enhancement_markers(self):
        metrics = (ROOT / "docs/resources/js/read-metrics.js").read_text(encoding="utf-8")
        resize = (ROOT / "docs/resources/js/sidebar-resize.js").read_text(encoding="utf-8")
        self.assertIn("window.document$", metrics)
        self.assertIn("WORDS_PER_MINUTE = 300", metrics)
        self.assertIn('(pointer: fine)', resize)
        self.assertIn('(min-width: 60em)', resize)

    def test_deployment_template_is_safe_and_pinned(self):
        workflow = (ROOT / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
        self.assertIn("branches: [main]", workflow)
        self.assertIn('python-version: "3.13"', workflow)
        self.assertIn("pip install -r requirements.txt", workflow)
        self.assertIn("mkdocs gh-deploy --strict --force", workflow)

    def test_internal_project_docs_are_excluded_from_site(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.assertIn("superpowers/**", config["exclude_docs"])


if __name__ == "__main__":
    unittest.main()
