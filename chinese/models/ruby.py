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

fields_list = ["Hanzi",  "Meaning", "Notes and pictures"]

# Card templates
######################################################################

recognition_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>
<div class=question>
<span class=chinese>{{ruby_bottom_text:Hanzi}}</span>
</div>
'''

recall_front = u'''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div class=question>
<div {{Meaning}}</div>
<div class=chinese>{{hanzi_silhouette:Hanzi}}</div>
</div>

<div class=hint>{{hint_transcription:Hanzi}}</div>

{{#Notes and pictures}}
<div class=note>{{Notes and pictures}}</div>
{{/Notes and pictures}}
'''

card_back = u'''
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>
<div class=question>
<div class=meaning>{{Meaning}}</div>
<span class=chinese>
{{ruby:Hanzi}}</span>
</div>

{{#Notes and pictures}}
<div class=note>{{Notes and pictures}}</div>
{{/Notes and pictures}}

<!-- {{sound:Hanzi}} -->
'''

# Add model for chinese word to Anki
######################################################################

def add_model_ruby(col):
    mm = col.models
    m = mm.new("Chinese Ruby")
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
    m['addon'] = 'Chinese Ruby'
    mm.add(m)
    # recognition card
    return m

anki.stdmodels.models.append(("Chinese Ruby", add_model_ruby))
