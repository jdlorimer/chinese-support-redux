# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2014 Alex Griffin <alex@alexjgriffin.com>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from .consts import bopomofo_replacements
from .util import cleanup


def bopomofo(pinyin):
    """Convert a pinyin string to Bopomofo.

    Optional tone info must be given as a number suffix, e.g.: 'ni3'.
    """

    pinyin = cleanup(pinyin).lower()
    for (a, b) in bopomofo_replacements:
        pinyin = pinyin.replace(a, b)

    return pinyin
