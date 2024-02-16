#!/usr/bin/env python
import sys
from pathlib import Path

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        f"""
==========================
Unsupported Python version
==========================
This version of nvd_search requires at least Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]},
but you're trying to install it on Python {CURRENT_PYTHON[0]}.{CURRENT_PYTHON[1]}.
"""
    )
    sys.exit(1)

requires = [
    "click",
    "requests",
    "pydantic>=2.6",
    "rich",
]

about: dict[str, str] = {}
info_path: Path = (Path(__file__).parent / "nvd_search" / "__version__.py").resolve()
with info_path.open(encoding="utf-8") as f:
    exec(f.read(10_000), about)

readme_path: Path = (Path(__file__).parent / "README.md").resolve()
with readme_path.open(encoding="utf-8") as f:
    readme = f.read(1_000_000)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    package_data={"": ["LICENSE"]},
    package_dir={"nvd_search": "nvd_search"},
    include_package_data=True,
    python_requires=f">={REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}",
    install_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Pydantic",
        "Framework :: Pytest",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        # "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    project_urls={
        "Source": "https://github.com/m-fr/nvd_search",
    },
    entry_points="""
        [console_scripts]
        nvd_search=nvd_search.cli.cli:cli
    """,
)
