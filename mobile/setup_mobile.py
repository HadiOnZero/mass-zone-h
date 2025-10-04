#!/usr/bin/env python3
"""
Setup script for Zone-H Mobile Mirror Tool
Installation and configuration script
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README_MOBILE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements_mobile.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="zone-h-mobile-mirror",
    version="1.0.0",
    author="Hadi Ramdhani",
    author_email="hadi.ramdhani@example.com",
    description="Mobile application for mass mirroring Zone-H notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hadiramdhani/zone-h-mass-mirror",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Android",
        "Operating System :: iOS",
        "Environment :: Mobile",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zone-h-mobile=main_mobile:main",
            "zone-h-mobile-gui=run_mobile:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json", "*.csv"],
        "src.assets": ["*.png", "*.jpg", "*.ico"],
    },
    keywords="zone-h mirror mobile security hacking kivy android ios",
    project_urls={
        "Bug Reports": "https://github.com/hadiramdhani/zone-h-mass-mirror/issues",
        "Source": "https://github.com/hadiramdhani/zone-h-mass-mirror",
        "Documentation": "https://github.com/hadiramdhani/zone-h-mass-mirror/blob/main/mobile/README_MOBILE.md",
    },
)