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

from re import search, sub

from .bopomofo import bopomofo
from .consts import hanzi_regex
from .hanzi import has_hanzi
from .main import config, dictionary
from .util import hide, no_color


def ruby(words, transcription=None):
    """Convert hanzi to ruby notation.

    For use with {{Ruby:fieldname}} on the card template.

    If not specified, use the transcription type set in the menubar.
    """

    from .transcribe import get_char_transcription, replace_tone_marks

    if not transcription:
        transcription = config['transcription']

    assert isinstance(words, list)

    rubified = []
    for text in words:
        text = sub(r'[［【]', '[', text)
        text = sub(r'[］】]', ']', text)

        def insert_multiple_pinyin_sub(p):
            hanzi = p.group(1)
            t = dictionary.get_pinyin(hanzi)
            if not t:
                return p.group()
            t = t.split(' ')
            s = ''
            hanzi = p.group(1)
            while hanzi:
                if transcription == 'Pinyin':
                    s += hanzi[0] + '[' + t.pop(0) + ']'
                elif transcription == 'Bopomofo':
                    s += hanzi[0] + '['
                    s += bopomofo(replace_tone_marks([t.pop(0)]))[0] + ']'
                hanzi = hanzi[1:]
            return s + p.group(2)

        def insert_pinyin_sub(p):
            t = get_char_transcription(p.group(1), transcription)
            return p.group(1) + '[' + t + ']' + p.group(2)

        text += '%'
        if transcription in ['Pinyin', 'Bopomofo']:
            text = sub(
                r'(%s+)([^[])' % hanzi_regex, insert_multiple_pinyin_sub, text
            )
        text = sub(r'(%s)([^[])' % hanzi_regex, insert_pinyin_sub, text)
        text = sub(r'(%s)([^[])' % hanzi_regex, insert_pinyin_sub, text)
        text = text[:-1]
        rubified.append(text)

    return rubified


def has_ruby(text):
    return search(r'%s\[.+\]' % hanzi_regex, text)


def hide_ruby(text):
    """Append hidden hanzi and toneless pinyin to a ruby string,
    to make a note searchable in the card browser.
    """
    from .transcribe import no_tone

    t = no_tone(ruby_top(text))
    t += no_color(ruby_bottom(text)).replace(' ', '')
    return hide(text, t)


def ruby_top(text):
    if not has_ruby(text):
        if not has_hanzi(text):
            return text
        return ''
    return sub('(%s+)\\[([^\\]]+)\\]' % hanzi_regex, r'\2 ', text).rstrip()


def ruby_bottom(text):
    if not has_ruby(text):
        if has_hanzi(text):
            return text
        return ''
    return sub('(%s+)\\[([^\\]]+)\\]' % hanzi_regex, r'\1 ', text).rstrip()


def separate_ruby(text):
    assert isinstance(text, list)
    return [
        (ruby_bottom(word).replace(' ', ''), ruby_top(word).replace(' ', ''))
        for word in text
    ]
