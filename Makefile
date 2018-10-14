HTMLs = index.html db/ sitemap.xml search.html 404.html

all: clean download build

clean:
	git rm -rf $(HTMLs) || rm -rf $(HTMLs)

build:
	mkdir -p db/
	python build.py

download:
	git pull
	git submodule update --recursive --remote

add:
	git add $(HTMLs)

deploy: add
	git commit -m "update web content"
	git push

serve:
	@echo "Starting local server at http://0.0.0.0:8100"
	@python -m SimpleHTTPServer 8100

.PHONY: all clean build download add deploy serve
