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

from re import IGNORECASE, search, sub

from .consts import (
    BOPOMOFO_REGEX,
    COLOR_RUBY_TEMPLATE,
    COLOR_TEMPLATE,
    HALF_RUBY_REGEX,
    HANZI_RANGE,
    JYUTPING_REGEX,
    PINYIN_REGEX,
    RUBY_REGEX,
)
from .hanzi import split_hanzi
from .sound import extract_tags
from .transcribe import tone_number, sanitize_transcript
from .util import align, is_punc, no_color


def colorize(words, target='pinyin', ruby_whole=False):
    from .ruby import has_ruby

    assert isinstance(words, list)

    def _repl(p):
        return COLOR_TEMPLATE.format(
            tone=tone_number(p.group(1)), chars=p.group()
        )

    done = []

    d = {
        'pinyin': PINYIN_REGEX,
        'pinyin_tw': PINYIN_REGEX,
        'jyutping': JYUTPING_REGEX,
        'bopomofo': BOPOMOFO_REGEX,
    }

    for word in words:
        (word, sound_tags) = extract_tags(no_color(word))

        if target in d:
            pattern = d[target]
            text = ''
            for syllable in word.split():
                if search(f'^{pattern}$', syllable):
                    text += sub(f'^{pattern}$', _repl, syllable, IGNORECASE)
                elif has_ruby(syllable):
                    if ruby_whole:
                        pattern = RUBY_REGEX
                    else:
                        pattern = HALF_RUBY_REGEX
                    text += sub(pattern, _repl, syllable, IGNORECASE)
                else:
                    text += f'<span class="tone5">{syllable}</span>'
        else:
            raise NotImplementedError(target)

        done.append(text + sound_tags)

    return ' '.join(done)


def colorize_dict(text):
    assert isinstance(text, str)

    def _sub(p):
        s = ''
        hanzi = p.group(1)
        pinyin = sanitize_transcript(p.group(2), 'pinyin', grouped=False)
        delim = '|'

        if hanzi.count(delim) == 1:
            hanzi = hanzi.split(delim)
            s += colorize_fuse(
                split_hanzi(hanzi[0], grouped=False), pinyin, True
            )
            s += delim
            s += colorize_fuse(
                split_hanzi(hanzi[1], grouped=False), pinyin, False
            )
        else:
            s += colorize_fuse(split_hanzi(hanzi, grouped=False), pinyin, True)

        return s

    return sub(r'([\%s|]+)\[(.*?)\]' % HANZI_RANGE, _sub, text)


def colorize_fuse(chars, trans, ruby=False):
    assert isinstance(chars, list)
    assert isinstance(trans, list)

    colorized = ''

    for c, t in align(chars, trans):
        if c is None or t is None:
            continue
        if is_punc(c) and is_punc(t):
            colorized += c
            continue
        if ruby:
            colorized += COLOR_RUBY_TEMPLATE.format(
                tone=tone_number(t), chars=c, trans=t
            )
        else:
            colorized += COLOR_TEMPLATE.format(tone=tone_number(t), chars=c)

    return colorized
