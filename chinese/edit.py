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
from anki.hooks import addHook, wrap
from aqt.editor import Editor, _html
from aqt.utils  import getBase
import anki.js

import Chinese_support
import edit_ui
import edit_behavior

# Focus lost hook
##########################################################################

def on_focus_lost(flag, fields_data, focus_field):
    if not edit_ui.enable: #the edit_ui "update fields" push-button is off
        return flag

    field_names = mw.col.models.fieldNames(fields_data.model())
    updated_field = field_names[focus_field]
    efields = dict(fields_data) #user-edited fields
    try:
        model_type = fields_data.model()['addon']
    except:
        model_type = ""
    model_name = fields_data.model()['name']

    edit_behavior.update_fields(efields, updated_field, model_name, model_type)

    for k in field_names:
        if efields[k] <> fields_data[k]:
            fields_data[k] = efields[k]
            flag = True
    
#    if flag:
#        print "Left field ", updated_field, "(polluted)", efields[updated_field]
#    else:
#        print "Left field ", updated_field, "(clean)", efields[updated_field]

    return flag

def colorize_notes(self, note, hide=True, focus=False):
    css_colors = ""
    if note:
        for l in note.model()["css"].split("\n"):
            if l.startswith(".tone"):
                css_colors += l+"\n"
        myHtml = _html % (
            getBase(self.mw.col), anki.js.jquery,
            _("Show Duplicates"))
        myHtml = myHtml.replace("<style>", "<style\n>"+css_colors)
        self.web.setHtml(myHtml, loadCB=self._loadFinished)


addHook('editFocusLost', on_focus_lost)

Editor.setNote = wrap(Editor.setNote, colorize_notes)
