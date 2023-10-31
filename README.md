# Experiment to Modernize the Debian Wiki (Outreachy Contribution)

This is an Outrecahy contribution project from Daniel Adepitan to complete the task as defined on
the contribution page of the internship project
https://www.outreachy.org/outreachy-december-2023-internship-round/communities/debian/#experiment-to-modernize-the-debian-wiki

## Synopsis

A basic Python program to convert the Debian Wiki News page (https://wiki.debian.org/News) to
markdown.

## Local Installation

This package provides a `setup.py` script that can be used to install the package. You can install
the package locally by running the following script:

> It's worth noting that installation should be done in a virtual environment rather than in the
> system path of your Python installation. So you may want to create a virtual env first
>
> `python -m venv .venv`
>
> `. .venv/bin/activate`
>
> There are two installation modes in the Makefile.
>
> - **Dev mode**: For development purposes. This is useful when changes are made in the source code
>   that need to take effect without needing to re-install.
> - **Standard mode**: For production ready environments. This installs the package as it would
>   normally do if the package were on a registry, but without the network requests for fetching the
>   package artifacts.

**Dev mode**:

```bash
make install-dev-local # pip3 install --editable=.
```

**Standard mode**:

```bash
make install-local # pip3 install .
```

and you can also uninstall by running:

```bash
make uninstall-local
```

The package after installation exposes a cli program with the name `deb_wiki_mod`.

**Basic usage**

```bash
deb_wiki_mod down <url> [--page-id] [-o|--output]
deb_wiki_mod toml <path>
```

[See #Usage](#usage) for more

## Usage

Appropriate usage is by installing the package as you would any other Python package. This package
is not on a registry so only local installation is available. After installing, you can call the
program from the command line like so:

```bash
deb_wiki_mod down https://wiki.debian.org/News
```

By default, this outputs a markdown file with a filename the same as the basename of the provided
URL in the current working directory, except a desired output file path is specified. The output
option can specify either a directory or a filepath. When a filepath is specified, the resulting
markdown content is saved to the filepath. When a directory is specified, the resulting markdown is
saved to that directory and may contain subdirectories based on the pathname of the URL and the
basename of the URL. In situations where the URL doesn't have a basename, "index" is used, followed
by an appropriate file extension (e.g., `.md`)

```bash
deb_wiki_mod down https://wiki.debian.org/News --output wiki-news.md
```

The main content element of the page can also be specified by `id` this helps to skip page layout
content and avoids duplication when generating markdown for multiple pages with the same basic
layout.

```bash
deb_wiki_mod down https://wiki.debian.org/News --output wiki-news.md --page-id page
```

To process multiple URLs at once, a TOML config file may be used. A basic TOML config file looks
something like this:

```toml
# deb_wiki.toml
[root]
output = "./markdown"

[[root.pages]]
url = "https://wiki.debian.org/News"
output = "News.md"
page_id = "page"

[[root.pages]]
url = "https://www.debian.org/News/project/"
page_id = "content"
```

```bash
deb_wiki_mod toml ./deb_wiki.toml
```

This generates the files `./News.md` and `./News/project/index.md` in `./markdown` directory.

**Note:**

Paths in the TOML config file are resolved relative to the path of the TOML file rather than the
`cwd`

### Non standard zero installation usage

A shell script, `run.sh`, is provided together with a `Makefile` to make usage easier and a
no-brainer.

The script will do the necessary bootstrapping, setup and installations, but if you want more
control, you can reach into the `main.py` file directly, having the same CLI API as the shell
script, and do the installations and setup manually.

For the first time you may want to run:

```bash
chmod +x ./run.sh
```

There are two conversion options provided for easy customization:

- There's the option to convert the whole page to markdown
- There's the option to convert the main content area of the page if you want to skip layout content
  which could be the same for many pages

Note: all arguments passed to the shell script is redirected to the Python program file.

By calling `./run.sh` the whole page would be converted to markdown on a best-effort basis. Calling
`run.sh` with a `--main=<main-content-id>` flag will only convert the main content area to markdown.

```bash
# ./run.sh <url>
./run.sh down https://wiki.debian.org/News
```

This converts the entire page to markdown

```bash
# ./run.sh down <url> --page-id=page
./run.sh down https://wiki.debian.org/News --page-id=page
```

This converts the main content area of the page to markdown

Alternatively, using the provided `Makefile` which is more intuitive and less generic (specific to
Debian Wiki News page):

```bash
make deb-wiki-news-to-md
```

This converts the entire page to markdown

```bash
make deb-wiki-news-main-to-md
```

This converts the main content area of the page to markdown

## Command Line Options

The command line is the entry interface provided by this program and there aren't much of any
application programming interface exposed to be interfaced with by another script other than through
the command line.

| Command                    | Description                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------ |
| `deb_wiki_mod down <url>`  | Download the HTML page from the URL and parse it to markdown                                     |
| `deb_wiki_mod toml <path>` | Take a path to a TOML file containing URLs to HTML pages to be downloaded and parsed to markdown |

**`deb_wiki_mod down <url>`**

| Argument       | Description                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `--page-id`    | Used to specify the id of the main content area of the page (`<main id="main">...</main>`, `--page-id=main`) |
| `-o\|--output` | Specifies the output file path or output directory                                                                     |

## LICENSE

MIT License Copyright (c) 2023 Daniel Adepitan
