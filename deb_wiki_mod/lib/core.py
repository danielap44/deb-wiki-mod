from typing import Optional

import requests
import html2text
from bs4 import BeautifulSoup

__all__ = (
    "convert_to_makrdown",
    "fetch_debian_news_page",
    "resolve_content",
    "html2text_factory",
    "write_markdown_to_output_file",
)


def fetch_debian_news_page(url: str):
    response = requests.get(url)
    return response


def resolve_content(html: str, *, content_id: Optional[str]):
    soup = BeautifulSoup(html, "html.parser")
    if content_id is None:
        return soup
    if soup.body is None:  # this shouldn't happen
        raise Exception("The fetched page has no body tag or body element")
    content = soup.body.find(id=content_id)

    if content is None:
        raise Exception(
            f"The main content area of the page `#{content_id}` could not be resolved"
        )
    return content


def html2text_factory(baseurl: str):
    h = html2text.HTML2Text(baseurl=baseurl)
    h.inline_links = False
    h.wrap_links = False

    return h


def convert_to_makrdown(converter: html2text.HTML2Text, html: str):
    return converter.handle(html)


def write_markdown_to_output_file(*, markdown: str, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(markdown)
