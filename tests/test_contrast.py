import re
import unittest
from pathlib import Path

CSS = (Path(__file__).resolve().parent.parent / "assets" / "style.css").read_text(encoding="utf-8")


def var(name):
    return re.search(r"--%s:\s*(#[0-9a-fA-F]{6})" % name, CSS).group(1)


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


class Contrast(unittest.TestCase):
    # The rose-2 colour is back to its original value (2026-11-01): Nathan owns the page design.
    # These two ratio checks stay as known gaps until he decides on a darker shade.
    @unittest.expectedFailure
    def test_rose2_on_cream(self):
        self.assertGreaterEqual(ratio(var("rose-2"), var("cream")), 4.5)

    @unittest.expectedFailure
    def test_white_on_rose2(self):
        self.assertGreaterEqual(ratio("#FFFFFF", var("rose-2")), 4.5)

    def test_ph_btn_uses_white_on_rose2(self):
        self.assertRegex(CSS, r"\.ph-btn\{[^}]*background:var\(--rose-2\);color:#fff")


if __name__ == "__main__":
    unittest.main()
