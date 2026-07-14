from pathlib import Path
import re
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.migrate_hexo_content import normalize_article


class MarkdownTransformationTests(unittest.TestCase):
    def test_normalizes_front_matter_title_and_image_destination(self):
        source = """---
title: Demo
catagories:
- [随便写写]
---
正文
![图片](/images/程序设计(A)(C)/示例.png)
"""
        result = normalize_article(source)
        self.assertNotIn("catagories:", result)
        self.assertIn("categories:", result)
        self.assertIn("\n# Demo\n", result)
        self.assertIn("![图片](</images/程序设计(A)(C)/示例.png>)", result)

    def test_does_not_duplicate_matching_h1_or_rewrite_plain_urls(self):
        source = """---
title: Demo
---
# Demo
http://127.0.0.1:12961/images/flag.txt
"""
        result = normalize_article(source)
        self.assertEqual(result.count("# Demo"), 1)
        self.assertIn("http://127.0.0.1:12961/images/flag.txt", result)


if __name__ == "__main__":
    unittest.main()
