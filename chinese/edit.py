# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2012-2013 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
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

from aqt import mw, gui_hooks
from aqt.theme import theme_manager
from aqt.editor import Editor

from .behavior import update_fields
from .main import config


def webviewDidInit(web_content, context):
    if isinstance(context, Editor):            
        web_content.head += """<script>
        function chineseSupport_activateButton() {
            jQuery('#chineseSupport').addClass('active');
        }
        function chineseSupport_deactivateButton() {
            jQuery('#chineseSupport').removeClass('active');
        }
        </script>
        """

class EditManager:
    def __init__(self):
        gui_hooks.editor_did_init_buttons.append(self.setupButton)
        gui_hooks.editor_did_load_note.append(self.updateButton)
        gui_hooks.editor_did_unfocus_field.append(self.onFocusLost)
        gui_hooks.webview_will_set_content.append(webviewDidInit)
        self.editors = []

    def setupButton(self, buttons, editor):
        self.editors.append(editor)

        # setting toggleable=False because this is currently broken in Anki 2.1.49.
        # We implement our own toggleing mechanism here.
        button = editor.addButton(
            icon=None,
            cmd='chineseSupport',
            tip='Chinese Support',
            label='<b>汉字</b>',
            id='chineseSupport',
            toggleable=False)  
        if theme_manager.night_mode:
            btnclass = "btn-night"
        else:
            btnclass = "btn-day"
        # this svelte-9lxpor class is required and was found by looking at the DOM
        # for the other buttons in Anki 2.1.49. No idea how stable this class
        # name is, though.
        button = button.replace('class="', f'class="btn {btnclass} svelte-9lxpor ')

        return buttons + [button]

    def onToggle(self, editor):
        mid = str(editor.note.note_type()['id'])
        enabled = mid in config['enabledModels']

        enabled = not enabled
        if enabled:
            config['enabledModels'].append(mid)
            editor.web.eval("chineseSupport_activateButton()")
        else:
            config['enabledModels'].remove(mid)
            editor.web.eval("chineseSupport_deactivateButton()")

        config.save()

    def updateButton(self, editor):
        enabled = str(editor.note.note_type()['id']) in config['enabledModels']
        if enabled:
            editor.web.eval("chineseSupport_activateButton()")
        else:
            editor.web.eval("chineseSupport_deactivateButton()")

    def onFocusLost(self, _, note, index):
        enabled = str(note.note_type()['id']) in config['enabledModels']
        if not enabled:
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
