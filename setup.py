#!/usr/bin/env python

from setuptools import setup, find_packages

# Get the version from the package
version = {}
with open("src/sqlfluff_constraint_naming/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="sqlfluff-constraint-naming",
    version=version["__version__"],
    description="A SQLFluff plugin for constraint naming conventions",
    author="Sergey Boykov",
    author_email="boikov.sa@yandex.ru",
    url="https://github.com/sergeiboikov/sqlfluff-constraint-naming",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["sqlfluff>=3.3.1"],
    entry_points={
        "sqlfluff": ["sqlfluff_constraint_naming=sqlfluff_constraint_naming.rules"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)