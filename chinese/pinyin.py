# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# Large portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
# and
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import sys
import os
from anki.utils import stripHTML
from anki.db import *


hanzi_fields = ['Chinese', 'Mandarin', 'Hanzi', u'汉字', u'漢字', 'Expression']
ruby_fields = ['Reading', 'Ruby', 'Pinyin']
tones_fields = ['Tones']


model_name = 'chinese'

#type = "cantonese"
type = "mandarin"

tone_classes =  {
    1 : 'tone1', 2 : 'tone2', 3 : 'tone3', 4 : 'tone4', 5 : 'tone5'
    }



def is_han_character(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        # The code from the JapaneseSupport plugin compares
        # ord(character) to a number. We compare one character with
        # another. Don't know which method is 'better'. (And we skip
        # u'\u2e00' to u'\u4dff', i guess the kana are somwhere in
        # there.)
        return True
    return False


class UnihanController(object):
    """Class to get pinyin for a character.

    These are some remnants of the unihan reading extractor from
    Damien Elmes' chinese plugin.
    """
    
    def __init__(self, target):
        if sys.platform.startswith("win32"):
           base = unicode(os.path.dirname(os.path.abspath(__file__)),
                          "mbcs")
        else:
           base = os.path.dirname(os.path.abspath(__file__))
        self.db = DB(os.path.abspath(os.path.join(base, "unihan.db")))
        self.type = target

    def reading(self, hanzi):
        """Get pinyin for a single character"""
        n = ord(hanzi)
        return self.db.execute("select %s from unihan where id = :id"
                               % self.type, id=n)


class Pinyinizer(object):
    
    def __init__(self):
        self.unihan = UnihanController(type)


    def get_pinyin_data(self, hanzi):
        # There are fifty ways to^H^H for this to blow up.

        pinyin = self.unihan.reading(hanzi)
        for p in pinyin:
            print 'pinyin: ', p
        tone_number = self._tone_number(pinyin)
        # Carfully craft the ruby format string so the build-in
        # furigana &c. templates can parse this and the colorization
        # can still work. The space between the outer span and the
        # hanzi is important.
        #                   ... that one ->|<- ...
        ruby = u'<span class="ruby {tone}"> {hanzi}'\
            '[<span class="pinyin {tone}">{pinyin}</span>]'\
            '</span>'\
            .format(hanzi=hanzi, tone=tone_classes[tone_number], pinyin=pinyin)
        return pinyin, ruby, tone_number

    def _tone_number(self, pinyin):
        # Another fifty ways to blow up.
        return int(pinyin[-1:])


pinyinize = Pinyinizer()

# Focus lost hook
##########################################################################

def on_focus_lost(flag, n, fidx):
    from aqt import mw
    hanzi_field = None
    ruby_field = None
    tones_field = None
    # japanese model?
    if model_name not in n.model()['name'].lower():
        return flag
    # Look for hanzi, ruby and tone fields.
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in hanzi_fields:
            if name == f:
                hanzi_field = f
                hanzi_index = c
        for f in ruby_fields:
            if name == f:
                ruby_field = f
        for f in tones_fields:
            if name == f:
                tones_field = f
    # We really want hanzi and ruby fields. (It’s OK if we have no
    # tones field.)
    if not hanzi_field or not ruby_field:
        return flag
    # ruby field already filled?
    if n[ruby_field]:
        return flag
    # event coming from hanzi field?
    if fidx != hanzi_index:
        return flag
    # grab hanzi
    hanzi = mw.col.media.strip(n[hanzi_field])
    if not hanzi:
        return flag
    # update field
    ruby = u''
    tones = u''
    for h in hanzi:
        r = h
        t = u' '
        if is_han_character(h):
            try:
                p, r, t = pinyinize.get_pinyin_data(h)
                t = unicode(t)
            except:
                pass
        ruby += r
        tones += t
    n[ruby_field] = ruby
    # Check if we have a tones field
    if tones_field:
        # But clobber what is alread there
        n[tones_field] = tones
    return True



