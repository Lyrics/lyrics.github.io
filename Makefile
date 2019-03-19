#!/usr/bin/make -f

HTML_FILES = index.html db/ sitemap.xml search.html 404.html
CSS_FILE = s.css

clean:
	git rm -rf $(HTML_FILES) $(CSS_FILE) || rm -rf $(HTML_FILES) $(CSS_FILE)

add:
	git add $(HTML_FILES) $(CSS_FILE)

deploy: add
	git commit -m "Update web content"
	git push

.PHONY: clean add deploy
