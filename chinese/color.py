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

from re import IGNORECASE, sub

from .consts import accents
from .sound import extract_sound_tags
from .transcribe import accentuate, separate, tone_number, transcribe
from .util import cleanup, no_color, no_hidden


def colorize(words, ruby_whole=False):
    """Add tone color info. Works on transcription, hanzi or ruby.

    Note: Can be seen in the card preview, but not the note edit view.

    In the case of ruby, it will colorize only the annotation by default.
    If ruby_whole = True, then it will colorize the whole character.
    """

    from .ruby import has_ruby

    if not isinstance(words, list):
        words = sanitize_pinyin(words)

    def colorize_ruby_sub(p):
        return '<span class="tone{t}">{r}</span>'.format(
            t=tone_number(p.group(2)),
            r=p.group()
        )

    def colorize_pinyin_sub(text, pattern):
        def repl(p):
            return '<span class="tone{t}">{r}</span>'.format(
                t=tone_number(p.group(1)),
                r=p.group()
            )

        return sub(pattern, repl, text, IGNORECASE).replace('> <', '><')

    whole_ruby_pattern = (
        r'([\u3400-\u9fff]\[\s*)([a-zü' +
        accents +
        r']+1?[0-9¹²³⁴]?)(.*?\])'
    )
    half_ruby_pattern = r'([a-zü' + accents + r']+1?[0-9¹²³⁴]?)'
    pinyin_pattern = (
        r'([&<"/]?[a-zü\u3100-\u312F' +
        accents +
        r']+1?[0-9¹²³⁴ˊˇˋ˙]?)'
    )

    colorized = []
    for text in words:
        text = no_color(text)
        (text, sound_tags) = extract_sound_tags(text)

        if has_ruby(text):
            if ruby_whole:
                text = sub(
                    whole_ruby_pattern,
                    colorize_ruby_sub,
                    text,
                    flags=IGNORECASE
                )
            else:
                text = colorize_pinyin_sub(text, half_ruby_pattern)
        else:
            text = colorize_pinyin_sub(text, pinyin_pattern)

        colorized.append(text + sound_tags)

    return ' '.join(colorized)


def colorize_fuse(hanzi, pinyin, ruby=False):
    """Colorize hanzi based on pinyin tone.

    If ruby=True, then annotate hanzi with pinyin.
    """

    standard_fmt = '<span class="tone{tone}">{hanzi}</span>'
    ruby_fmt = '<span class="tone{tone}"><ruby>{hanzi}<rt>{pinyin}</rt></ruby></span>'

    hanzi = [h for h in cleanup(hanzi)]
    pinyin = sanitize_pinyin(pinyin)
    text = ''

    for h, p in zip(hanzi, pinyin):
        if ruby:
            text += ruby_fmt.format(tone=tone_number(p), hanzi=h, pinyin=p)
        else:
            text += standard_fmt.format(tone=tone_number(p), hanzi=h)

    return text


def local_dict_colorize(text, ruby=True):
    """Colorize text in the form: 你好[ni3 hao].

    As used in the local dictionaries.
    """

    def _sub(p):
        c = ''
        hanzi = p.group(1)
        pinyin = p.group(2)
        delimiter = '|'

        if hanzi.count(delimiter) == 1:
            hanzi = hanzi.split(delimiter)
            c += colorize_fuse(hanzi[0], pinyin, True)
            c += delimiter
            c += colorize_fuse(hanzi[1], pinyin, False)
        else:
            c += colorize_fuse(hanzi, pinyin, True)

        if not ruby:
            c += '[' + colorize(pinyin) + ']'

        return c

    text = sub(r'([\u3400-\u9fff|]+)\[(.*?)\]', _sub, text)
    return text


def sanitize_pinyin(pinyin, grouped=False):
    return ' '.join(
        accentuate(separate(cleanup(no_color(pinyin)), grouped))
    ).split()
