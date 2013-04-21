# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>, Thomas TEMPE <thomas.tempe@alysse.org>
# Copyright 2012, Thomas TEMPE <thomas.tempe@alysse.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.


# This module interprets ruby annotations and converts them into HTML.
# 
# Ruby annotations are small annotations written above a chinese or
# kanji character, and are typically used for representing its
# pronounciation.
# 
# With This module assumes the corresponding field is written as
# a[hello], where "hello" is the ruby annotation for the letter "a".

import re
from anki.hooks import addHook
from anki.utils import stripHTML

r = r' ?([^ >]+?)\[(.+?)\]'
s = r'\[sound:.*?\]'
ruby_re = r'<ruby><rb>\1</rb><rt>\2</rt></ruby>'
html_comments_re = r'<!--.*?-->'

def no_comments(txt):
    #Remove HTML comments.
    return re.sub(html_comments_re, '', txt)

def no_sound(txt):
    return re.sub(s, "", txt)

def ruby(txt, *args):
    return re.sub(r, ruby_re, no_sound(txt))

def ruby_top(txt, *args):
    return re.sub(r, r'\2 ', no_sound(txt))

def ruby_bottom(txt, *args):
    return re.sub(r, r'\1', no_sound(txt))

def ruby_top_text(txt, *args):
    return stripHTML(re.sub(r, r'\2 ', no_sound(no_comments(txt))))

def ruby_bottom_text(txt, *args):
    return stripHTML(re.sub(r, r'\1', no_sound(no_comments(txt))))

def sound(txt, *args):
    return re.sub(r'(\[sound:.+?\])', r'\1', txt)

def install():
    addHook('fmod_ruby', ruby)
    addHook('fmod_ruby_top', ruby_top)
    addHook('fmod_ruby_bottom', ruby_bottom)
    addHook('fmod_ruby_top_text', ruby_top_text)
    addHook('fmod_ruby_bottom_text', ruby_bottom_text) 
