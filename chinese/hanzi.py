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

from re import search, split, sub

from jieba import cut

from .consts import HANZI_RANGE
from .main import config, dictionary
from .util import cleanup, get_first


def get_silhouette(hanzi):
    def insert_spaces(p):
        r = ''
        for i in p.group(0):
            r += i + ' '
        return r[:-1]

    hanzi = sub(f'[{HANZI_RANGE}]+', insert_spaces, hanzi)
    return sub(f'[{HANZI_RANGE}]', '_', hanzi)


def get_simp(text):
    return dictionary.get_simplified(text)


def get_trad(text):
    return dictionary.get_traditional(text)


def has_hanzi(text):
    return search(f'[{HANZI_RANGE}]', text)


def get_hanzi(note):
    return cleanup(get_first(config['fields']['hanzi'], note))


def split_hanzi(hanzi, grouped=True):
    assert isinstance(hanzi, str)

    if len(hanzi.split()) > 1:
        separated = remove_empty(split('([ ,.，。])', hanzi))
    else:
        separated = list(cut(hanzi))

    if grouped:
        return separated

    return flatten(separated)


def remove_empty(a):
    return list(filter(lambda s: s.strip(), a))


def flatten(hanzi):
    assert isinstance(hanzi, list)

    a = []
    for s in hanzi:
        if list(filter(has_hanzi, s)):
            a.extend(list(s))
        else:
            a.append(s)
    return a
