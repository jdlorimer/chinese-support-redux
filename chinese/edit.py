# -*- coding: utf-8 -*-
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
from anki.hooks import addHook

from .config import chinese_support_config as config
from .edit_behavior import update_fields


def updateFields(updated, note, index):
    if not config.toggleOn:
        return updated

    fieldsCopy = dict(note)
    fieldNames = mw.col.models.fieldNames(note.model())

    if 'addon' in note.model():
        modelType = note.model()['addon']
    else:
        modelType = None

    update_fields(fieldsCopy,
                  fieldNames[index],
                  note.model()['name'],
                  modelType)

    for f in fieldNames:
        if fieldsCopy[f] != note[f]:
            note[f] = fieldsCopy[f]
            updated = True

    return updated


def appendToneStyling(editor):
    js = 'var css = document.styleSheets[0];'

    for line in editor.note.model()['css'].split('\n'):
        if line.startswith('.tone'):
            js += 'css.insertRule("{}", css.cssRules.length);'.format(
                line.rstrip())

    editor.web.eval(js)


addHook('editFocusLost', updateFields)
addHook('loadNote', appendToneStyling)
