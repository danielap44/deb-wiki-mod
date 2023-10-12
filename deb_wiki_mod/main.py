#!/usr/bin/env python

import sys

from lib.cli import get_cli_options
from lib.core import (
    fetch_debian_news_page,
    resolve_content,
    write_html_page_to_markdown_file,
)


def main(argv):
    options = get_cli_options()
    response = fetch_debian_news_page(options.url)
    html = response.text

    try:
        page = resolve_content(html=html, content_id=options.main)
    except Exception as exc:
        print(str(exc))
        return sys.exit(1)
    write_html_page_to_markdown_file(
        page=page, baseurl=options.url, filename="./News.md"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
