# -*- coding: utf-8 -*-
# Copyright 2013 Thomas TEMPE <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki.hooks import addHook

from .config import chinese_support_config as config


def setupToggleButton(buttons, editor):
    config.toggleOn = False

    editor._links['chineseSupport'] = onClick

    toggleButton = editor._addButton(
        icon=None,
        cmd='chineseSupport',
        tip='Chinese Support',
        label='<b>汉字</b>',
        id='chineseSupport',
        toggleable=True)

    return buttons + [toggleButton]


def updateToggleButton(editor):
    enabled = editor.note.model()['id'] in config.options['enabledModels']

    if (enabled and not config.toggleOn) or (not enabled and config.toggleOn):
        editor.web.eval('toggleEditorButton(chineseSupport);')
        onClick(editor)


def onClick(editor):
    config.toggleOn = not config.toggleOn

    mid = str(editor.note.model()['id'])

    if config.toggleOn and mid not in config.options['enabledModels']:
        config.options['enabledModels'].append(mid)
    elif not config.toggleOn and mid in config.options['enabledModels']:
        config.options['enabledModels'].remove(mid)

    config.save()


addHook('setupEditorButtons', setupToggleButton)
addHook('loadNote', updateToggleButton)
