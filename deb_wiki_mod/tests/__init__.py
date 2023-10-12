from os.path import dirname, exists, join

from deb_wiki_mod.lib.core import convert_to_makrdown, html2text_factory

DEBIAN_WIKI_NEWS_PAGE_URL = "https://wiki.debian.org/News"

fixture_md_file = join(dirname(__file__), "test_output.md")
fixture_html_file = join(dirname(__file__), "test_input.html")


def get_fixture(variant: str):
    """Get the fixture data for either of html or markdown

    :param variant: The type of fixture data to get. Could be one of `html` or `markdown`
    """

    fixture_file = fixture_html_file if variant == "html" else fixture_md_file
    with open(fixture_file, "r") as fixture:
        return fixture.read()


def _setup():
    if not exists(fixture_md_file):
        with open(fixture_md_file, "w") as output:
            converter = html2text_factory(DEBIAN_WIKI_NEWS_PAGE_URL)
            html = get_fixture("html")
            output.write(convert_to_makrdown(converter, html))


_setup()
