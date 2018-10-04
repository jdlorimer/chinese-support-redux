# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from re import sub


def no_hidden(text):
    return sub(r'<!--.*?-->', '', text)


def no_sound(text):
    '''
    Removes the [sound:xxx.mp3] tag that's added by Anki when you record
    sound into a field.

    If you don't remove it before taking data from one field to another,
    it will likely be duplicated, and the sound will play twice.
    '''
    return sub(r'\[sound:.*?]', '', text)


def ruby_top(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\2 ', no_sound(text))


def ruby_bottom(text):
    return sub(r' ?([^ >]+?)\[(.+?)\]', r'\1 ', no_sound(text))
