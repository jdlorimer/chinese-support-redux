# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
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

from re import IGNORECASE, search, split, sub
from unicodedata import name, normalize

from .bopomofo import bopomofo
from .consts import (
    accents,
    bopomofo_regex,
    DIACRITIC_TO_TONE,
    hanzi_regex,
    jyutping_split_regex,
    not_pinyin_regex,
    pinyin_split_regex,
    punc_map,
    tone_number_regex,
    TONE_NUMBERS,
    vowel_decorations,
)
from .hanzi import has_hanzi
from .main import config, dictionary
from .ruby import has_ruby, ruby_bottom, ruby_top, separate_ruby
from .util import cleanup, is_punc, no_color


def convert_punc(a):
    converted = []
    for s in a:
        if s in punc_map:
            converted.append(punc_map[s])
        else:
            converted.append(s)
    return converted


def is_sentence(s):
    if len(s) > 6:
        return True
    for c in s:
        if is_punc(c):
            return True
    return False


def transcribe(words, target, type_):
    assert isinstance(words, list)

    if target == 'pinyin':
        prefer_tw = False
    elif target in ['pinyin_tw', 'bopomofo']:
        prefer_tw = True
    elif target != 'jyutping':
        raise NotImplementedError(target)

    transcribed = []

    if not list(filter(has_hanzi, words)):
        return transcribed

    for text in words:
        text = cleanup(text)

        if not has_hanzi(text):
            transcribed.append(text)
            continue

        if target in ['pinyin', 'pinyin_tw', 'bopomofo']:
            s = dictionary.get_pinyin(text, type_, prefer_tw)
        elif target == 'jyutping':
            s = dictionary.get_cantonese(text, type_)

        if target == 'bopomofo':
            transcribed.extend(bopomofo([s]))
        else:
            transcribed.append(s)

    return convert_punc(transcribed)


def transcribe_char(hanzi, target, type_):
    if target == 'pinyin':
        return dictionary.get_pinyin(hanzi, type_)
    if target == 'pinyin_tw':
        return dictionary.get_pinyin(hanzi, type_, prefer_tw=True)
    if target == 'jyutping':
        return dictionary.get_cantonese(hanzi, type_)
    if target == 'bopomofo':
        return bopomofo(dictionary.get_pinyin(hanzi, type_, prefer_tw=True))

    raise NotImplementedError(target)


def accentuate(syllables, target):
    assert isinstance(syllables, list)

    if target not in ['pinyin', 'pinyin_tw']:
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
                        count=1,
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
            flags=IGNORECASE,
        )
        accentuated.append(text)

    return accentuated


def replace_tone_marks(pinyin):
    assert isinstance(pinyin, list)
    result = []
    for bottom, top in separate_ruby(pinyin):
        a = []
        for syllable in split_transcript(top, target='pinyin', grouped=False):
            s = get_tone_number_pinyin(syllable)
            if bottom:
                s = f'{bottom}[{s}]'
            a.append(s)
        result.append(' '.join(a))
    return result


def get_tone_number_pinyin(syllable):
    assert isinstance(syllable, str)

    if (
        search(tone_number_regex, syllable)
        or search(bopomofo_regex, syllable)
        or is_punc(syllable)
    ):
        return syllable

    if has_ruby(syllable):
        s = ruby_bottom(syllable) + '['
        syllable = ruby_top(syllable)
    else:
        s = ''

    tone = '5'
    for c in normalize('NFD', syllable):
        if name(c) in DIACRITIC_TO_TONE:
            tone = DIACRITIC_TO_TONE[name(c)]
        else:
            s += c

    if '[' in s:
        s += ']'

    return normalize('NFC', s + tone)


def split_transcript(transcript, target, grouped=True):
    assert isinstance(transcript, str)

    if target not in ['pinyin', 'pinyin_tw', 'jyutping']:
        raise NotImplementedError(target)

    def _clean(t):
        if t.startswith("'"):
            return t[1:]
        return t

    def _split(p):
        return _clean(p.group('one')) + ' ' + _clean(p.group('two'))

    separated = []

    for text in split(not_pinyin_regex, transcript):
        if target in ['pinyin', 'pinyin_tw']:
            text = pinyin_split_regex.sub(_split, text)
            text = pinyin_split_regex.sub(_split, text)
        elif target == 'jyutping':
            text = jyutping_split_regex.sub(_split, text)
            text = jyutping_split_regex.sub(_split, text)

        if grouped:
            separated.append(text)
        else:
            separated.extend(text.split())

    return list(filter(lambda s: s.strip(), separated))


def tone_number(s):
    assert isinstance(s, str)

    s, *_ = replace_tone_marks([cleanup(s)])

    if search(f'[¹²³⁴]$', s):
        return str(' ¹²³⁴'.index(s[-1:]))

    if search(f'[{TONE_NUMBERS}]$', s):
        return s[-1]

    if search(bopomofo_regex, s):
        if search(r'[ˊˇˋ˙]$', s):
            return str('  ˊˇˋ˙'.index(s[-1]))
        return '1'

    return '5'


def no_tone(text):
    assert isinstance(text, str)

    text = no_color(text)
    text, *_ = replace_tone_marks([text])

    def _remove_tone(p):
        return p.group(1) + sub(tone_number_regex, '', p.group(2)) + ']'

    if has_ruby(text):
        return sub(r'(%s\[)([^[]+?)\]' % hanzi_regex, _remove_tone, text)

    return sub(r'([a-zü]+)%s' % tone_number_regex, r'\1', text)


def sanitize_transcript(transcript, target, grouped=False):
    return ' '.join(
        accentuate(
            split_transcript(cleanup(no_color(transcript)), target, grouped),
            target,
        )
    ).split()
