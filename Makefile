all: update clean build

update:
	#git pull
	git submodule update --recursive --remote

clean:
	rm -rf db || git rm -rf db

build:
	mkdir -p db
	python build.py
