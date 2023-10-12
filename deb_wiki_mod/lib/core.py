import requests
import html2text
from bs4 import BeautifulSoup

__all__ = (
    "fetch_debian_news_page",
    "resolve_content",
    "html2text_factory",
    "write_html_page_to_markdown_file",
)


def fetch_debian_news_page(url: str):
    response = requests.get(url)
    return response


def resolve_content(html: str, *, content_id: str | None):
    soup = BeautifulSoup(html, "html.parser")
    if content_id is None:
        return soup
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


def write_html_page_to_markdown_file(
    *, page: BeautifulSoup, baseurl: str, filename: str
):
    converter = html2text_factory(baseurl)
    markdown_content = converter.handle(str(page))
    with open(filename, "w", encoding="utf-8") as file:
        file.write(markdown_content)
