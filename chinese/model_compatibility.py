# -*- coding: utf-8 -*-
# 
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import anki.stdmodels

# List of fields
######################################################################

fields_list = ["Hanzi",  "Meaning", "Pinyin", "Color"]

# Card templates
######################################################################

recognition_front = u'''
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<span class=chinese>{{Hanzi}}</span>
'''

recognition_back = u'''
{{Front}}
{{Meaning}}
<div class=chinese>{{Pinyin}}<br>{{Color}}</div>
'''

recall_front = u'''
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

{{Meaning}}
<span class=chinese>{{hanzi_silhouette:Hanzi}}</span>
<div class=hint>{{hint_transcription:Hanzi}}</div>

'''

recall_back = u'''
{{Front}}
<div class=chinese>{{Pinyin}}<br>{{Color}}</div>
'''

# CSS styling
######################################################################

css_style = u'''
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.chinese { font-size: 30px }
.win .chinese { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .chinese { }
.linux .chinese { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .chinese { font-family: "Hiragino Mincho ProN"; }
.tags {color:gray;text-align:right;font-size:10pt;}
.hint {font-size:12pt;}
.tone1 {color: red;}
.tone2 {color: orange;}
.tone3 {color: green;}
.tone4 {color: blue;}
.tone5 {color: gray;}
'''

# Add model for chinese word to Anki
######################################################################

def add_model_ruby(col):
    mm = col.models
    m = mm.new("Chinese (compatibility)")
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate(u"Recognition")
    t['qfmt'] = recognition_front
    t['afmt'] = recognition_back
    mm.addTemplate(m, t)
    t = mm.newTemplate(u"Recall")
    t['qfmt'] = recall_front
    t['afmt'] = recall_back
    mm.addTemplate(m, t)

    m['css'] += css_style
    m['addon'] = 'Chinese (compatibility)'
    mm.add(m)
    # recognition card
    return m

anki.stdmodels.models.append(("Chinese (compatibility)", add_model_ruby))
