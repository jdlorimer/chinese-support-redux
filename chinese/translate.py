# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2018 Joseph Lorimer <joseph@lorimer.me>
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

from .color import colorize_dict
from .main import dictionary
from .util import cleanup


def translate_local(hanzi, lang):
    """Translate using local dictionary.

    lang is one of 'en', 'fr', 'de', 'es'.
    """

    defs = dictionary.get_definitions(hanzi, lang)

    if not defs:
        return ''

    def multiple_pinyins(defs):
        prev_p, _, _, _ = defs[0]
        for pinyin, _, _, _ in defs:
            if pinyin != prev_p:
                return True
        return False

    res = ''

    for pinyin, definition, _, _ in defs:
        if multiple_pinyins(defs):
            res += '❖ %s[%s] %s\n' % (hanzi, pinyin, definition)
        else:
            res += ' \t' + definition + '\n'

    return colorize_dict(res.replace('\n', '\n<br>'))


def translate(hanzi, lang):
    hanzi = cleanup(hanzi)

    if not hanzi or not lang:
        return ''

    return translate_local(hanzi, lang)
