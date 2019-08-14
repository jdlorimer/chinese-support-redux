# Chinese Support Redux

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6b99fcb30a2142d899f79c601a6aa291)](https://app.codacy.com/app/luoliyan/chinese-support-redux?utm_source=github.com&utm_medium=referral&utm_content=luoliyan/chinese-support-redux&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/luoliyan/chinese-support-redux.svg?branch=master)](https://travis-ci.org/luoliyan/chinese-support-redux) [![Coverage Status](https://coveralls.io/repos/github/luoliyan/chinese-support-redux/badge.svg?branch=master)](https://coveralls.io/github/luoliyan/chinese-support-redux?branch=master)

Chinese Support Redux is a rewrite and port of the Chinese Support add-on to Anki 2.1. It offers a number of features that streamline the process of creating flashcards for learning Chinese. The current focus of development effort is on improving the stability of the add-on and the accuracy of its output. Once the core functionality is sufficiently robust and reliable, additional features will be considered. While many of the changes will be structural in nature, I would encourage users to update the add-on whenever the version number increases and notify me of any problems. Your feedback is important.

The original (and 2.1-incompatible) version is available [here](https://github.com/ttempe/chinese-support-addon).

## Features

- Automatic field filling
  - Translation (from built-in dictionary; supports English, German and French)
  - Romanisation (supports [Pīnyīn (拼音)](https://en.wikipedia.org/wiki/Pinyin) and Cantonese [Jyutping (粵拼)](https://en.wikipedia.org/wiki/Jyutping))
  - Mandarin Audio (fetched from Google or Baidu)
  - Traditional (繁體字) and simplified (簡體字) characters
  - [Bopomofo (ㄅㄆㄇㄈ)](https://en.wikipedia.org/wiki/Bopomofo), also known as Zhuyin (注音)
  - [Rubies](https://www.w3schools.com/tags/tag_ruby.asp) (small-print transcription placed above characters)
- Tone colours (applied to characters, romanisation and Bopomofo)
- Built-in note types (Basic and Advanced)

## Status

The vast majority of features have been successfully ported, and the add-on is in a usable state, albeit with some definite rough edges.

The add-on is still in beta. By this I mean “it works, but I wouldn’t trust it with my children”. Expect occasional issues, and please make a back-up before trying it. I use it myself and haven't experienced data loss, but _your_ mileage may vary.

Please report any issues [here](https://github.com/luoliyan/chinese-support-redux/issues) on GitHub. Feature requests are also welcome.

If you are new to the Chinese Support add-on, the wiki from the previous version is still relevant ([here](https://github.com/ttempe/chinese-support-addon/wiki)).

## Usage

The core feature of the add-on is the automatic field filling. To take advantage of this, you need to have an Anki note type with the appropriate fields (e.g., `Hanzi`, `Meaning`, `Reading`, `Sound`). See `config.json` for a list of valid field names.

If you don't already have such a note type, the easiest approach is to use one of the built-in models. Two types are installed automatically: Basic and Advanced. The only important difference is that the Advanced model shows more information.

To use the field-filling features:

1. Add a new note to Anki (press <kbd>a</kbd>)
2. Select `Chinese (Basic)` or `Chinese (Advanced)` as the note type
3. Enable Chinese Support Redux for this note type (click `汉字`)
4. Enter a word (e.g., 電話) into the `Hanzi` field (sentences will also work)
5. Press <kbd>Tab</kbd>
6. The remaining fields should then be populated automatically

## Screenshots

![Screenshot #1](https://raw.githubusercontent.com/luoliyan/chinese-support/master/screenshots/add-card.png)

![Screenshot #2](https://raw.githubusercontent.com/luoliyan/chinese-support/master/screenshots/view-card.png)

## Support

If you encounter any issues, the best way to have these addressed is to [raise them on GitHub](https://github.com/luoliyan/chinese-support-redux/issues). Feature requests are welcome, with the caveat that all good things take time.

I understand the documentation is sparse. Anyone who wishes to add content to [the wiki](https://github.com/luoliyan/chinese-support-redux/wiki) is more than welcome to.

## Testing

For those who wish to run the tests locally, this is fairly straightforward.

Clone the repository:

```sh
git clone https://github.com/luoliyan/chinese-support-redux
cd chinese-support-redux
```

Ideally, set up a virtual environment to isolate the project:

```sh
curl https://pyenv.run | bash
pyenv virtualenv 3.6.8 csr
pyenv local csr
```

Install dependencies and run the tests:

```sh
pip install -r requirements.txt
make test
```

