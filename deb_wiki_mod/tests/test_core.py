# import re
import unittest

from os.path import abspath

from bs4 import BeautifulSoup

from deb_wiki_mod.lib.core import *

from . import DEBIAN_WIKI_NEWS_PAGE_URL, get_fixture


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

    def test_compute_output_file(self):
        no_ouput = resolve_output_file(
            url="https://wiki.debian.org/News",
            output=None,
        )
        with_output = resolve_output_file(
            url="https://wiki.debian.org/News",
            output="./markdown/File.md",
        )
        with_output_dir = resolve_output_file(
            url="https://wiki.debian.org/News",
            output="./markdown/",  # The trailing slash is important to show it's a dir
        )
        no_output_no_basename = resolve_output_file(
            url="https://www.debian.org/News/project/",
            output=None,
        )
        with_output_no_basename = resolve_output_file(
            url="https://www.debian.org/News/project/",
            output="./markdown/File.md",
        )
        with_output_dir_no_basename = resolve_output_file(
            url="https://www.debian.org/News/project/",
            output="./markdown/",
        )

        self.assertEqual(no_ouput, abspath("./News.md"))
        self.assertEqual(with_output, abspath("./markdown/File.md"))
        self.assertEqual(with_output_dir, abspath("./markdown/News.md"))
        self.assertEqual(no_output_no_basename, abspath("./News/project/index.md"))
        self.assertEqual(with_output_no_basename, abspath("./markdown/File.md"))
        self.assertEqual(
            with_output_dir_no_basename, abspath("./markdown/News/project/index.md")
        )

    def test_plural(self):
        self.assertEqual(plural(0, "egg", "eggs"), "egg")
        self.assertEqual(plural(1, "egg", "eggs"), "egg")
        self.assertEqual(plural(2, "egg", "eggs"), "eggs")


if __name__ == "__main__":
    unittest.main()
