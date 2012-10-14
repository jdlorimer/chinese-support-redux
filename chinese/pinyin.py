# -*- coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
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


import os
import re
import json

from aqt import mw
import Chinese_support

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

vowel_decorations = [
{ },
{ u'a':u'ā', u'e':u'ē', u'i':u'ī', u'o':u'ō', u'u':u'ū', u'ü':u'ǖ', u'v':u'ǖ'},
{ u'a':u'á', u'e':u'é', u'i':u'í', u'o':u'ó', u'u':u'ú', u'ü':u'ǘ', u'v':u'ǘ'},
{ u'a':u'ǎ', u'e':u'ě', u'i':u'ǐ', u'o':u'ǒ', u'u':u'ǔ', u'ü':u'ǚ', u'v':u'ǚ'},
{ u'a':u'à', u'e':u'è', u'i':u'ì', u'o':u'ò', u'u':u'ù', u'ü':u'ǜ', u'v':u'ǜ'},
{ u'a':u'a', u'e':u'e', u'i':u'i', u'o':u'o', u'u':u'u', u'ü':u'ü', u'v':u'ü'},
]


def is_han_character(uchar):
    return uchar >= u'\u4e00' and uchar <= u'\u9fff'


class Pinyinizer(object):
    
    def __init__(self):
        # N.B. This assumes that type is either 'cantonese' or
        # 'mandarin'.
        readings_file_name = os.path.join(mw.pm.addonFolder(), 'chinese', 'dictionaries', Chinese_support.language + '_readings.json')
        self.readings = json.load(open(readings_file_name))
            
    def get_pinyin(self, hanzi):
        #Return all pinyin readings, separated by spaces
        return self.readings[hanzi]

    def get_tone_number(self, pinyin):
        """Return a string containing a tone number.

        Return a tone number, depending on the language, either derived
        from the end of the pinyin string or determined
        depending on the first "decorated" vowel we find.

        """
        if re.match(r".*[0－9]$", pinyin[-1:]):
            return int(pinyin[-1:])
        else:
            for c in pinyin:
                try:
                    return vowel_tone_dict[c]
                except KeyError:
                    continue
            return 5
                
pinyinize = Pinyinizer()


# Decorate Pinyin with accent on vowel, if Mandarin
##########################################################################

def decorate_pinyin(pinyin):
    if not 'mandarin'== Chinese_support.language:
        #Tone marking is only applicable for mandarin pinyin, not for other transcriptions
        return pinyin
    if re.match("\s*[a-z]*[aeiouüÜv][a-z]*[1-5]$", pinyin, flags=re.IGNORECASE):
        #We have something that looks like pinyin, with a tone number at the end
        tone=pinyin[-1:]
        pinyin=pinyin[:-1]
        #Decorate the 1st vowel we find
        for v in u"aeiouüvAEIOUÜV":
            if pinyin.find(v)>-1:
            #We have found a vowel
                try:
                    pinyin=re.sub(v, vowel_decorations[int(tone)][v.lower()], pinyin, count=1)
                    break
                except KeyError, IndexError:
                    pass
    else:
        pinyin = re.sub(r'[vV]', 'ü', pinyin, count=1)
    return pinyin


# Update Hanzi field to Ruby format after it has been modified
##########################################################################

def update_hanzi_field(flag, fields_data, hanzi_field):
    """Re-compute the Hanzi field value after update
    
    Add ruby annotation like 你[nǐ] to each Chinese character that does not have one already.
    Don't update existing ruby annotations, as the user may have modified them intentionally.
    
    Erase and re-insert tone number information in HTML data for colorization.
    """

    hanzi_string = fields_data[hanzi_field]
        
    #Strip former HTML tone marking
    hanzi_string = re.sub(r'<span class="tone[0-9]">(.*?)</span>', r'\1', hanzi_string)
    hanzi_string = re.sub(r'&nbsp;', '', hanzi_string)

    #Replace Chinese typography with its ASCII counterpart
    hanzi_string = re.sub(u'［', u'[', hanzi_string)
    hanzi_string = re.sub(u'］', u']', hanzi_string)
    
    #insert [pinyin] after each chinese character not followed by a '['
    #In case there are multiple pinyin transcriptions, give them all to let the user decide
    def insert_pinyin_sub(p):
            return p.group(1)+'['+pinyinize.get_pinyin(p.group(1))+']'+p.group(2)
    hanzi_string = re.sub(u'([\u4e00-\u9fff])(\[sound:)', r'\1 \2', hanzi_string)
    hanzi_string = re.sub(u'([\u4e00-\u9fff])([^[])', insert_pinyin_sub, hanzi_string+' ')[:-1]
    hanzi_string = re.sub(u'([\u4e00-\u9fff])([^[])', insert_pinyin_sub, hanzi_string+' ')[:-1]

    # Replace pinyin in the format "[ma2]" with "[má]", if we're in mandarin mode.
    # Handle multiple pinyin gracefully, eg : "到[dao3 dao4]"
    def decorate_pinyin_sub(p):
        r = p.group(1)+decorate_pinyin(p.group(2))
        for i in re.split(r"\s+", p.group(3)):
            if i:
                r += " " + decorate_pinyin(i)
        return r+']'
    if "mandarin" == Chinese_support.language:
        hanzi_string = re.sub(u'([\u4e00-\u9fff]\[)\s*([a-zɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ]+[0-9]?)((\s+[a-zɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ]+[0-9]?)*)\s*\]', decorate_pinyin_sub, hanzi_string, flags=re.IGNORECASE)

    # Detect each occurence of something like "吗[mǎ]" or "吗[ma3]"， and add HTML tone info.
    # Use only the first pinyin transcription, in case there are more than one.
    def add_color_to_pinyin_sub(p):
        return u'<span class="tone{t}">{r}</span>'.format(t=pinyinize.get_tone_number(p.group(2)), r=p.group())

    hanzi_string = re.sub(u'([\u4e00-\u9fff]\[\s*)([a-zɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ]+[0-9]?)([^]]*\])', add_color_to_pinyin_sub, hanzi_string, flags=re.IGNORECASE)

    #Return new string
    return hanzi_string
