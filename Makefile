deb-wiki-news-to-md:
	./run.sh https://wiki.debian.org/News
deb-wiki-news-main-to-md:
	./run.sh https://wiki.debian.org/News --main=page

install-local:
	pip install --editable=.
uninstall-local:
	pip uninstall deb_wiki_mod