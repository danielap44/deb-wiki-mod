from argparse import ArgumentParser
from dataclasses import dataclass
from os.path import basename, abspath
from typing import Optional


_DEBIAN_WIKI_NEWS_PAGE_URL = "https://wiki.debian.org/News"


_parser = ArgumentParser()
_parser.add_argument(
    "url",
    type=str,
    default=_DEBIAN_WIKI_NEWS_PAGE_URL,
    help="The url to the page to parse and convert to markdown",
)
_parser.add_argument(
    "--main",
    type=str,
    required=False,
    help="The ID of the main content area of the page",
)
_parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=False,
    help="The output filename for the resulting markdown",
)


@dataclass(kw_only=True)
class CLIOptions:
    url: str = ...  # type: ignore
    main: Optional[str] = None
    output: str = ...  # type: ignore


def get_cli_options():
    args = _parser.parse_args()
    options = CLIOptions()
    attrs = options.__dict__.keys()

    for attr in attrs:
        setattr(options, attr, getattr(args, attr))

    if not options.output:
        options.output = abspath(basename(options.url) + ".md")
    return options
