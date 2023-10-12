import re
import unittest
from typing import Any, Callable

from deb_wiki_mod.lib.core import *
# from deb_wiki_mod.lib
# from deb_wiki_mod.lib.core

main_page_id = "page"

main = f"""<div id="{main_page_id}">
    <div>Hello World!</div>
</div>"""

html = f"""<!DOCTYPE html>
<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <div id="header">Header content goes here</div>
            {main}
        <footer id="footer">Debian © 2023</footer>
    </body>
</html>"""

minify: Callable[[Any], str] = lambda x: re.sub(r"^ +|(?<=\n)\n", '', str(x), flags=re.MULTILINE)


class CoreTest(unittest.TestCase):
    def test_resolve_content(self):
        content = resolve_content(html, content_id=None)
        self.assertEqual(minify(content), minify(html))

    def test_resolve_content_main(self):
        content = resolve_content(html, content_id=main_page_id)
        self.assertEqual(minify(content), minify(main))

    def test_resolve_content_main_fail_if_missing(self):
        with self.assertRaises(Exception):
            resolve_content(html, content_id="missing-id")


if __name__ == "__main__":
    unittest.main()

