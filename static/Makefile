all: update clean build

update:
	git submodule update --recursive --remote

clean:
	rm -rf db index.htm

build:
	mkdir -p db
	python build.py

pull:
	git pull

push:
	git add index.htm db
	git commit -am "generate new web content"
	git push
