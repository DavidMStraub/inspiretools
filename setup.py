from setuptools import setup

with open("README.md") as readme_file:
    README = readme_file.read()

setup(
    name="inspiretools",
    version="0.3",
    url="https://github.com/DavidMStraub/inspire-tools",
    author="David M. Straub",
    description="Python package to auto-generate bibliographies pulling the bibtex data from Inspire",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["inspiretools"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "auxtobib = inspiretools:aux2bib",
            "blgtobib = inspiretools:blg2bib",
        ]
    },
)
