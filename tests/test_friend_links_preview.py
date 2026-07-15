from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FriendLinksPreviewTests(unittest.TestCase):
    def test_preview_contains_migrated_data(self):
        preview = (ROOT / "docs/style-preview-links.md").read_text(encoding="utf-8")
        for marker in ("friends-a", "friends-b", "friends-c"):
            self.assertIn(marker, preview)

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
        for url, avatar in entries.items():
            self.assertEqual(preview.count(f'href="{url}"'), 3)
            self.assertEqual(preview.count(f'src="../images/{avatar}"'), 3)
            self.assertTrue((ROOT / "docs/images" / avatar).is_file())
        self.assertEqual(
            preview.count('target="_blank" rel="noopener noreferrer"'), 30
        )


if __name__ == "__main__":
    unittest.main()
