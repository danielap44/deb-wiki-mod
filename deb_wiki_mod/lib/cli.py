from argparse import ArgumentParser
from dataclasses import dataclass

_DEBIAN_WIKI_NEWS_PAGE_URL = "https://wiki.debian.org/News"


_parser = ArgumentParser()
_parser.add_argument("url", type=str, default=_DEBIAN_WIKI_NEWS_PAGE_URL, help="The url to the page to parse and convert to markdown")
_parser.add_argument('--main', type=str, required=False, help="The ID of the main content area of the page")

@dataclass(kw_only=True)
class CLIOptions:
    url: str = ...
    main: str | None =  None
    

def get_cli_options():
    args = _parser.parse_args()
    options = CLIOptions()
    attrs = options.__dict__.keys()

    for attr in attrs:
        setattr(options, attr, getattr(args, attr))
    return options

