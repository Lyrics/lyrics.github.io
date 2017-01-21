all: clean pull build

clean:
	git rm -rf index.html db/ sitemap.xmp search.html || rm -rf index.html db/ sitemap.xml search.html

build:
	mkdir -p db/
	python build.py

pull:
	git pull
	git submodule update --recursive --remote

push:
	git add index.html db/ sitemap.xml search.html
	git commit -m "update web content"
	git push

server:
	python -m SimpleHTTPServer 8100

.PHONY: all clean build pull push server
