from argparse import Namespace
from dataclasses import dataclass, field
from typing import List, Optional
from deb_wiki_mod.lib.cli.parser import (
    load_down_command_parser,
    load_parser,
    load_toml_command_parser,
)


__all__ = ("get_cli_options", "CLIOptions", "CLIDownOptions", "CLITOMLOptions")


@dataclass()
class CLITOMLOptions:
    path: str = field(default="")


@dataclass()
class CLIDownOptions:
    url: str = field(default="")
    page_id: Optional[str] = None
    output: Optional[str] = None


@dataclass()
class CLIOptions:
    down: Optional[CLIDownOptions] = field(default=None)
    toml: Optional[CLITOMLOptions] = field(default=None)


def create_down_action(options: CLIOptions):
    def down_action(args: Namespace):
        options.down = CLIDownOptions()
        attrs = options.down.__dict__.keys()
        for attr in attrs:
            setattr(options.down, attr, getattr(args, attr))

    return down_action


def create_toml_action(options: CLIOptions):
    def toml_action(args: Namespace):
        options.toml = CLITOMLOptions()
        attrs = options.toml.__dict__.keys()
        for attr in attrs:
            setattr(options.toml, attr, getattr(args, attr))

    return toml_action


def get_cli_options(argv: List[str]):
    """Given a list of command line arguments, parse the argument and serialize them into a dataclass object

    Args:
        argv: The list of command line arguments
    Returns:
        options: The CLIOptions dataclass object into which the argments are serialized
    Raises:
        Exception: When --outfile is specified with multiple urls (e.g, program url1 url2 --outfile path)
    """
    parser = load_parser()
    subparsers = parser.add_subparsers()

    cli_options = CLIOptions()

    load_down_command_parser(subparsers, action=create_down_action(cli_options))
    load_toml_command_parser(subparsers, action=create_toml_action(cli_options))

    args = parser.parse_args(argv)
    args.func(args)

    return cli_options
