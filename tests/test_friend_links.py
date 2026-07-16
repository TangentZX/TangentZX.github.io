from pathlib import Path
import unittest

import yaml

from tests.mkdocs_config import load_mkdocs_config


ROOT = Path(__file__).resolve().parents[1]


class FriendLinksTests(unittest.TestCase):
    def test_final_page_contains_migrated_data(self):
        page = (ROOT / "docs/links/index.md").read_text(encoding="utf-8")
        entries = {
            "https://www.zt2misay2.cn/": "eveonecat1.jpg",
            "https://lunereal.1kal0vic.top/": "avatar_ika.jpg",
            "https://0n3-0.github.io/": "avatar_one.jpg",
            "https://kuri.jwmc.top/": "avatar_Kuri.jpg",
            "https://oldmaple.top/": "avatar_M4ple.jpg",
            "https://b1ank799.github.io/": "avatar_Blank.jpg",
            "https://lightcloveyou.github.io/": "avatar_lightc.jpg",
            "https://crisq.top/": "avatar_Crisq.jpg",
            "https://huangoxygen.github.io/": "oxygen.jpg",
            "https://dicaeopolis.github.io/": "avatar_Dicaeopolis.png",
        }
        self.assertIn('class="friend-links"', page)
        for url, avatar in entries.items():
            self.assertEqual(page.count(f'href="{url}"'), 1)
            self.assertEqual(page.count(f'src="../images/{avatar}"'), 1)
            self.assertTrue((ROOT / "docs/images" / avatar).is_file())
        self.assertEqual(page.count('target="_blank" rel="noopener noreferrer"'), 10)

    def test_final_styles_are_registered_and_preview_is_removed(self):
        config = load_mkdocs_config(ROOT)
        self.assertIn("resources/css/friend-links.css", config["extra_css"])
        css = (ROOT / "docs/resources/css/friend-links.css").read_text(encoding="utf-8")
        self.assertIn(".friend-links", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", css)
        self.assertNotIn(".friend-card::after", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn('data-md-color-scheme="slate"', css)
        self.assertFalse((ROOT / "docs/style-preview-links.md").exists())


if __name__ == "__main__":
    unittest.main()
