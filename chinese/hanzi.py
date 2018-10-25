# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import search, sub

from .main import dictionary


def silhouette(hanzi):
    """Replaces each Chinese character by a blank space.

    Eg: 以A为B -> _A_B
    Eg: 哈密瓜 -> _ _ _
    """
    def insert_spaces(p):
        r = ""
        for i in p.group(0):
            r += i + " "
        return r[:-1]

    hanzi = sub("[\u3400-\u9fff]+", insert_spaces, hanzi)
    txt = sub("[\u3400-\u9fff]", "_", hanzi)
    return txt


def simplify(text):
    return dictionary.get_simplified(text)


def traditional(text):
    return dictionary.get_traditional(text)


def has_hanzi(text):
    return search(r'[\u3400-\u9fff]', text)
