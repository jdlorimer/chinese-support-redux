# -*- coding: utf-8 -*-
# 
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Standard Chinese model.
#

import anki.stdmodels

def addChineseModel(col):
    mm = col.models
    m = mm.new(_("Chinese"))
    fm = mm.newField(_("Hanzi"))
    mm.addField(m, fm)
    fm = mm.newField(_("Meaning"))
    mm.addField(m, fm)
    fm = mm.newField(_("Ruby"))
    mm.addField(m, fm)
    fm = mm.newField(_("Tones"))
    mm.addField(m, fm)
    t = mm.newTemplate(_("Recognition"))
    t['qfmt'] = "<div class=chinese>{{Hanzi}}</div>"
    t['afmt'] = """{{FrontSide}}<hr id=answer>\
<div class=chinese>{{furigana:Ruby}}</div>\
<div>{{Meaning}}</div>"""
    mm.addTemplate(m, t)
    t = mm.newTemplate(_("Recall"))
    t['qfmt'] = "<div>{{Meaning}}</div>"
    t['afmt'] = """{{FrontSide}}<hr id=answer>\
<div class=chinese>{{furigana:Ruby}}</div>"""
    mm.addTemplate(m, t)
    # css
    m['css'] += u"""\
.chinese { font-size: 30px }
.win .chinese { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .chinese { font-family: "Hiragino Mincho Pro", "ヒラギノ明朝 Pro"; }
.linux .chinese { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .chinese { font-family: "Hiragino Mincho ProN"; }
.tone1 {color: red;}
.tone2 {color: orange;}
.tone3 {color: green;}
.tone4 {color: blue;}
.tone5 {color: black;}
"""
    # recognition card
    mm.add(m)
    return m

anki.stdmodels.models.append((_("Chinese"), addChineseModel))
