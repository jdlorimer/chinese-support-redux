# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# Portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
# as part of the Japanese addon.
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# The data in the two .json files are derived from Unihan.zip data:
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


import sys
import os
import json
from aqt import mw



hanzi_fields = ['Chinese', 'Mandarin', 'Hanzi', u'汉字', u'漢字', 'Expression']
ruby_fields = ['Reading', 'Ruby', 'Pinyin']
tones_fields = ['Tones']



model_name = 'chinese'

# type = "cantonese"
type = "mandarin"

tone_classes =  {
    1 : 'tone1', 2 : 'tone2', 3 : 'tone3', 4 : 'tone4', 5 : 'tone5',
    # You will have to define your own colors and meanings for the
    # extra 'tones'.
    6: 'tone6', 7: 'tone7',    8: 'tone8', 9: 'tone9'
    }


# To get the tone numbers from mandarin readings. Values taken from
# wikipedia. Not in this dict is taken as tone 5.
vowel_tone_dict = {
    u'ā':1, u'ā':1, u'ɑ̄':1, u'ē':1, u'ī':1, u'ō':1, u'ū':1,
    u'ǖ':1, u'Ā':1, u'Ē':1, u'Ī':1, u'Ō':1, u'Ū':1, u'Ǖ':1,
    u'á':2, u'ɑ́':2, u'é':2, u'í':2, u'ó':2, u'ú':2, u'ǘ':2,
    u'Á':2, u'É':2, u'Í':2, u'Ó':2, u'Ú':2, u'Ǘ':2,
    u'ǎ':3, u'ɑ̌':3, u'ě':3, u'ǐ':3, u'ǒ':3, u'ǔ':3, u'ǚ':3,
    u'Ǎ':3, u'Ě':3, u'Ǐ':3, u'Ǒ':3, u'Ǔ':3, u'Ǚ':3,
    u'à':4, u'ɑ̀':4, u'è':4, u'ì':4, u'ò':4, u'ù':4, u'ǜ':4,
    u'À':4, u'È':4, u'Ì':4, u'Ò':4, u'Ù':4, u'Ǜ':4
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



class Pinyinizer(object):
    
    def __init__(self):
        # N.B. This assumes that type is either 'cantonese' or
        # 'mandarin'.
        readings_file_name = os.path.join(mw.pm.addonFolder(), 'chinese',
                                          type + '_readings.json')
        self.readings = json.load(open(readings_file_name))
            

    def get_pinyin_data(self, hanzi):
        # This may throw a KeyError
        pinyin = self.readings[hanzi]
        # Ignore all put the first reading
        pinyin = pinyin.split(' ')[0]
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
        if type == 'cantonese':
        # Another fifty ways to blow up.
            return int(pinyin[-1:])
        else:
            for c in pinyin:
                try:
                    return vowel_tone_dict[c]
                except KeyError:
                    continue
            return 5
                


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



