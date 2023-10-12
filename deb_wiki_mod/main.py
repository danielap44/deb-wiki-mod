#!/usr/bin/env python

import sys

from deb_wiki_mod.lib.cli import get_cli_options
from deb_wiki_mod.lib.core import (
    convert_to_makrdown,
    fetch_debian_news_page,
    html2text_factory,
    resolve_content,
    write_markdown_to_output_file,
)


def main():
    options = get_cli_options()
    response = fetch_debian_news_page(options.url)
    html = response.text

    try:
        page = resolve_content(html=html, content_id=options.main)
    except Exception as exc:
        print(str(exc))
        return sys.exit(1)
    converter = html2text_factory(options.url)
    markdown_content = convert_to_makrdown(converter, str(page))

    write_markdown_to_output_file(markdown=markdown_content, filename=options.output)


if __name__ == "__main__":
    main()
