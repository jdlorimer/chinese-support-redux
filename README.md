# Chinese Support Redux

[![Build Status](https://travis-ci.org/luoliyan/chinese-support-redux.svg?branch=master)](https://travis-ci.org/luoliyan/chinese-support-redux) [![Coverage Status](https://coveralls.io/repos/github/luoliyan/chinese-support-redux/badge.svg?branch=master)](https://coveralls.io/github/luoliyan/chinese-support-redux?branch=master)

Chinese Support Redux is a rewrite and port of the Chinese Support add-on to Anki 2.1. It offers a number of features that streamline the process of creating flashcards for learning Chinese. The current focus of development effort is on improving the stability of the add-on and the accuracy of its output. Once the core functionality is sufficiently robust and reliable, additional features will be considered. While many of the changes will be structural in nature, I would encourage users to update the add-on whenever the version number increases and notify me of any problems. Your feedback is important.

The original (and 2.1-incompatible) version is available [here](https://github.com/ttempe/chinese-support-addon).

**Note**: The add-on has undergone a major rewrite during January to make it more maintainable going forward. This should address many of the issues that were raised last year, but is likely to have introduced different issues I am not aware of. The best way to have these fixed is to [raise them on GitHub](https://github.com/luoliyan/chinese-support-redux/issues).

**Additional Note**: Anyone who wishes to add content to [the wiki](https://github.com/luoliyan/chinese-support-redux/wiki) is more than welcome to.


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

## History

- **2019.04.02**
  - Update bundled libs
    - Fixes gTTS error (hat tip: Robert Irelan)
- **2019.01.17**
  - Use `jieba` library for segmentation
    - Should fix most issues with inaccurate Pinyin
  - Fix Bopomofo generation (courtesy of Matthias Wimmer)
  - Fix errors caused by rare characters (courtesy of Robert Irelan)
  - Fix several broken function calls
  - Fix handling of mixed Chinese/English
  - Major refacting and test expansion
- **2019.01.01**
  - Fix bulk filling of Pinyin
  - Refactor several near-duplicate functions
  - Expand tests
- **2018.12.25**
  - Fix accentuate call errors
  - Fix handling of punctuation by colorize functions
  - Try to identify sentences vs. vocab and handle appropriately
  - Respect word separation in Hanzi field
  - Add Chinese→English punctuation mapping
  - Don't apply tone number to punctuation
  - Save configuration on exit
  - Expand tests
  - Tweak regular expressions
  - Tweak searchable HTML formatting
- **2018.11.30**
  - Update `gTTS-token` (fixes TTS error)
- **2018.11.15**
  - Expand tests
  - Fix and refactor definition filling code
  - Fix incorrect fill counts
- **2018.11.14**
  - Remove bogus tone number from TTS input
  - Simplify inclusion of required libs
- **2018.11.13**
  - Fix incorrect model names
  - Expand and refactor tests
- **2018.11.09**
  - Fix field filling for alternative forms
  - Fix bulk field filling
  - Fix and relocate menu
  - Add models automatically on start-up
  - Refactor tests
  - Tweak configuration
- **2018.10.26**
  - Fix Pinyin and Bopomofo coloring
  - Fix classifier rubies (show one ruby per classifier)
  - Handle non-hanzi in Hanzi field _slightly_ more gracefully
  - Only attempt to add DB indices on first run
- **2018.10.25**
  - Major refactoring and test expansion
    - Functions under test should be more reliable
    - Functions not under test are still black magic
  - Fix several issues with Bopomofo handling
  - Fix filling of classifier field
  - Make splitting of Pinyin optional (internally)
- **2018.10.12**
  - Improve handling of Pinyin (will no longer split)
  - Refactor start-up code
  - Expand and refactor tests
- **2018.10.11**
  - Bundle Google TTS dependencies
  - Improve character selection (courtesy of infernalis)
- **2018.10.10**
  - Refactor TTS code
  - Remove Cantonese TTS (discontinued by Google)
- **2018.10.09**
  - Restore Google TTS (again)
  - Begin seriously starting to wrap tests around this old, buggy code
- **2018.02.17**
  - Fix _Fill Incomplete Notes_ functionality
- **2017.11.14**
  - Fix more issues with automatic field population
  - Move field names into configuration file
- **2017.11.10**
  - Use Anki 2.1 built-in config facilities
- **2017.11.07**
  - Fix issues with automatic field population
- **2017.11.06**
  - Restore Google TTS (for Mandarin and Cantonese)
- **2017.11.05**
  - Initial port to Anki 2.1 (most features working)
  - Restore tone colours in editor
