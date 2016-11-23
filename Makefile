all: clean build

git-clean:
	git rm -rf index.html db/

clean:
	rm -rf index.html db/

build:
	mkdir -p db/
	python build.py

pull:
	git pull

push:
	git add index.html db/
	git commit -am "update web content"
	git push
