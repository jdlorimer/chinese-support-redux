# Copyright 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from .css import style

fields_list = [
    'Hanzi',
    'Color',
    'Pinyin',
    'Bopomofo',
    'Ruby',
    'Ruby (Bopomofo)',
    'English',
    'Classifier',
    'Simplified',
    'Traditional',
    'Also Written',
    'Frequency',
    'Silhouette',
    'Sound',
]

recognition_front = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<span class=chinese>{{Hanzi}}</span>
'''

recall_front = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div>{{English}}</div>
<div>{{Silhouette}}</div>
<div class=hint>{{hint_transcription:Pinyin}}</div>
'''

card_back = '''\
<div class=tags>{{Deck}} {{#Tags}} -- {{/Tags}}{{Tags}}</div>

<div class=answer>
<div>{{English}}</div>
<div class=reading>{{Pinyin}}</div>
<div class=chinese>{{Color}}</div>
{{#Simplified}}<div class=chinese><span class=comment>Simplified:</span> {{Simplified}}</div>{{/Simplified}}
{{#Traditional}}<div class=chinese><span class=comment>Traditional:</span> {{Traditional}}</div>{{/Traditional}}
{{#Classifier}}<div class=chinese><span class=comment>Classifier:</span> {{Classifier}}</div>{{/Classifier}}
{{#Also Written}}<div class=chinese><span class=comment>Also written:</span> {{Also Written}}</div>{{/Also Written}}<!-- {{Sound}}-->
</div>

<div class=comment> <!-- Word lookup -->
<a href="http://www.mdbg.net/chindict/chindict.php?page=worddict&wdrst=0&wdqb={{text:Hanzi}}">MDBG</a>,
<a href="http://zhidao.baidu.com/q?word={{text:Hanzi}}&ct=17&pn=0&tn=ikaslist&rn=10&lm=0&fr=search">百度</a>,
<a href="http://image.baidu.com/i?ie=utf-8&word={{text:Hanzi}}">Image</a>
</div>
'''


def add_model(col):
    mm = col.models
    m = mm.new('Chinese (Advanced)')
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate('Recognition')
    t['qfmt'] = recognition_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)
    t = mm.newTemplate('Recall')
    t['qfmt'] = recall_front
    t['afmt'] = card_back
    mm.addTemplate(m, t)
    m['css'] += style
    m['addon'] = 'Chinese (Advanced)'
    mm.add(m)
    return m
