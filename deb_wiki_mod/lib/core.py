from os.path import abspath, basename, dirname, isdir, join, normpath
from typing import List, Optional, TypedDict
from urllib.parse import urlparse

import toml
import html2text
import requests
from bs4 import BeautifulSoup

__all__ = (
    "compute_output_file",
    "convert_to_makrdown",
    "fetch_debian_news_page",
    "html2text_factory",
    "plural",
    "resolve_content",
    "write_markdown_to_output_file",
)


class RootTOMLPagesDict(TypedDict):
    url: str
    output: Optional[str]
    page_id: Optional[str]


class RootTOMLConfigDict(TypedDict):
    output: Optional[str]
    pages: List[RootTOMLPagesDict]


class TOMLConfigDict(TypedDict):
    root: RootTOMLConfigDict


def fetch_debian_news_page(url: str):
    """Fetches the page by URL using the requests library.

    Args:
        url: The string url of the page to fetch
    Returns:
        response: The response object from the request
    """
    response = requests.get(url)
    response.raise_for_status()
    return response


def resolve_content(html: str, *, content_id: Optional[str]):
    """Resolves the main content area of an HTML string after parsing with BeautifulSoup.

    Args:
        html: The HTML string to parse and resolve main content from
        content_id: The id of the main page element in the HTML string
    Returns:
        content: The resolved main content element in the HTML string
    """
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
    """A factory function for constructing a HTML2Text object and configuring specific attributes.

    Args:
        baseurl: The baseurl or the origin url to resolve all relative links to
    Returns:
        h: The HTML2Text object
    """
    h = html2text.HTML2Text(baseurl=baseurl)
    h.inline_links = False
    h.wrap_links = False

    return h


def convert_to_makrdown(converter: html2text.HTML2Text, html: str):
    """Converts an HTML string to markdown using a converter supplied as one of the args.

    Args:
        converter: An instance of HTML2Text to use to convert the HTML string to markdown.
        html: The HTML string to convert.
    Returns:
        markdown: The converted markdown string
    """
    return converter.handle(html)


def write_markdown_to_output_file(*, markdown: str, filename: str):
    """Writes a markdown string to an output file with a given filename

    Args:
        markdown: The markdown string to write to a file.
        filename: The filename or file path to write the markdown file to.
    Returns:
        None
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(markdown)


def compute_output_file(*, url: str, output: Optional[str]):
    """Compute the resultant output filename or file path from a set of variable options.

    Args:
        url: The url of the page whose markdown content is being written to a file
        output: The output arg supplied from the command line read from CLIOptions.
    Returs:
        The eventual file path taking into account all variables.
    """

    parsed_url = urlparse(url)
    url_basename = basename(url)
    url_path = parsed_url.path
    resolved_basename = url_basename or "index"

    if output is None:
        url_basepath = dirname(url_path) if url_basename != "" else parsed_url.path
        joined = join(f".{url_basepath}", resolved_basename) + ".md"
        outfile = normpath(abspath(joined))
        return outfile
    # Output is not a directory and is most likely a file
    if basename(output) != "" and not isdir(output):
        return abspath(output)
    else:
        url_basepath = dirname(url_path) if url_basename != "" else parsed_url.path
        joined = join(f"{output}.{url_basepath}", resolved_basename) + ".md"
        outfile = normpath(abspath(joined))
        return outfile


def plural(count: int, singular: str, plural: str):
    """Return plural if count is greater than 1, otherwise return singular.

    Args:
        count: The number of an arbitrary item
        singular: The singular word variant or the default
        plural: The plural word variant
    Returns:
        returns signular or plural
    """
    return plural if count > 1 else singular


def get_config_from_toml_file(config_file: str) -> TOMLConfigDict:
    toml_content = toml.load(config_file)
    return TOMLConfigDict(**toml_content)
