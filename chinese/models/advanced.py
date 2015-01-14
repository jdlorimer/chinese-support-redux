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

fields_list = ["Hanzi",  "Meaning", "Reading", "Color", "Mean Word", "Sound", "Simplified", "Traditional", "Also Written", "Ruby", "Silhouette"]

# Card templates
######################################################################

recognition_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<span class=chinese>{{Hanzi}}</span>
'''

recall_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{Meaning}}</div>
<div>{{Silhouette}}</div>
<div class=hint>{{hint_transcription:Reading}}</div>
'''

card_back = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div class=answer>
<div>{{Meaning}}</div>
<div class=reading>{{Reading}}</div>
<div class=chinese>{{Color}}</div>
{{#Simplified}}<div class=chinese><span class=comment>Simplified:</span> {{Simplified}}</div>{{/Simplified}}
{{#Traditional}}<div class=chinese><span class=comment>Traditional:</span> {{Traditional}}</div>{{/Traditional}}
{{#Mean Word}}<div class=chinese><span class=comment>Mean Word:</span> {{Mean Word}}</div>{{/Mean Word}}
{{#Also Written}}<div class=chinese><span class=comment>Also written:</span> {{Also Written}}</div>{{/Also Written}}<!-- {{Sound}}-->
</div>

<div class=comment> <!-- Word lookup -->
<a href="http://www.mdbg.net/chindict/chindict.php?page=worddict&wdrst=0&wdqb={{text:Hanzi}}">MDBG</a>, 
<a href="http://zhidao.baidu.com/q?word={{text:Hanzi}}&ct=17&pn=0&tn=ikaslist&rn=10&lm=0&fr=search">百度</a>,
<a href="http://image.baidu.com/i?ie=utf-8&word={{text:Hanzi}}">Image</a>
</div>
'''


# Add model for chinese word to Anki
######################################################################

def add_model(col):
    mm = col.models
    m = mm.new("Chinese (advanced)")
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate(u"Recognition")
    t['qfmt'] = recognition_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)
    t = mm.newTemplate(u"Recall")
    t['qfmt'] = recall_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)

    m['css'] += style
    m['addon'] = 'Chinese (advanced)'
    mm.add(m)
    # recognition card
    return m

anki.stdmodels.models.append(("Chinese (advanced)", add_model))
