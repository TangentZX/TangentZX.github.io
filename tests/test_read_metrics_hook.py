from types import SimpleNamespace
import unittest

from hooks.read_metrics import MARKER, on_page_content


class ReadMetricsHookTests(unittest.TestCase):
    def render(self, hide=None):
        meta = {} if hide is None else {"hide": hide}
        page = SimpleNamespace(meta=meta)
        return on_page_content("<p>正文</p>", page, None, None)

    def test_keeps_html_unchanged_without_switch(self):
        self.assertEqual(self.render(), "<p>正文</p>")
        self.assertEqual(self.render(["toc"]), "<p>正文</p>")

    def test_prepends_marker_for_list_switch(self):
        self.assertEqual(
            self.render(["toc", "read-metrics"]),
            f"{MARKER}\n<p>正文</p>",
        )

    def test_accepts_string_switch(self):
        self.assertEqual(
            self.render("read-metrics"),
            f"{MARKER}\n<p>正文</p>",
        )


if __name__ == "__main__":
    unittest.main()
