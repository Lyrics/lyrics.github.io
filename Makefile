all: clean build

git-clean:
	git rm -rf index.htm db/

clean:
	rm -rf index.htm db/

build:
	mkdir -p db/
	python build.py

pull:
	git pull

push:
	git add index.htm db/
	git commit -am "update web content"
	git push
