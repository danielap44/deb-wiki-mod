# import re
import unittest

# from typing import Any, Callable

from bs4 import BeautifulSoup

from deb_wiki_mod.lib.core import *

from . import DEBIAN_WIKI_NEWS_PAGE_URL, get_fixture


# minify: Callable[[Any], str] = lambda x: re.sub(
#     r"^ +|(?<=\n)\n", "", str(x), flags=re.MULTILINE
# )


class CoreTest(unittest.TestCase):
    main_page_id = "page"
    soup = BeautifulSoup(get_fixture("html"), "html.parser")
    html = str(soup)
    main = str(soup.find("div", id=main_page_id))

    def test_resolve_content(self):
        content = resolve_content(self.html, content_id=None)
        self.assertEqual(str(content), self.html)

    def test_resolve_content_main(self):
        content = resolve_content(self.html, content_id=self.main_page_id)
        self.assertEqual(str(content), self.main)

    def test_resolve_content_main_fail_if_missing(self):
        with self.assertRaises(Exception):
            resolve_content(self.html, content_id="missing-id")

    def test_html2text_factory(self):
        html2text = html2text_factory(baseurl=DEBIAN_WIKI_NEWS_PAGE_URL)
        self.assertEqual(html2text.baseurl, DEBIAN_WIKI_NEWS_PAGE_URL)
        self.assertEqual(html2text.inline_links, False)
        self.assertEqual(html2text.wrap_links, False)

    def test_convert_to_markdown(self):
        converter = html2text_factory(DEBIAN_WIKI_NEWS_PAGE_URL)
        markdown_content = convert_to_makrdown(converter, self.html)
        self.assertEqual(markdown_content, get_fixture("markdown"))


if __name__ == "__main__":
    unittest.main()
