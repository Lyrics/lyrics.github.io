all: update clean build

update:
	git submodule update --recursive --remote

clean:
	rm -f index.htm
	rm -rf db || git rm -rf db

build:
	mkdir -p db
	python build.py

pull:
	git pull

push:
	git add index.htm db
	git commit -am "generate new web content"
	git push
