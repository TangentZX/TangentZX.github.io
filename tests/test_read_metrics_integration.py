from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadMetricsIntegrationTests(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_hook_is_registered(self):
        self.assertIn("- hooks/read_metrics.py", self.read("mkdocs.yml"))

    def test_homepage_disables_metrics(self):
        front_matter = self.read("docs/index.md").split("---", 2)[1]
        self.assertIn("- read-metrics", front_matter)

    def test_script_honors_hidden_marker(self):
        script = self.read("docs/resources/js/read-metrics.js")
        self.assertIn(
            'article.querySelector(\'[data-read-metrics="hidden"]\')',
            script,
        )


if __name__ == "__main__":
    unittest.main()
