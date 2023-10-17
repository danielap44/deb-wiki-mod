deb-wiki-news-to-md:
	./run.sh https://wiki.debian.org/News
deb-wiki-news-main-to-md:
	./run.sh https://wiki.debian.org/News --main=page

install-local:
	pip3 install --editable=.
uninstall-local:
	pip3 uninstall deb_wiki_mod