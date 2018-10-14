export PYTHONPATH=.
VERSION=`cat _version.py | grep __version__ | sed "s/.*'\(.*\)'.*/\1/"`
PROJECT_SHORT=chinese
PROJECT_LONG=chinese-support-redux

all: test prep pack clean

test:
	pytest --cov="$(PROJECT_SHORT)" tests -v

prep:
	rm -f $(PROJECT_LONG)-v*.zip
	find . -name '*.pyc' -type f -delete
	find . -name '*~' -type f -delete
	find . -name .mypy_cache -type d -exec rm -rf {} +
	find . -name .ropeproject -type d -exec rm -rf {} +
	find . -name __pycache__ -type d -exec rm -rf {} +
	mv "$(PROJECT_SHORT)/meta.json" .
	cp LICENSE "$(PROJECT_SHORT)/LICENSE.txt"

pack:
	(cd "$(PROJECT_SHORT)" && zip -r ../$(PROJECT_LONG)-v$(VERSION).zip *)
	./convert-readme.py

clean:
	rm "$(PROJECT_SHORT)/LICENSE.txt"
	mv meta.json "$(PROJECT_SHORT)/meta.json"
