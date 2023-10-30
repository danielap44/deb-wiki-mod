import unittest

from deb_wiki_mod.lib.cli import *


class CoreTest(unittest.TestCase):
    def test_get_cli_down_command_options(self):
        options = get_cli_options(
            "down https://example.com/pages/page --output filename.md".split(),
        )
        assert options.down is not None
        self.assertEqual(options.down.url, "https://example.com/pages/page")
        self.assertEqual(options.down.output, "filename.md")

    def test_get_cli_toml_command_options(self):
        options = get_cli_options("toml ./deb_wiki.toml".split())
        assert options.toml is not None
        self.assertEqual(options.toml.path, "./deb_wiki.toml")
