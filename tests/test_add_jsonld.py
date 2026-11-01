import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import add_jsonld  # noqa: E402

PAGE = "<!doctype html><html><head><title>t</title></head><body>%s</body></html>"
OFFRE = PAGE % ('<section><div class="grid">'
                '<div class="card tier"><h2>Solo</h2><div class="price">480 € <small>par an</small></div><p>x</p></div>'
                '<div class="card tier featured"><h2>Salon</h2><div class="price">777 € <small>par an</small></div><p>y</p></div>'
                '</div></section>')
INDEX = PAGE % ('<details><summary>Q1 ?</summary><p>R1 &amp; plus.</p></details>'
                '<details><summary>Q2 ?</summary><p>R2.</p></details>')


def blocks(src):
    return [json.loads(b) for b in re.findall(
        r'<script type="application/ld\+json"[^>]*>(.*?)</script>', src, re.S)]


class Inject(unittest.TestCase):
    def test_organization_only(self):
        b = blocks(add_jsonld.process(PAGE % "x", "cgv.html"))
        self.assertEqual(len(b), 1)
        self.assertEqual([n["@type"] for n in b[0]["@graph"]], ["Organization"])

    def test_offer_prices_read_from_page(self):
        g = blocks(add_jsonld.process(OFFRE, "offre.html"))[0]["@graph"]
        offers = [n for n in g if n["@type"] == "Offer"]
        self.assertEqual([(o["name"], o["price"]) for o in offers], [("Solo", "480"), ("Salon", "777")])

    def test_faq(self):
        g = blocks(add_jsonld.process(INDEX, "index.html"))[0]["@graph"]
        f = [n for n in g if n["@type"] == "FAQPage"][0]
        self.assertEqual(len(f["mainEntity"]), 2)
        self.assertEqual(f["mainEntity"][0]["acceptedAnswer"]["text"], "R1 & plus.")

    def test_no_faq_no_block(self):
        g = blocks(add_jsonld.process(PAGE % "x", "index.html"))[0]["@graph"]
        self.assertFalse([n for n in g if n["@type"] == "FAQPage"])

    def test_idempotent(self):
        once = add_jsonld.process(OFFRE, "offre.html")
        self.assertEqual(add_jsonld.process(once, "offre.html"), once)
        self.assertEqual(once.count("application/ld+json"), 1)

    def test_cli_skips_404_and_reruns(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "404.html").write_text(PAGE % "x", encoding="utf-8")
            (d / "offre.html").write_text(OFFRE, encoding="utf-8")
            add_jsonld.main([str(d)])
            first = (d / "offre.html").read_text(encoding="utf-8")
            add_jsonld.main([str(d)])
            self.assertEqual((d / "offre.html").read_text(encoding="utf-8"), first)
            self.assertNotIn("ld+json", (d / "404.html").read_text(encoding="utf-8"))

    def test_real_site_prices_match_page(self):
        src = (ROOT / "offre.html").read_text(encoding="utf-8")
        src = add_jsonld.BLOCK_RE.sub("", src)
        for o in add_jsonld.offers(src):
            self.assertIn(o["price"] + " €", src)
        self.assertEqual(len(add_jsonld.offers(src)), 2)


if __name__ == "__main__":
    unittest.main()
