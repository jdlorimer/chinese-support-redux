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

from re import search, split, sub

from jieba import cut

from .main import dictionary


def silhouette(hanzi):
    """Replaces each Chinese character by a blank space."""

    def insert_spaces(p):
        r = ''
        for i in p.group(0):
            r += i + ' '
        return r[:-1]

    hanzi = sub(r'[\u3400-\u9fff]+', insert_spaces, hanzi)
    return sub(r'[\u3400-\u9fff]', '_', hanzi)


def simplify(text):
    return dictionary.get_simplified(text)


def traditional(text):
    return dictionary.get_traditional(text)


def has_hanzi(text):
    return search(r'[\u3400-\u9fff]', text)


def separate_chars(chars, grouped=True):
    assert isinstance(chars, str)

    if not grouped:
        return list(filter(lambda s: s.strip(), chars))

    if len(chars.split()) > 1:
        separated = split('([ ,.，。])', chars)
        return list(filter(lambda s: s.strip(), separated))

    return list(cut(chars))
