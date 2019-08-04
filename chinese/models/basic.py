# Copyright 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from .css import style

fields_list = ['Hanzi', 'Color', 'Pinyin', 'English', 'Sound']

recognition_front = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<span class=chinese>{{Hanzi}}</span>
'''

recall_front = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{English}}</div>
'''

card_back = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{English}}</div>
<div class=reading>{{Pinyin}}</div>
<div class=chinese>{{Color}}</div>
<!-- {{Sound}}-->
'''


def add_model(col):
    mm = col.models
    m = mm.new('Chinese (Basic)')
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate('Recall')
    t['qfmt'] = recall_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)
    m['css'] += style
    m['addon'] = 'Chinese (Basic)'
    mm.add(m)
    return m
