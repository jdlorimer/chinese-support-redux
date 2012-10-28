# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


import re

from aqt import mw
from anki.hooks import addHook

import Chinese_support
import pinyin
import translate


# Focus lost hook
##########################################################################

def on_focus_lost(flag, fields_data, focus_field):
    from aqt import mw
  
    field_names = mw.col.models.fieldNames(fields_data.model())
    focus_field_name = field_names[focus_field]

    print focus_field

    #Are we editing a Chinese-support-addon note?
    #If not, we'd better not modify anything automatically.
    try:
        if fields_data.model()['addon'] != Chinese_support.model_type_word:
            return flag
    except:
        return flag

    #did we just loose focus on a Hanzi field?
    def match_field_name(possible_name):
        return re.match(possible_name, focus_field_name, re.I)
    if not(filter(match_field_name, Chinese_support.possible_hanzi_field_names)):
        #We lost focus on a non-hanzi field.
        return flag

    #Recompute and update the hanzi field
    if len(fields_data[focus_field_name])>0:
        updated_hanzi_field = pinyin.update_hanzi_field(flag, fields_data, focus_field_name)
        if fields_data[focus_field_name] <> updated_hanzi_field:
            #Debugging: 
            #This should not be run if you exit an unmodified Hanzi field 
            print "Updating field from ", fields_data[focus_field_name]," to ", updated_hanzi_field
            fields_data[focus_field_name] = updated_hanzi_field
        else:
            return flag

    #Was this the first Hanzi field?
    for f in field_names:
        if filter(match_field_name, Chinese_support.possible_hanzi_field_names):
            if f == focus_field_name:
                #We're on the 1st Hanzi field. Continue
                break
            else:
                return True

    #Look fo the 'meaning' field
    meaning_field_name = None
    def match_meaning_field(possible_name):
        return re.match(possible_name, focus_field_name, re.I)
    for f in field_names:
        for m in Chinese_support.possible_meaning_field_names:
            if re.match(m, f):
                meaning_field_name = f
                break
        if meaning_field_name:
            break

    #Update 'meaning' field
    if meaning_field_name:
        #We found a "meaning" field, 
        if 0 == len(fields_data[focus_field_name]):
            #the Hanzi field is empty -> erase the meaning
            fields_data[meaning_field_name] = ""
        elif 0 == len(fields_data[meaning_field_name]):
            #the meaning is empty, but not the hanzi -> translate
            fields_data[meaning_field_name] = translate.translate(updated_hanzi_field)
    return True

addHook('editFocusLost', on_focus_lost)

