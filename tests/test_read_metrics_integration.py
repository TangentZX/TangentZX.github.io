from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX_PAGES = (
    "docs/index.md",
    "docs/study/index.md",
    "docs/ctf/index.md",
    "docs/sth/index.md",
    "docs/archive/index.md",
    "docs/links/index.md",
    "docs/about/index.md",
)


class ReadMetricsIntegrationTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_hook_is_registered(self):
        self.assertIn("- hooks/read_metrics.py", self.read("mkdocs.yml"))

    def test_section_index_pages_disable_metrics(self):
        for relative_path in INDEX_PAGES:
            with self.subTest(path=relative_path):
                source = self.read(relative_path)
                self.assertTrue(source.startswith("---\n"))
                front_matter = source.split("---", 2)[1]
                self.assertIn("- read-metrics", front_matter)

    def test_script_honors_hidden_marker(self):
        script = self.read("docs/resources/js/read-metrics.js")
        self.assertIn(
            'article.querySelector(\'[data-read-metrics="hidden"]\')',
            script,
        )


if __name__ == "__main__":
    unittest.main()
