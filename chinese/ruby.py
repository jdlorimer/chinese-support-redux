# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import sub

from .util import no_sound


def ruby_top(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\2 ', no_sound(text))


def ruby_bottom(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\1 ', no_sound(text))
