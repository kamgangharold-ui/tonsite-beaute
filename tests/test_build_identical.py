"""The build output must be byte identical to the committed site."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
import build  # noqa: E402

TOP = ["robots.txt", "sitemap.xml", ".nojekyll"]


def site_files(base):
    files = [p for p in base.glob("*.html")]
    files += (base / "demos").glob("*.html")
    files += (base / "assets").glob("*")
    files += [base / f for f in TOP if (base / f).exists()]
    return sorted(p.relative_to(base).as_posix() for p in files)


class BuildIdentical(unittest.TestCase):
    def test_every_file_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build.build(out)
            built, committed = site_files(out), site_files(ROOT)
            self.assertEqual(built, committed)
            self.assertGreaterEqual(len(committed), 18)
            for rel in committed:
                self.assertEqual((out / rel).read_bytes(), (ROOT / rel).read_bytes(), rel)


if __name__ == "__main__":
    unittest.main()
