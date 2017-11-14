# -*- coding: utf-8 -*-
# Copyright 2012, 2013 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from anki.hooks import addHook
from aqt import mw

from .config import chinese_support_config as config
from .edit_behavior import updateFields


class EditManager:
    def __init__(self):
        addHook('setupEditorButtons', self.setupButton)
        addHook('loadNote', self.updateButton)
        addHook('editFocusLost', self.onFocusLost)

    def setupButton(self, buttons, editor):
        self.editor = editor
        self.buttonOn = False
        editor._links['chineseSupport'] = self.onToggle

        button = editor._addButton(
            icon=None,
            cmd='chineseSupport',
            tip='Chinese Support',
            label='<b>汉字</b>',
            id='chineseSupport',
            toggleable=True)

        return buttons + [button]

    def onToggle(self, editor):
        self.buttonOn = not self.buttonOn

        mid = str(editor.note.model()['id'])

        if self.buttonOn and mid not in config.options['enabledModels']:
            config.options['enabledModels'].append(mid)
        elif not self.buttonOn and mid in config.options['enabledModels']:
            config.options['enabledModels'].remove(mid)

        config.save()

    def updateButton(self, editor):
        enabled = (str(editor.note.model()['id']) in
                   config.options['enabledModels'])

        if (enabled and not self.buttonOn) or (not enabled and self.buttonOn):
            editor.web.eval('toggleEditorButton(chineseSupport);')
            self.buttonOn = not self.buttonOn

    def onFocusLost(self, _, note, index):
        if not self.buttonOn:
            return False

        allFields = mw.col.models.fieldNames(note.model())
        field = allFields[index]

        if updateFields(note, field, allFields):
            if index == len(allFields) - 1:
                self.editor.loadNote(focusTo=index)
            else:
                self.editor.loadNote(focusTo=index+1)

        return False


def appendToneStyling(editor):
    js = 'var css = document.styleSheets[0];'

    for line in editor.note.model()['css'].split('\n'):
        if line.startswith('.tone'):
            js += 'css.insertRule("{}", css.cssRules.length);'.format(
                line.rstrip())

    editor.web.eval(js)


addHook('loadNote', appendToneStyling)

EditManager()
