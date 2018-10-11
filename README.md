# Chinese Support Redux

[![Build Status](https://travis-ci.org/luoliyan/chinese-support-redux.svg?branch=master)](https://travis-ci.org/luoliyan/chinese-support-redux) ![Coveralls github branch](https://img.shields.io/coveralls/github/luoliyan/chinese-support-redux/master.svg)

A rewrite and port of the Chinese Support add-on to Anki 2.1.

## Features

* Automatic field filling
  * Translation (from built-in dictionary; supports English, German and French)
  * Romanisation (supports [Pinyin](https://en.wikipedia.org/wiki/Pinyin) and Cantonese [Jyutping](https://en.wikipedia.org/wiki/Jyutping))
  * Audio (fetched from Google or Baidu; supports Mandarin and Cantonese)
  * Simplified and traditional characters
  * [Bopomofo/Zhuyin](https://en.wikipedia.org/wiki/Bopomofo)
* Tone colours (applied to characters, romanisation and Bopomofo)
* Built-in note types (basic and advanced)

## Status

The vast majority of features have been successfully ported, and the add-on is in a usable state, albeit with some definite rough edges.

The add-on is still in beta. By this I mean “it works, but I wouldn’t trust it with my children”. Expect occasional issues, and please make a back-up before trying it. I use it myself and haven't experienced data loss, but _your_ mileage may vary.

Please report any issues [here](https://github.com/luoliyan/chinese-support-redux/issues) on GitHub. Feature requests are also welcome.

If you are new to the Chinese Support add-on, the wiki from the previous version is still relevant ([here](https://github.com/ttempe/chinese-support-addon/wiki)).

## Usage

The core feature of the add-on is the automatic field filling. To take advantage of this, you need to have an Anki note type with the appropriate fields (e.g., `Hanzi`, `Meaning`, `Reading`, `Sound`). If you don't already have such a note type, the easiest way to create one is to use the built-in model:

1. Navigate to Tools → Manage Note Types (or press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>N</kbd>)
2. Click `Add`
3. Select `Add: Chinese (basic)`
4. Click `OK`
5. Click `OK` again
6. Click `Close`

Then, to use the field filling features:

1. Add a new note to Anki (press <kbd>a</kbd>)
2. Select `Chinese (basic)` as the note type
3. Enable Chinese Support Redux for this note type (click `汉字`)
4. Enter a word (e.g., 電話) in the `Hanzi` field
5. Press <kbd>Tab</kbd>
6. The remaining fields should then be populated automatically

## History

- **v0.5.3-beta (2018.10.10)**
  - Refactor TTS code
  - Bundle Google TTS dependencies
  - Remove Cantonese TTS (discontinued by Google)
- **v0.5.0-beta (2018.10.09)**
  - Restore Google TTS (again)
  - Begin seriously starting to wrap tests around this old, buggy code
- **v0.4.1-beta (2018.02.17)**
  - Fix _Fill Incomplete Notes_ functionality
- **v0.4.0-beta (2017.11.14)**
  - Fix more issues with automatic field population
  - Move field names into configuration file
- **v0.3.1-beta (2017.11.10)**
  - Use built-in configuration facilities
- **v0.3-beta (2017.11.07)**
  - Fix issues with automatic field population
- **v0.2-beta (2017.11.06)**
  - Restore Google TTS (for Mandarin and Cantonese)
- **v0.1-beta (2017.11.05)**
  - Initial port to Anki 2.1 (most features working)
  - Restore tone colours in editor
