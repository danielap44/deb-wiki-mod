#!/usr/bin/env PYTHONPATH=. python3

import sys

from requests import HTTPError

from deb_wiki_mod.lib.cli import get_cli_options
from deb_wiki_mod.lib.core import (
    compute_output_file,
    convert_to_makrdown,
    fetch_debian_news_page,
    html2text_factory,
    plural,
    resolve_content,
    write_markdown_to_output_file,
)
from deb_wiki_mod.lib.logger import get_logger

PROGRAM_NAME = "DebWikiModernizer"

logger = get_logger(PROGRAM_NAME)


def main():
    try:
        options = get_cli_options(sys.argv[1:])
    except Exception as exc:
        logger.error(str(exc))
        return sys.exit(1)
    success_count = 0
    input_len = len(options.urls)

    for url in options.urls:
        try:
            logger.info(f"Fetching page from {url}")
            response = fetch_debian_news_page(url)
            html = response.text
        except HTTPError as exc:
            logger.error(str(exc))
            continue
        try:
            logger.info("Resolving main content area of the page")
            page = resolve_content(html=html, content_id=options.main)
        except Exception as exc:
            logger.error(str(exc))
            continue

        logger.info(f"Converting page content extracted from '{url}' to markdown")
        converter = html2text_factory(url)
        markdown_content = convert_to_makrdown(converter, str(page))

        filename = compute_output_file(
            url=url,
            outfile=options.out_file,
            outdir=options.out_dir,
        )
        logger.info(f"Writing output file to disk: {url} -> {filename}")
        write_markdown_to_output_file(markdown=markdown_content, filename=filename)
        success_count += 1

    logger.info(
        f"Complete: Processed {success_count} of {input_len} "
        f"{plural(input_len, 'url', 'urls')} successfully"
    )


if __name__ == "__main__":
    main()
