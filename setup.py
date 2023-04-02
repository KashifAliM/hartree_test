import re

from setuptools import setup

with open("src/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


# Metadata goes in setup.cfg.
setup(
    name="hartreetest",
    version=version,
    install_requires=[
    ],
    extras_require={"dev": ["pytest", "pytest-cov", "pytest-env"]},
)
