from pathlib import Path
import re
import unittest

import yaml

from tests.mkdocs_config import load_mkdocs_config


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
        config = load_mkdocs_config(ROOT)
        self.assertEqual(config["site_name"], "TangentZX's Blog")
        self.assertNotIn("repo_url", config)
        self.assertEqual(config["theme"]["name"], "material")
        self.assertEqual(config["theme"]["custom_dir"], "overrides")
        self.assertEqual(config["plugins"], ["search", "material/tags", "awesome-nav"])
        self.assertIn("hooks/taxonomy.py", config["hooks"])
        self.assertIn("resources/css/taxonomy.css", config["extra_css"])
        self.assertTrue(config["strict"])

    def test_root_navigation_order(self):
        nav = yaml.safe_load((ROOT / "docs" / ".nav.yml").read_text(encoding="utf-8"))
        self.assertEqual(
            nav["nav"],
            [
                {"首页": "index.md"},
                {"校内篇": "study"},
                {"CTF篇": "ctf"},
                {"杂篇": "sth"},
                {"归档": "archive"},
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
            "docs/archive/index.md",
            "docs/archive/categories.md",
            "docs/archive/tags.md",
            "docs/links/index.md",
            "docs/about/index.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_homepage_identity(self):
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("TangentZX's Blog", home)
        self.assertIn("校内学习、CTF", home)
        self.assertIn("[关于](/about)", home)
        self.assertIn("images/洛天依壁纸.png", home)
        self.assertIn("images/洛天依壁纸_夜.png", home)

    def test_about_page_contains_migrated_profile(self):
        about = (ROOT / "docs/about/index.md").read_text(encoding="utf-8")
        for text in (
            "Tangent丶ZX",
            "我怎会不知你挚爱纯蓝。",
            "CTF ID",
            "1so",
            "武汉大学",
            "武汉",
            "tangentzx@hotmail.com",
            "https://github.com/TangentZX",
        ):
            self.assertIn(text, about)

    def test_avatar_is_png(self):
        avatar = ROOT / "docs" / "images" / "avatar.png"
        self.assertGreater(avatar.stat().st_size, 1000)
        self.assertEqual(avatar.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_declared_theme_resources_exist(self):
        config = load_mkdocs_config(ROOT)
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

    def test_primary_sidebar_uses_material_active_rail(self):
        css = (ROOT / "docs/resources/css/leftsidebar.css").read_text(encoding="utf-8")
        self.assertIn("a.md-nav__link--active::before", css)
        self.assertIn("#6171f5", css)
        self.assertIn("#7dafe9", css)
        self.assertIn("prefers-reduced-motion: reduce", css)

    def test_taxonomy_uses_connected_tree_styles(self):
        css = (ROOT / "docs/resources/css/taxonomy.css").read_text(encoding="utf-8")

        for token in (
            "--taxonomy-accent: #6171f5",
            "--taxonomy-accent: #7dafe9",
            "--taxonomy-hover: rgba(97, 113, 245, 0.08)",
            "--taxonomy-hover: rgba(125, 175, 233, 0.12)",
            ".taxonomy-categories h2",
            ".taxonomy-categories h3::before",
            ".taxonomy-categories h4::before",
            ".taxonomy-categories ul > li::before",
            "grid-template-columns: 6.4rem 0.6rem minmax(0, 1fr)",
            ".taxonomy-article__date",
            ".taxonomy-categories li:focus-within",
            "background-color: var(--taxonomy-hover)",
            "@media (max-width: 44rem)",
            "grid-template-columns: 5.35rem minmax(0, 1fr)",
        ):
            self.assertIn(token, css)

    def test_taxonomy_branch_colors_follow_heading_depth(self):
        css = (ROOT / "docs/resources/css/taxonomy.css").read_text(encoding="utf-8")

        depth_values = re.findall(
            r"--taxonomy-branch-h[2-6]: ([^;]+);",
            css,
        )
        self.assertEqual(
            depth_values,
            [
                "#6171f5",
                "rgba(97, 113, 245, 0.30)",
                "rgba(97, 113, 245, 0.24)",
                "rgba(97, 113, 245, 0.18)",
                "rgba(97, 113, 245, 0.12)",
                "#7dafe9",
                "rgba(125, 175, 233, 0.36)",
                "rgba(125, 175, 233, 0.29)",
                "rgba(125, 175, 233, 0.22)",
                "rgba(125, 175, 233, 0.15)",
            ],
        )
        self.assertEqual(len(set(depth_values[:5])), 5)
        self.assertEqual(len(set(depth_values[5:])), 5)

        for level in range(2, 7):
            self.assertRegex(
                css,
                rf"(?s)\.taxonomy-categories h{level} \{{[^}}]*"
                rf"border-left: [^;]+var\(--taxonomy-branch-h{level}\)",
            )
            self.assertRegex(
                css,
                rf"(?s)\.taxonomy-categories h{level} \+ ul \{{[^}}]*"
                rf"border-left-color: var\(--taxonomy-branch-h{level}\)",
            )

        for level in range(3, 7):
            self.assertRegex(
                css,
                rf"(?s)\.taxonomy-categories h{level}::before \{{[^}}]*"
                rf"border-top-color: var\(--taxonomy-branch-h{level}\)",
            )

    def test_secondary_toc_follows_the_active_heading(self):
        config = load_mkdocs_config(ROOT)
        self.assertIn("resources/css/article-content.css", config["extra_css"])
        self.assertIn("resources/js/toc-follow.js", config["extra_javascript"])

        css = (ROOT / "docs/resources/css/article-content.css").read_text(encoding="utf-8")
        script = (ROOT / "docs/resources/js/toc-follow.js").read_text(encoding="utf-8")
        self.assertIn(".md-sidebar--secondary .md-sidebar__scrollwrap", css)
        self.assertIn("overflow-y: auto", css)
        self.assertIn("MutationObserver", script)
        self.assertIn(".md-nav__link--active", script)
        self.assertIn('block: "nearest"', script)
        self.assertIn("window.document$", script)
        self.assertIn('window.addEventListener("scroll"', script)
        self.assertIn("scrollwrap.scrollTo", script)

    def test_selected_article_styles_are_global(self):
        config = load_mkdocs_config(ROOT)
        self.assertIn("resources/js/code-fold.js", config["extra_javascript"])
        highlight = next(
            item["pymdownx.highlight"]
            for item in config["markdown_extensions"]
            if isinstance(item, dict) and "pymdownx.highlight" in item
        )
        self.assertTrue(highlight["auto_title"])

        css = (ROOT / "docs/resources/css/article-content.css").read_text(encoding="utf-8")
        fold = (ROOT / "docs/resources/js/code-fold.js").read_text(encoding="utf-8")
        self.assertIn(".md-typeset .highlight", css)
        self.assertIn(".md-typeset :not(pre) > code", css)
        self.assertIn(".md-typeset blockquote", css)
        self.assertIn(".md-typeset__table table:not([class])", css)
        self.assertIn("Maple Mono CN", css)
        self.assertIn("--article-code-bg-light", css)
        self.assertIn("border-left-color: #6171f5 !important", css)
        self.assertIn("border-left-color: #7dafe9 !important", css)
        self.assertIn("lineCount <= 32", fold)
        self.assertIn("window.document$", fold)

    def test_highlight_and_strikethrough_extensions_are_enabled(self):
        config = load_mkdocs_config(ROOT)
        self.assertIn("pymdownx.mark", config["markdown_extensions"])
        self.assertIn("pymdownx.tilde", config["markdown_extensions"])

    def test_deployment_template_is_safe_and_pinned(self):
        workflow = (ROOT / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
        self.assertIn("branches: [main]", workflow)
        self.assertIn('python-version: "3.13"', workflow)
        self.assertIn("pip install -r requirements.txt", workflow)
        self.assertIn("mkdocs gh-deploy --strict --force", workflow)

    def test_internal_project_docs_are_excluded_from_site(self):
        config = load_mkdocs_config(ROOT)
        self.assertIn("superpowers/**", config["exclude_docs"])


if __name__ == "__main__":
    unittest.main()
