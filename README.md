# Experiment to Modernize the Debian Wiki (Outreachy Contribution)

This is an Outrecahy contribution project from Daniel Adepitan to complete the task as defined on the
contribution page of the internship project
https://www.outreachy.org/outreachy-december-2023-internship-round/communities/debian/#experiment-to-modernize-the-debian-wiki

## Synopsis

A basic Python program to convert the Debian Wiki News page (https://wiki.debian.org/News) to markdown.

## Usage

A shell script, `run.sh`, is provided together with a `Makefile` to make usage easier and a no-brainer.

The `run.sh` script will do the necessary bootstrapping, setup and installations, but if you want more control,
you can reach into the `main.py` file directly, having the same CLI API as the `run.sh` script, and do the
installations and setup manually.

For the first time you may want to run:

```bash
chmod +x ./run.sh
```

There are two conversion options provided for easy customization:

- There's the option to convert the whole page to markdown
- There's the option to convert the main content area of the page `div#page` (`<div id="page">...</div>`)
  to markdown

By calling `./run.sh` the whole page would be converted to markdown on a best-effort basis. Calling `run.sh`
with a `--main=<main-content-id>` flag will only convert the main content area to markdown.

```bash
# ./run.sh <url>
./run.sh https://wiki.debian.org/News
```

This converts the entire page to markdown

```bash
# ./run.sh <url> --main=page
./run.sh https://wiki.debian.org/News --main=page
```

This converts the main content area of the page to markdown

Alternatively, using the provided `Makefile` which is more intuitive:

```bash
make deb-wiki-news-to-md
```

This converts the entire page to markdown

```bash
make deb-wiki-news-main-to-md
```

This converts the main content area of the page to markdown

## Author

Daniel Adepitan

