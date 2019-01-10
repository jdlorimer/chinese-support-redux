# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <luoliyan@posteo.net>
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

from re import IGNORECASE, sub

from .consts import (
    COLOR_RUBY_TEMPLATE,
    COLOR_TEMPLATE,
    pinyin_regex,
    half_ruby_regex,
    HANZI_RANGE,
    ruby_regex,
)
from .hanzi import split_hanzi
from .sound import extract_sound_tags
from .transcribe import tone_number, sanitize_transcript
from .util import align, cleanup, is_punc, no_color


def colorize(words, ruby_whole=False):
    from .ruby import has_ruby

    assert isinstance(words, list)

    def colorize_ruby_sub(p):
        return '<span class="tone{t}">{r}</span>'.format(
            t=tone_number(p.group(2)), r=p.group()
        )

    def colorize_pinyin_sub(text, pattern):
        def repl(p):
            return '<span class="tone{t}">{r}</span>'.format(
                t=tone_number(p.group(1)), r=p.group()
            )

        colorized = ''
        for s in text.split():
            colorized += sub(pattern, repl, s, IGNORECASE)
        return colorized

    colorized = []
    for text in words:
        text = no_color(text)
        (text, sound_tags) = extract_sound_tags(text)

        if has_ruby(text):
            if ruby_whole:
                text = sub(ruby_regex, colorize_ruby_sub, text, IGNORECASE)
            else:
                text = colorize_pinyin_sub(text, half_ruby_regex)
        else:
            text = colorize_pinyin_sub(text, pinyin_regex)

        colorized.append(text + sound_tags)

    return ' '.join(colorized)


def colorize_dict(text):
    def _sub(p):
        s = ''
        hanzi = p.group(1)
        pinyin = p.group(2)
        delim = '|'

        if hanzi.count(delim) == 1:
            hanzi = hanzi.split(delim)
            s += colorize_fuse(hanzi[0], pinyin, True)
            s += delim
            s += colorize_fuse(hanzi[1], pinyin, False)
        else:
            s += colorize_fuse(hanzi, pinyin, True)

        return s

    return sub(r'([\%s|]+)\[(.*?)\]' % HANZI_RANGE, _sub, text)


def colorize_fuse(chars, transcript, ruby=False):
    chars = split_hanzi(cleanup(chars), grouped=False)
    transcript = sanitize_transcript(transcript)
    colorized = ''

    for c, t in align(chars, transcript):
        if c is None or t is None:
            continue
        if is_punc(c) and is_punc(t):
            colorized += c
            continue
        if ruby:
            colorized += COLOR_RUBY_TEMPLATE.format(
                tone=tone_number(t), chars=c, transcript=t
            )
        else:
            colorized += COLOR_TEMPLATE.format(tone=tone_number(t), chars=c)

    return colorized
