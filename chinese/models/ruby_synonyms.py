# -*- coding: utf-8 -*-
# 
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import string

import anki.stdmodels
from css import style

# List of fields
######################################################################

fields_list = ["Hanzi", "Meaning", "Hanzi2", "Hanzi3", "Hanzi4", 
               "Notes and pictures"]

# Card templates
######################################################################

recognition_front = string.Template(u'''\
{{#Hanzi$num}}
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div class=question>
<span class=chinese>{{ruby_bottom_text:Hanzi$num}}</span>
</div>

{{/Hanzi$num}}
''')

recall_front = string.Template(u'''
{{#Hanzi$num}}
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div class=question>
<div>{{Meaning}}</div>
<div class=chinese>{{hanzi_silhouette:Hanzi$num}}</div>
</div>

<div class=hint>{{hint_transcription:Hanzi$num}}</div>
<div class=context>{{hanzi_context:Hanzi$num}}</div>

{{#Notes and pictures}}
<div class=note>{{Notes and pictures}}</div>
{{/Notes and pictures}}

{{/Hanzi$num}}
''')

card_back = string.Template(u'''
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>
<div class=question>
<div class=meaning>{{Meaning}}</div>
<span class=chinese>
{{ruby:Hanzi$num}}</span>
</div>

<div class=chinese>
{{ruby:Hanzi}}
{{#Hanzi2}} / {{/Hanzi2}}{{ruby:Hanzi2}} 
{{#Hanzi3}} / {{/Hanzi3}}{{ruby:Hanzi3}} 
{{#Hanzi4}} / {{/Hanzi4}}{{ruby:Hanzi4}} 
</div>

{{#Notes and pictures}}
<div class=note>{{Notes and pictures}}</div>
{{/Notes and pictures}}
<!--{{sound:Hanzi$num}}-->
''')


# Add model for chinese word to Anki
######################################################################

def add_model_ruby_synonyms(col):
    mm = col.models
    m = mm.new("Chinese Ruby (+synonyms)")
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    for n in ["", "2", "3", "4"]:
        t = mm.newTemplate(u"Recognition"+n)
        t['qfmt'] = recognition_front.substitute(num=n)
        t['afmt'] = card_back.substitute(num=n)
        mm.addTemplate(m, t)
        t = mm.newTemplate(u"Recall"+n)
        t['qfmt'] = recall_front.substitute(num=n)
        t['afmt'] = card_back.substitute(num=n)
        mm.addTemplate(m, t)

    m['css'] += style
    m['addon'] = "Chinese Ruby"
    mm.add(m)
    # recognition card
    return m

anki.stdmodels.models.append(("Chinese Ruby (+synonyms)", add_model_ruby_synonyms))
