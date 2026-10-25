import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "tools"))

import check_site  # noqa: E402


def codes(name):
    findings, _ = check_site.check(FIXTURES / name)
    return [(f.level, f.code, f.page, f.line) for f in findings]


def cli(*args):
    return subprocess.run([sys.executable, str(ROOT / "tools" / "check_site.py"), *args],
                          capture_output=True, text=True)


class GoodSite(unittest.TestCase):
    def test_no_findings(self):
        self.assertEqual(codes("good"), [])

    def test_exit_code_zero(self):
        self.assertEqual(cli(str(FIXTURES / "good")).returncode, 0)


class BrokenSite(unittest.TestCase):
    def setUp(self):
        self.found = codes("broken")

    def test_missing_page_link(self):
        self.assertIn(("error", "broken-link", "index.html", 10), self.found)

    def test_broken_anchor(self):
        self.assertIn(("error", "broken-anchor", "index.html", 11), self.found)

    def test_root_relative_and_escaping_links(self):
        self.assertIn(("error", "broken-link", "index.html", 12), self.found)
        self.assertIn(("error", "broken-link", "index.html", 13), self.found)

    def test_missing_image(self):
        self.assertIn(("error", "broken-link", "index.html", 14), self.found)

    def test_sitemap_page_missing_with_line(self):
        self.assertIn(("error", "sitemap-missing-page", "sitemap.xml", 5), self.found)

    def test_exit_code_one(self):
        self.assertEqual(cli(str(FIXTURES / "broken")).returncode, 1)


class TrackerSite(unittest.TestCase):
    def setUp(self):
        self.found = codes("trackers")

    def test_external_script(self):
        self.assertIn(("error", "external-script", "index.html", 7), self.found)

    def test_tracker_url_and_inline(self):
        self.assertIn(("error", "tracker", "index.html", 8), self.found)
        self.assertIn(("error", "tracker", "index.html", 9), self.found)

    def test_tracker_in_local_js(self):
        self.assertIn(("error", "tracker", "app.js", 1), self.found)

    def test_missing_lang(self):
        self.assertIn(("error", "missing-lang", "index.html", None), self.found)

    def test_cookie_is_warning_only(self):
        self.assertIn(("warning", "cookie-use", "index.html", 9), self.found)


class WarningSite(unittest.TestCase):
    def setUp(self):
        self.found = codes("warnings")
        self.names = {(c, p) for _, c, p, _ in self.found}

    def test_only_warnings(self):
        self.assertEqual({lv for lv, *_ in self.found}, {"warning"})

    def test_exit_code_zero_with_warnings(self):
        self.assertEqual(cli(str(FIXTURES / "warnings")).returncode, 0)

    def test_canonical_mismatch(self):
        self.assertIn(("canonical-mismatch", "index.html"), self.names)

    def test_h1_count(self):
        self.assertIn(("h1-count", "index.html"), self.names)

    def test_img_alt(self):
        self.assertIn(("img-alt", "index.html"), self.names)

    def test_missing_noindex(self):
        self.assertIn(("missing-noindex", "404.html"), self.names)
        self.assertIn(("missing-noindex", "demos/a.html"), self.names)

    def test_price_and_delay_variants(self):
        self.assertIn(("price-variants", "index.html"), self.names)
        self.assertIn(("delay-variants", "index.html"), self.names)

    def test_demo_prices_are_not_compared(self):
        findings, _ = check_site.check(FIXTURES / "warnings")
        self.assertFalse([f for f in findings if f.code == "price-variants" and "42" in f.message])


class Extraction(unittest.TestCase):
    def values(self, text):
        return [(k, v, s) for k, v, s, _ in check_site.extract_quantities([(text, 1)])]

    def test_price_forms(self):
        got = {v for k, v, _ in self.values("19 €, 19€, 19,00 euros, €19") if k == "price"}
        self.assertEqual(got, {19.0})

    def test_delay_forms(self):
        got = {v for k, v, _ in self.values("72 h, 72 heures, 3 jours") if k == "delay"}
        self.assertEqual(got, {(72.0, "h")})

    def test_time_of_day_is_skipped(self):
        self.assertEqual(self.values("à 9 h (heure de Paris)"), [])


class Discovery(unittest.TestCase):
    def test_fixtures_and_tools_are_skipped_on_repo_root(self):
        pages = check_site.find_pages(ROOT)
        self.assertFalse([p for p in pages if p.startswith(("tests/", "tools/"))])


class Report(unittest.TestCase):
    def test_markdown_has_not_found_and_no_em_dash(self):
        findings, quantities = check_site.check(FIXTURES / "good")
        md = check_site.render_markdown(findings, quantities)
        self.assertIn("not found", md)
        self.assertNotIn(chr(0x2014), md)

    def test_text_summary(self):
        findings, _ = check_site.check(FIXTURES / "broken")
        self.assertTrue(check_site.render_text(findings).endswith("6 error(s), 0 warning(s)"))


if __name__ == "__main__":
    unittest.main()
