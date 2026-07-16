from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AboutSocialTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_material_emoji_and_about_css_are_registered(self):
        config = self.read("mkdocs.yml")
        self.assertEqual(config.count("- hooks/read_metrics.py"), 1)
        self.assertIn("- pymdownx.emoji:", config)
        self.assertIn("material.extensions.emoji.twemoji", config)
        self.assertIn("material.extensions.emoji.to_svg", config)
        self.assertIn("- resources/css/about.css", config)

    def test_about_page_contains_social_buttons(self):
        page = self.read("docs/about/index.md")
        self.assertNotIn("- **GitHub：**", page)
        self.assertIn(":simple-github: GitHub", page)
        self.assertIn("https://github.com/TangentZX", page)
        self.assertIn(":simple-bilibili: Bilibili", page)
        self.assertIn("https://space.bilibili.com/670950385", page)
        self.assertNotIn("spm_id_from", page)
        self.assertEqual(page.count('target="_blank"'), 2)
        self.assertEqual(page.count('rel="noopener noreferrer"'), 2)

    def test_about_button_styles_exist(self):
        css = self.read("docs/resources/css/about.css")
        for class_name in (
            ".about-actions",
            ".about-button",
            ".about-button--github",
            ".about-button--bilibili",
        ):
            with self.subTest(class_name=class_name):
                self.assertIn(class_name, css)


if __name__ == "__main__":
    unittest.main()
