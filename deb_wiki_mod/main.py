#!/usr/bin/env PYTHONPATH=. python3

import os.path
import pathlib
import sys
from typing import List

from requests import HTTPError

from deb_wiki_mod.lib.cli import get_cli_options, CLIDownOptions, CLITOMLOptions
from deb_wiki_mod.lib.config import PROGRAM_NAME
from deb_wiki_mod.lib.core import (
    resolve_output_file,
    convert_to_makrdown,
    fetch_debian_news_page,
    get_config_from_toml_file,
    html2text_factory,
    plural,
    resolve_content,
    write_markdown_to_output_file,
)
from deb_wiki_mod.lib.logger import get_logger


logger = get_logger(PROGRAM_NAME)


def down_handler(options_list: List[CLIDownOptions]):
    success_count = 0
    input_len = len(options_list)

    if not options_list:
        return

    for options in options_list:
        try:
            logger.info(f"Fetching page from {options.url}")
            response = fetch_debian_news_page(options.url)
            html = response.text
        except HTTPError as exc:
            logger.error(str(exc))
            continue
        try:
            logger.info("Resolving main content area of the page")
            page = resolve_content(html=html, content_id=options.page_id)
        except Exception as exc:
            logger.error(str(exc))
            continue

        logger.info(
            f"Converting page content extracted from '{options.url}' to markdown"
        )
        converter = html2text_factory(options.url)
        markdown_content = convert_to_makrdown(converter, str(page))
        filename = resolve_output_file(url=options.url, output=options.output)
        
        if not os.path.isdir(os.path.dirname(filename)):
            pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        logger.info(f"Writing output file to disk: {options.url} -> {filename}")
        write_markdown_to_output_file(markdown=markdown_content, filename=filename)
        success_count += 1

    logger.info(
        f"Complete: Processed {success_count} of {input_len} "
        f"{plural(input_len, 'url', 'urls')} successfully"
    )


def toml_handler(options: CLITOMLOptions):
    """Using configurations read from a toml file specified in a CLITOMLOptions object,
    for the number of pages present in the config file, parse each page url and convert
    to markdown.

        Args:
            options: The set of command line options and arguments parsed and serialised\
            into dataclass object `CLITOMLOptions`
        Returns:
            None
    """

    if not options.path:
        return
    config = get_config_from_toml_file(options.path)

    """Paths specified in the TOML config file are relative to the config file path, 
    except they are absolute paths.

    The `root_output` is expected to be a directory rather than a file, while the pages 
    output is expected to be a file rather than a directory.
    """

    basedir = os.path.abspath(os.path.dirname(options.path))
    root = config.get("root")
    root_output = root.get("output") or basedir
    pages = root.get("pages")

    """If `root_output` isn't absolute, then it wasn't originally `None`, because 
    `basedir` is guranteed to be absolute. So it's safe to join `basedir` with 
    `root_output` which is a relative path.
    """

    if not os.path.isabs(root_output):
        root_output = os.path.join(basedir, root_output)

    """If `root_output` isn't a directory, then it wasn't originally `None`, because 
    `basedir` is guaranteed to be a directory. Go ahead and `mkdir -p ${root_output}`.
    """

    if not os.path.isdir(root_output):
        pathlib.Path(root_output).mkdir(parents=True, exist_ok=True)

    down_options_list: List[CLIDownOptions] = []

    for page in pages:
        url, output, page_id = page.get("url"), page.get("output"), page.get("page_id")

        if output is not None:
            # this may be unnecessary since join would return the last abs path passed in
            if not os.path.isabs(output):
                output = os.path.normpath(os.path.join(root_output, output))
            down_options = CLIDownOptions(url=url, page_id=page_id, output=output)
        else:
            down_options = CLIDownOptions(url=url, page_id=page_id, output=root_output)
        down_options_list.append(down_options)
    down_handler(down_options_list)


def main():
    try:
        options = get_cli_options(sys.argv[1:])
    except Exception as exc:
        logger.error(str(exc))
        return sys.exit(1)
    if options.down is not None:
        down_handler([options.down])
    if options.toml is not None:
        toml_handler(options.toml)


if __name__ == "__main__":
    main()
