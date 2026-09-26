import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("setuptools"), "build backend unavailable in this environment")
    def test_built_package_runs_outside_source_checkout_with_spec(self):
        with tempfile.TemporaryDirectory(prefix="openproduct-dist-") as temp:
            build = Path(temp) / "build"
            result = subprocess.run(
                [sys.executable, "setup.py", "build_py", "--build-lib", str(build)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((build / "openproduct" / "_spec" / "object-schema" / "types.json").is_file())

            env = os.environ.copy()
            env["PYTHONPATH"] = str(build)
            env["PYTHONNOUSERSITE"] = "1"
            help_result = subprocess.run(
                [sys.executable, "-m", "openproduct", "--help"],
                cwd=temp,
                env=env,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(help_result.returncode, 0, help_result.stdout + help_result.stderr)

            spec_result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from openproduct.parser import definition; "
                    "print(len(definition('object-schema/types.json')['types']))",
                ],
                cwd=temp,
                env=env,
                text=True,
                capture_output=True,
                timeout=30,
            )
            self.assertEqual(spec_result.returncode, 0, spec_result.stdout + spec_result.stderr)
            self.assertEqual(spec_result.stdout.strip(), "16")


if __name__ == "__main__":
    unittest.main()
