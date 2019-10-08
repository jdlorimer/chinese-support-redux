# Copyright 2017-2018 Joseph Lorimer <joseph@lorimer.me>
#
# Permission to use, copy, modify, and distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright
# notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

export PYTHONPATH=.
VERSION=`cat _version.py | grep __version__ | sed "s/.*'\(.*\)'.*/\1/"`
PROJECT_SHORT=chinese
PROJECT_LONG=chinese-support-redux
PYTEST=pytest

all: test prep pack clean

test:
	"$(PYTEST)" --cov="$(PROJECT_SHORT)" tests -v

prep:
	rm -f $(PROJECT_LONG)-v*.zip
	find . -name '*.pyc' -type f -delete
	find . -name '*~' -type f -delete
	find . -name '.python-version' -type f -delete
	find . -name .mypy_cache -type d -exec rm -rf {} +
	find . -name .ropeproject -type d -exec rm -rf {} +
	find . -name __pycache__ -type d -exec rm -rf {} +
	mv "$(PROJECT_SHORT)/meta.json" .
	mv "$(PROJECT_SHORT)/config_saved.json" .
	cp LICENSE "$(PROJECT_SHORT)/LICENSE.txt"
	git checkout chinese/data/db/chinese.db

pack:
	(cd "$(PROJECT_SHORT)" && zip -r ../$(PROJECT_LONG)-v$(VERSION).zip *)
	(cd "$(PROJECT_SHORT)" && zip -r ../package.zip *)
	./convert-readme.py

OS := $(shell uname)
ifeq ($(OS),Darwin)
	ANKI_PATH = ${HOME}/Library/Application Support/Anki2/addons21/chinese-support-redux
endif
ifeq ($(OS),Linux)
	ANKI_PATH = ${HOME}/.local/share/Anki2/addons21/chinese-support-redux
endif


# installs into local anki for testing.
install:
	rm -rf package
	mkdir package
	cp package.zip package
	cd package && unzip package.zip
	rm package/package.zip
	rm -rf "${ANKI_PATH}"
	cp -r package "${ANKI_PATH}"

clean:
	rm "$(PROJECT_SHORT)/LICENSE.txt"
	mv meta.json "$(PROJECT_SHORT)/meta.json"
	mv config_saved.json "$(PROJECT_SHORT)/config_saved.json"
