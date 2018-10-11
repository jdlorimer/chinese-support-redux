VERSION = `cat _version.py | grep __version__ | sed "s/.*'\(.*\)'.*/\1/"`

all: prep pack clean

prep:
	rm -f chinese-support-redux-v*.zip
	find . -name '*.pyc' -type f -delete
	find . -name '*~' -type f -delete
	find . -name .mypy_cache -type d -exec rm -rf {} +
	find . -name .ropeproject -type d -exec rm -rf {} +
	find . -name __pycache__ -type d -exec rm -rf {} +
	mv chinese/meta.json .
	cp LICENSE chinese/LICENSE.txt

pack:
	(cd chinese && zip -r ../chinese-support-redux-v$(VERSION).zip *)
	./convert-readme.py

clean:
	rm chinese/LICENSE.txt
	mv meta.json chinese/meta.json
