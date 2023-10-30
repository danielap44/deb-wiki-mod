from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from argparse import _SubParsersAction, Action  # type: ignore
from typing import Any, Callable, Dict, List

from deb_wiki_mod.lib.config import DESCRIPTION, PROGRAM_NAME

_DOWN_COMMAND_DESC = """Parse the pages with the following urls to markdown"""
_TOML_COMMAND_DESC = """Using a toml config file, reads the toml file and \
parses a set of pages specified in the toml file to markdown.
Basic structure of toml config file is as follows::

    [root]
    outdir = "/path/to/output/directory" # Joined with output path for each page, except absolute

    [[root.pages]]
    url = "https://example.com/pages/first"
    output = "first.md" # resolves to /path/to/output/directory/first.md
    page_id = "main"

    [[root.pages]]
    url = "https://example.com/pages/second"
    output = "/path/to/different/directory/second.md" # resolves to /path/to/different/directory/second.md
    page_id = "content"

Note: Paths specified in the TOML config file are resolved relative to the file
"""

_DOWN_COMMAND_ARGS: List[Dict[str, Any]] = [
    {
        "name": ["url"],
        "type": str,
        "help": "A list of page URLs to parse and convert to markdown",
    },
    {
        "name": ["--page-id"],
        "type": str,
        "required": False,
        "help": "The ID of the main content area of the page",
    },
    {
        "name": ["-o", "--output"],
        "type": str,
        "required": False,
        "help": "The output filename or directory for the resulting markdown",
    },
]

_TOML_COMMAND_ARGS: List[Dict[str, Any]] = [
    {
        "name": ["path"],
        "type": str,
        "help": "A file path to the TOML config file to use to fetch and parse pages to markdown",
    }
]


def load_parser():
    parser = ArgumentParser(
        prog=PROGRAM_NAME,
        description=DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
    )
    return parser


def load_down_command_parser(
    subparsers: "_SubParsersAction[ArgumentParser]", action: Callable[[Namespace], Any]
):
    down_command = subparsers.add_parser(
        "down",
        description=_DOWN_COMMAND_DESC,
        formatter_class=RawDescriptionHelpFormatter,
    )

    for argument in _DOWN_COMMAND_ARGS:
        argument_copy = argument.copy()
        down_command.add_argument(*argument_copy.pop("name"), **argument_copy)
    down_command.set_defaults(func=action)


def load_toml_command_parser(
    subparsers: "_SubParsersAction[ArgumentParser]", action: Callable[[Namespace], Any]
):
    toml_command = subparsers.add_parser(
        "toml",
        description=_TOML_COMMAND_DESC,
        formatter_class=RawDescriptionHelpFormatter,
    )

    for argument in _TOML_COMMAND_ARGS:
        argument_copy = argument.copy()
        toml_command.add_argument(*argument_copy.pop("name"), **argument_copy)
    toml_command.set_defaults(func=action)
