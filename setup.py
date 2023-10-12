from setuptools import setup, find_packages

setup(
    name="deb_wiki_mod",
    packages=find_packages(exclude=["test"]),
    version="0.1.0",
    description="A simple to to convert a HTML page to Markdown",
    author="Daniel Adepitan <danieladepitan44@gmail.com>",
    keywords=["debian", "wiki", "markdown"],
    entry_points={
        "console_scripts": [
            "deb_wiki_mod = deb_wiki_mod.main:main",
        ]
    },
)
