"""Rejection tests for malformed and geometrically false proof objects."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "verify_322.py"
CERTIFICATE = ROOT / "data" / "tiling-322.json"


class CertificateRejectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    def rejected(self, mutate):
        obj = copy.deepcopy(self.original)
        mutate(obj)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "false-certificate.json"
            path.write_text(json.dumps(obj), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(path)],
                capture_output=True, text=True, timeout=30,
            )
        self.assertNotEqual(result.returncode, 0, "A false certificate was accepted")
        self.assertNotIn('"verdict": "PASS"', result.stdout)

    def test_missing_tile(self):
        self.rejected(lambda obj: obj["tiles"].pop())

    def test_overlap_and_hole(self):
        # Congruence, tile count, and total area survive this corruption.
        self.rejected(lambda obj: obj["tiles"].__setitem__(1, obj["tiles"][0]))

    def test_changed_vertex(self):
        self.rejected(lambda obj: obj["tiles"][0][0].__setitem__(0, obj["tiles"][0][0][0] + 1))

    def test_noninteger_coordinate(self):
        self.rejected(lambda obj: obj["tiles"][0][0].__setitem__(0, float(obj["tiles"][0][0][0])))

    def test_reversed_tile(self):
        self.rejected(lambda obj: obj["tiles"][0].reverse())

    def test_wrong_metric(self):
        self.rejected(lambda obj: obj.__setitem__("D", 31))

    def test_wrong_denominator(self):
        self.rejected(lambda obj: obj.__setitem__("denominator", 19))

    def test_wrong_target(self):
        self.rejected(lambda obj: obj["target"][0].__setitem__(0, obj["target"][0][0] + 18))

    def test_optimized_python_is_rejected(self):
        result = subprocess.run(
            [sys.executable, "-O", str(CHECKER), str(CERTIFICATE)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires assertions", result.stderr)

    def test_valid_certificate_positive_control(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(CERTIFICATE)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["all_tile_pair_intersections_tested"], 51681)


if __name__ == "__main__":
    unittest.main()
