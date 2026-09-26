from pathlib import Path
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


ROOT = Path(__file__).resolve().parent


class build_py(_build_py):
    """Build the runtime package with an immutable copy of the canonical spec."""

    def run(self):
        super().run()
        source = ROOT / "spec"
        target = Path(self.build_lib) / "openproduct" / "_spec"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)


setup(cmdclass={"build_py": build_py})
