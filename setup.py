#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


def get_version():
    with open("src/service_monitor/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="service-monitor",
    version=get_version(),
    description="Monitor a list of urls periodically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Savio Fernandes",
    author_email="savio@saviof.com",
    license="MIT",
    url="https://github.com/artbycrunk/service-monitor",
    # packages=setuptools.find_packages(),
    # packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages("src"),
    entry_points={
        "console_scripts": ["service-monitor = service_monitor.cli:main"]
    },
)
