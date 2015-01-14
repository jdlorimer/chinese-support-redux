# -*- coding: utf-8 -*-
# 
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import anki.stdmodels
from css import style

# List of fields
######################################################################

fields_list = ["Hanzi",  "Meaning", "Reading", "Color", "Sound"]

# Card templates
######################################################################

recognition_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<span class=chinese>{{Hanzi}}</span>
'''

recall_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{Meaning}}</div>
'''

card_back = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{Meaning}}</div>
<div class=reading>{{Reading}}</div>
<div class=chinese>{{Color}}</div>
<!-- {{Sound}}-->
'''


# Add model for chinese word to Anki
######################################################################

def add_model_simp(col):
    mm = col.models
    m = mm.new("Chinese (basic)")
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
#    t = mm.newTemplate(u"Recognition")
#    t['qfmt'] = recognition_front
#    t['afmt'] = card_back
#    mm.addTemplate(m, t)
    t = mm.newTemplate(u"Recall")
    t['qfmt'] = recall_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)

    m['css'] += style
    m['addon'] = 'Chinese (basic)'
    mm.add(m)
    # recognition card
    return m

anki.stdmodels.models.append(("Chinese (basic)", add_model_simp))
