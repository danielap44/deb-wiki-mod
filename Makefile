deb-wiki-news-to-md:
	./run.sh https://wiki.debian.org/News
deb-wiki-news-main-to-md:
	./run.sh https://wiki.debian.org/News --main=page

install-dev-local:
	pip3 install --editable=.

install-local:
	pip3 install .

uninstall-local:
	pip3 uninstall deb_wiki_mod

test:
	PYTHONDONTWRITEBYTECODE=1 python -m unittest discover

python-clean:
	find . -type d -name "__pycache__" ! -path "./venv/*" -exec rm -rf {} +