import unittest

from deb_wiki_mod.lib.cli import *


class CoreTest(unittest.TestCase):
    def test_get_cli_options(self):
        options = get_cli_options(
            [
                "https://example.com/pages/page",
                "--out-file",
                "filename.md",
                "--out-dir",
                "./markdown",
            ]
        )
        self.assertEqual(options.urls, ["https://example.com/pages/page"])
        self.assertEqual(options.out_file, "filename.md")
        self.assertEqual(options.out_dir, "./markdown")

    def test_get_cli_options_output_file_multiple_urls(self):
        with self.assertRaises(Exception):
            get_cli_options(
                [
                    "https://example.com/pages/page",
                    "https://example.com/news/new",
                    "--out-file",
                    "filename.md",
                    "--out-dir",
                    "./markdown",
                ]
            )