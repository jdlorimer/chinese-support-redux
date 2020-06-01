# Copyright © 2019 Daniel Rich <https://github.com/danielrich>
# Copyright © 2017-2020 Joseph Lorimer <joseph@lorimer.me>
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

PROJECT_SHORT = chinese
PROJECT_LONG = chinese-support-redux
VERSION = 0.14.0
XDG_DATA_HOME ?= $(HOME)/.local/share
ADDON_PATH = "$(XDG_DATA_HOME)/Anki2/addons21/$(PROJECT_LONG)"
ZIP_NAME = $(PROJECT_LONG)-v$(VERSION).zip

all: test prep pack clean

install: prep pack extract clean

test:
	pipenv install --dev
	pipenv run pytest --cov=$(PROJECT_SHORT) tests -v

prep:
	rm -f $(PROJECT_LONG)-v*.zip
	find . -name .hypothesis -type d -exec rm -rf {} +
	find . -name .mypy_cache -type d -exec rm -rf {} +
	find . -name .ropeproject -type d -exec rm -rf {} +
	find . -name __pycache__ -type d -exec rm -rf {} +
	find . -name '*.pyc' -type f -delete
	find . -name '*~' -type f -delete
	find . -name '.python-version' -type f -delete
	mv $(PROJECT_SHORT)/meta.json .
	mv $(PROJECT_SHORT)/config_saved.json .
	cp LICENSE $(PROJECT_SHORT)/LICENSE.txt
	git checkout chinese/data/db/chinese.db

pack:
	pipenv install --dev
	(cd $(PROJECT_SHORT) && zip -r ../$(ZIP_NAME) *)
	pipenv run ../misc/convert-readme.py

extract:
	rm -rf $(ADDON_PATH)
	unzip -d $(ADDON_PATH) $(ZIP_NAME)

clean:
	rm $(PROJECT_SHORT)/LICENSE.txt
	mv meta.json $(PROJECT_SHORT)/meta.json
	mv config_saved.json $(PROJECT_SHORT)/config_saved.json
	cat chinese/_version.py chinese/config.json Makefile | grep -i 'version[_" ].*[=:]' | tr -cd '[0-9\n]'
