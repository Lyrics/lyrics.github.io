#!/usr/bin/make -f

SASS_OPTS = --style compressed
HTML_FILES = index.html db/ sitemap.xml search.html 404.html
CSS_FILE = s.css

all: clean download build

clean:
	git rm -rf $(HTML_FILES) || rm -rf $(HTML_FILES)

build: css
	mkdir -p db/
	python build.py

download:
	git pull
	git submodule update --recursive --remote

add:
	git add $(HTML_FILES) $(CSS_FILE)

deploy: add
	git commit -m "Update web content"
	git push

serve:
	@echo "Starting local server at http://0.0.0.0:8100"
	@python -m SimpleHTTPServer 8100

css:
	@which sassc > /dev/null &2> /dev/null && \
         sassc ${SASS_OPTS} src/css/style.scss $(CSS_FILE) \
         || echo -n ''

.PHONY: all clean build download add deploy serve css
