from argparse import ArgumentParser
from dataclasses import dataclass, field
from typing import Optional

__all__ = ("get_cli_options",)


_parser = ArgumentParser(
    prog="DebianWikiModernizer",
    description="A basic Python package to convert HTML pages to markdown",
)
_parser.add_argument(
    "urls",
    type=str,
    nargs="+",
    help="A list of page urls to parse and convert to markdown",
)
_parser.add_argument(
    "--main",
    type=str,
    required=False,
    help="The ID of the main content area of the page",
)
_parser.add_argument(
    "-f",
    "--out-file",
    type=str,
    required=False,
    help="The output filename for the resulting markdown.",
)
_parser.add_argument(
    "-d",
    "--out-dir",
    type=str,
    required=False,
    help="The output dirname for the resulting markdown.",
)


@dataclass(kw_only=True)
class CLIOptions:
    urls: list[str] = field(default_factory=list)
    main: Optional[str] = None
    out_file: Optional[str] = None
    out_dir: Optional[str] = None


def get_cli_options(argv: list[str]):
    """Given a list of command line arguments, parse the argument and serialize them into a dataclass object

    Args:
        argv: The list of command line arguments
    Returns:
        options: The CLIOptions dataclass object into which the argments are serialized
    Raises:
        Exception: When --out-file is specified with multiple urls (e.g, program url1 url2 --out-file path)
    """
    args = _parser.parse_args(argv)
    options = CLIOptions()
    attrs = options.__dict__.keys()

    for attr in attrs:
        setattr(options, attr, getattr(args, attr))
    if len(options.urls) > 1 and options.out_file is not None:
        raise Exception(
            "--out-file cannot be specified with multiple urls (consider --out-dir)"
        )
    return options
