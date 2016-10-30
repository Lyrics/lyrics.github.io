all: update clean build

update:
	git submodule update --recursive --remote

clean:
	rm -rf static || git rm -rf static

build:
	mkdir -p static/db
	python build.py

pull:
	git pull

push:
	git add index.htm db
	git commit -am "generate new web content"
	git push
