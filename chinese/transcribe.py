# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from re import compile, IGNORECASE, search, sub
from unicodedata import name, normalize

from .bopomofo import bopomofo
from .consts import (
    accents,
    bopomofo_regex,
    hanzi_regex,
    jyutping_finals,
    jyutping_inits,
    jyutping_standalones,
    pinyin_finals,
    pinyin_inits,
    pinyin_standalones,
    tone_number_regex,
    vowel_decorations
)
from .hanzi import has_hanzi
from .main import config, dictionary
from .ruby import has_ruby, ruby_bottom, ruby_top
from .util import cleanup, no_color


def pinyin_re_sub():
    return '(({})({})[1-5]?|({})[1-5]?)'.format(
        pinyin_inits, pinyin_finals, pinyin_standalones)


def jyutping_re_sub():
    return '(({})({})[1-6]?|({})[1-6]?)'.format(
        jyutping_inits, jyutping_finals, jyutping_standalones)


pinyin_re = pinyin_re_sub()
pinyin_two_re = compile("(?P<one>"+pinyin_re+")(?P<two>"+pinyin_re+")", IGNORECASE)

jyutping_re = jyutping_re_sub()
jyutping_two_re = compile("(?P<one>"+jyutping_re+")(?P<two>"+jyutping_re+")", IGNORECASE)


def transcribe(words, transcription=None, only_one=True):
    """Converts to specified transcription.

    Example: 你 becomes nǐ (transcription="Pinyin", only_one=True)

    Pinyin, Taiwan Pinyin and Bopomofo: lookup in local words dictionaries
    first, and use characters dictionary as a backup.

    If no transcription is specified, use the transcription set in the menu.
    """

    # if words is not a list, but a string like "中国"
    # filter down below would break the string up into a list of two characters
    # but this would break searching for words in the dictionary
    if not isinstance(words, (list,)):
        words = [words]

    words = list(filter(has_hanzi, words))
    transcribed = []

    if not words:
        return transcribed

    for text in words:
        text = cleanup(text)
        if not text:
            transcribed.append('')
        if not transcription:
            transcription = config['transcription']
        if transcription == 'Pinyin':
            transcribed.append(dictionary.get_pinyin(text, taiwan=False))
        elif transcription == 'Pinyin (Taiwan)':
            transcribed.append(dictionary.get_pinyin(text, taiwan=True))
        elif transcription == 'Cantonese':
            transcribed.append(dictionary.get_cantonese(text, only_one))
        elif transcription == 'Bopomofo':
            r = dictionary.get_pinyin(text, taiwan=True)
            transcribed.append(bopomofo(replace_tone_marks(r)))
        else:
            transcribed.append('')

    return transcribed


def get_char_transcription(hanzi, transcription=None):
    if not transcription:
        transcription = config['transcription']
    if transcription == 'Pinyin':
        return dictionary.get_pinyin(hanzi)
    if transcription == 'Pinyin (Taiwan)':
        return dictionary.get_pinyin(hanzi, taiwan=True)
    if transcription == 'Cantonese':
        return dictionary.get_cantonese(hanzi)
    if transcription == 'Bopomofo':
        return bopomofo(dictionary.get_pinyin(hanzi, taiwan=True))
    return str()


def accentuate(syllables):
    """Add accents to pinyin.

    Note: also removes coloring.
    """

    if config['transcription'] not in ['Pinyin', 'Pinyin (Taiwan)']:
        return syllables

    def _accentuate(p):
        pinyin = p.group(1)
        tone = p.group(2)
        pinyin = no_tone(pinyin)
        for v in 'aeouüviAEOUÜVI':
            if pinyin.find(v) > -1:
                try:
                    return sub(
                        v,
                        vowel_decorations[int(tone)][v.lower()],
                        pinyin,
                        count=1
                    )
                except (KeyError, IndexError):
                    pass
        return pinyin

    accentuated = []
    for text in syllables:
        text = no_color(text)
        text = sub(
            r'([a-z]*[aeiouüÜv' + accents + r'][a-zü]*)([1-5])',
            _accentuate,
            text,
            flags=IGNORECASE
        )
        accentuated.append(text)

    return accentuated


def replace_tone_marks(text):
    """Replace Pinyin tone marks with tone numbers."""

    if search(tone_number_regex, text) or search(bopomofo_regex, text):
        return text

    d = {
        'COMBINING MACRON'      : '1',
        'COMBINING ACUTE ACCENT': '2',
        'COMBINING CARON'       : '3',
        'COMBINING GRAVE ACCENT': '4',
    }

    done = []
    for syllable in text.split():
        tone = '5'

        if has_ruby(syllable):
            s = ruby_bottom(syllable) + '['
            syllable = ruby_top(syllable)
        else:
            s = str()

        for c in normalize('NFD', syllable):
            if name(c) in d:
                tone = d[name(c)]
            else:
                s += c

        s += tone
        if '[' in s:
            s += ']'

        done.append(normalize('NFC', s))

    return ' '.join(done)


def separate(pinyin, grouped=True):
    """Separate pinyin syllables."""

    def _clean(t):
        if t.startswith("'"):
            return t[1:]
        return t

    def _separate(p):
        return _clean(p.group('one')) + ' ' + _clean(p.group('two'))

    transcription = config['transcription']

    separated = []
    for text in pinyin.split():
        if transcription in ['Pinyin', 'Pinyin (Taiwan)']:
            text = pinyin_two_re.sub(_separate, text)
            text = pinyin_two_re.sub(_separate, text)

        if transcription in ['Cantonese']:
            text = jyutping_two_re.sub(_separate, text)
            text = jyutping_two_re.sub(_separate, text)

        if grouped:
            separated.append(text)
        else:
            separated.extend(text.split())

    return separated


def tone_number(s):
    s = replace_tone_marks(cleanup(s))

    if search(r'[0-9]$', s):
        return s[-1]

    if search(r'[¹²³⁴]$', s):
        return str(' ¹²³⁴'.index(s[-1:]))

    if search(bopomofo_regex, s):
        if search(r'[ˊˇˋ˙]$', s):
            return str('  ˊˇˋ˙'.index(s[-1]))
        return '1'

    return '5'


def no_tone(text):
    """Remove tone information and coloring."""

    text = no_color(text)
    text = replace_tone_marks(text)

    def _remove_tone(p):
        return p.group(1) + sub(tone_number_regex, '', p.group(2)) + ']'

    if has_ruby(text):
        return sub(r'(%s\[)([^[]+?)\]' % hanzi_regex, _remove_tone, text)

    return sub(r'([a-zü]+)%s' % tone_number_regex, r'\1', text)
