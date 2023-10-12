from setuptools import setup, find_packages

def get_requirements():
    with open('./requirements.txt', 'r') as file:
        return file.read().splitlines()

setup(
    name="deb_wiki_mod",
    packages=find_packages(exclude=["tests"]),
    version="0.1.0",
    description="A simple to to convert a HTML page to Markdown",
    author="Daniel Adepitan <danieladepitan44@gmail.com>",
    author_email="<danieladepitan44@gmail.com>",
    keywords=["debian", "wiki", "markdown"],
    python_requires=">=3.5",
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "deb_wiki_mod = deb_wiki_mod.main:main",
        ]
    },
)
