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

import re
import json

import anki.buildinfo
from anki.hooks import addHook
from aqt.utils import showWarning
from aqt import mw
from aqt.editor import Editor

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


TONE_CSS_RULE = re.compile("(\\.tone\\d) *\\{([^}]*)\\}")

# append_tone_styling(editor: Editor)
#
# Extracts the CSS rules for tones (i.e. matching TONE_CSS_RULE) from the 
# user defined CSS style sheet. For the sake of simplicity, a tone CSS rule
# must be a one liner.
#
# IMPLEMENTATION NOTES:
#
# The code makes heavily use of internal APIs in Anki that may change in
# future releases. Hopefully, these notes are useful to adapt the code to
# new releases in case of breaking.
#
# The solution is based on Anki 2.1.54.
#
# The Javascript code being evaluated in the QWebView executes the following steps:
#   1. Wait until the UI has been loaded. The code for that is based on [1].
#   2. Loop through all RichTextInput Svelte component instances. They are
#      reachable via "require" because they have been registered before here [2].
#      Unfortunately, this method is only available since 2.1.54.
#   3. Using the RichTextInputAPI [3], we can query the associated CustomStyles
#      instance. A CustomStyles instance has a `styleMap` [4] that contains an 
#      "userBase" entry, which wraps a <style> HTML element. This style element's
#      intended function is to apply color, font family, font size, etc. [5,6].
#      It is the perfect place to add our own CSS tone rules.
#
# [1] https://github.com/ankitects/anki/blob/2.1.54/qt/aqt/editor.py#L184
# [2] https://github.com/ankitects/anki/blob/2.1.54/ts/editor/rich-text-input/RichTextInput.svelte#L40
# [3] https://github.com/ankitects/anki/blob/2.1.54/ts/editor/rich-text-input/RichTextInput.svelte#L21
# [4] https://github.com/ankitects/anki/blob/2.1.54/ts/editor/rich-text-input/CustomStyles.svelte#L37
# [5] https://github.com/ankitects/anki/blob/2.1.54/ts/editor/rich-text-input/RichTextStyles.svelte#L17
# [6] https://github.com/ankitects/anki/blob/2.1.54/ts/editor/rich-text-input/RichTextStyles.svelte#L33

def append_tone_styling_anki2_1_54(editor: Editor):
    rules = []
    for line in editor.note.note_type()['css'].split('\n'):
        if '.tone' in line:
            m = TONE_CSS_RULE.search(line)
            if m:
                rules.append(line)
            else:
                showWarning("WARN: could not parse CSS tone rule. "
                            "Currently, tone CSS rules need to be one liners.")

    js = f"var CSSRULES = {json.dumps(rules)};"
    js += """
    require("anki/ui").loaded.then(() => 
      require("anki/RichTextInput").instances.forEach(inst =>
        inst.customStyles.then(styles => {
          var sheet = styles.styleMap.get("userBase").element.sheet;
          CSSRULES.forEach(rule =>
            sheet.insertRule(rule)
          );
        })
      )
    );
    """
    editor.web.eval(js)

def append_tone_styling_anki2_1_49(editor):
    rules = []
    for line in editor.note.note_type()['css'].split('\n'):
        if line.startswith('.tone'):
            m = TONE_CSS_RULE.search(line)
            if m:
                rules.append((m.group(1), m.group(2)))
            else:
                showWarning("WARN: could not parse CSS tone rule. "
                            "Currently, tone CSS rules need to be one liners.")

    inner_js = ""
    for rulename, ruledef in rules:
        for part in ruledef.split(';'):
            if ':' in part:
                [property, value] = part.split(':', 1)
                inner_js += f"jQuery('{rulename.strip()}', this.shadowRoot).css('{property.strip()}', '{value.strip()}');\n"
    js = "jQuery('div.field').each(function () {\n%s})" % inner_js

    editor.web.eval(js)


__version = [int(x) for x in anki.buildinfo.version.split('.')]
if __version < [2,1,50]:
    append_tone_styling = append_tone_styling_anki2_1_49
elif __version >= [2,1,54]:
    append_tone_styling = append_tone_styling_anki2_1_54
else:
    showWarning("Chinese tone styling has not been implemented for your current Anki version. "
                "Supported versions are Anki 2.1.49 as well as 2.1.54 and later.")
    def append_tone_styling(editor):
        pass