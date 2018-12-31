# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012-2013 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <luoliyan@posteo.net>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

from anki.hooks import addHook
from aqt import mw

from .behavior import update_fields
from .main import config


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

        if self.buttonOn and mid not in config['enabledModels']:
            config['enabledModels'].append(mid)
        elif not self.buttonOn and mid in config['enabledModels']:
            config['enabledModels'].remove(mid)

        config.save()

    def updateButton(self, editor):
        enabled = str(editor.note.model()['id']) in config['enabledModels']

        if (enabled and not self.buttonOn) or (not enabled and self.buttonOn):
            editor.web.eval('toggleEditorButton(chineseSupport);')
            self.buttonOn = not self.buttonOn

    def onFocusLost(self, _, note, index):
        if not self.buttonOn:
            return False

        allFields = mw.col.models.fieldNames(note.model())
        field = allFields[index]

        if update_fields(note, field, allFields):
            if index == len(allFields) - 1:
                self.editor.loadNote(focusTo=index)
            else:
                self.editor.loadNote(focusTo=index+1)

        return False


def append_tone_styling(editor):
    js = 'var css = document.styleSheets[0];'

    for line in editor.note.model()['css'].split('\n'):
        if line.startswith('.tone'):
            js += 'css.insertRule("{}", css.cssRules.length);'.format(
                line.rstrip())

    editor.web.eval(js)
