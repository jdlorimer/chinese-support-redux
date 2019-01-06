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

from .consts import pinyin_regex, half_ruby_regex, ruby_regex
from .hanzi import separate_chars
from .sound import extract_sound_tags
from .transcribe import accentuate, separate_trans, tone_number
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


def colorize_fuse(chars, trans, ruby=False):
    """Colorize hanzi based on pinyin tone.

    If ruby=True, then annotate hanzi with pinyin.
    """

    standard_fmt = '<span class="tone{tone}">{chars}</span>'
    ruby_fmt = (
        '<span class="tone{tone}"><ruby>{chars}<rt>{trans}</rt></ruby></span>'
    )

    chars = separate_chars(cleanup(chars), grouped=False)
    trans = sanitize_pinyin(trans)
    text = ''

    for c, t in align(chars, trans):
        if c is None or t is None:
            continue
        if is_punc(c) and is_punc(t):
            text += c
            continue
        if ruby:
            text += ruby_fmt.format(tone=tone_number(t), chars=c, trans=t)
        else:
            text += standard_fmt.format(tone=tone_number(t), chars=c)

    return text


def colorize_dict(text):
    """Colorize text in the form: 你好[ni3 hao].

    As used in the local dictionaries.
    """

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

    return sub(r'([\u3400-\u9fff|]+)\[(.*?)\]', _sub, text)


def sanitize_pinyin(pinyin, grouped=False):
    return ' '.join(
        accentuate(separate_trans(cleanup(no_color(pinyin)), grouped))
    ).split()
