#!/usr/bin/make -f

HTML_FILES = index.html db/ sitemap.xml s.htm 404.html
ASSET_FILES = s.css js/ 2.svg 3.svg 4.svg favicon.ico

clean:
	git rm -rf $(HTML_FILES) $(ASSET_FILES) || rm -rf $(HTML_FILES) $(ASSET_FILES)

add:
	git add $(HTML_FILES) $(ASSET_FILES)

deploy: add
	git commit -m "Update website content"
	git push

.PHONY: clean add deploy
