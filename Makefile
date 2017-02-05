HTMLs = index.html db/ sitemap.xml search.html 404.html

all: clean pull build

clean:
	git rm -rf $(HTMLs) || rm -rf $(HTMLs)

build:
	mkdir -p db/
	python build.py

pull:
	git pull
	git submodule update --recursive --remote

push:
	git add $(HTMLs)
	git commit -m "update web content"
	git push

server:
	python -m SimpleHTTPServer 8100

.PHONY: all clean build pull push server
