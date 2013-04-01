# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#COPYRIGHT AND PERMISSION NOTICE

#Copyright © 1991-2012 Unicode, Inc. All rights reserved. Distributed under the Terms of Use in http://www.unicode.org/copyright.html.

#Permission is hereby granted, free of charge, to any person obtaining a copy of the Unicode data files and any associated documentation (the "Data Files") or Unicode software and any associated documentation (the "Software") to deal in the Data Files or Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, and/or sell copies of the Data Files or Software, and to permit persons to whom the Data Files or Software are furnished to do so, provided that (a) the above copyright notice(s) and this permission notice appear with all copies of the Data Files or Software, (b) both the above copyright notice(s) and this permission notice appear in associated documentation, and (c) there is clear notice in each modified Data File or in the Software as well as in the documentation associated with the Data File(s) or Software that the data or software has been modified.

#THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA FILES OR SOFTWARE.

#Except as contained in this notice, the name of a copyright holder shall not be used in advertising or otherwise to promote the sale, use or other dealings in these Data Files or Software without prior written authorization of the copyright holder.


from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, openLink, askUser
import aqt.addons 
from anki.hooks import wrap

from config import chinese_support_config
import __init__
import translate
import Chinese_support
import edit_behavior
from upgrade import edit_behavior_file

ui_actions = {}
dictionaries = [ 
("None", _("None")), 
("CEDICT", _("English")), 
("HanDeDict", _("German")),
("CFDICT", _("French"))]

transcriptions = [
    "Pinyin", "WadeGiles", "CantoneseYale", "Jyutping", "Bopomofo"]
speech_options = [ "None", "Google TTS Mandarin"]


def display_next_tip():
    (tip, link) = chinese_support_config.get_next_tip()
    if tip:
        if link:
            if askUser(tip):
                openLink(link)
        else:
            showInfo(tip)

def goto_page(page):
    openLink(page)

def set_dict_constructor(dict):
    def set_dict():
        translate.set_dict(dict)
        update_dict_action_checkboxes()
    return set_dict

def set_option_constructor(option, value):
    def set_option():
        chinese_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


edit_window = None

def edit_logic_ok():
    open(edit_behavior_file, "w").write(edit_window.text.toPlainText().encode("utf8"))
    reload(edit_behavior)

def edit_logic():
    d = QDialog(mw)
    global edit_window
    edit_window = aqt.forms.editaddon.Ui_Dialog()
    edit_window.setupUi(d)
    d.setWindowTitle(_("Configure behavior of note edit dialog box"))
    edit_window.text.setPlainText(unicode(open(edit_behavior_file).read(), "utf8"))
    d.connect(edit_window.buttonBox, SIGNAL("accepted()"), edit_logic_ok)
    d.exec_()

def add_action(title, to, funct, checkable=False):
    action = QAction(_(title), mw)
    if checkable:
        action.setCheckable(True)
    mw.connect(action, SIGNAL("triggered()"), funct)
    to.addAction(action)
    return action

def update_dict_action_checkboxes():
    global ui_actions
    for d, d_name in dictionaries:
        ui_actions["dict_"+d].setChecked(d==chinese_support_config.options["dictionary"])
    for t in transcriptions:
        ui_actions["transcription_"+t].setChecked(t==chinese_support_config.options["transcription"])
    for t in speech_options:
        ui_actions["speech_"+t].setChecked(t==chinese_support_config.options["speech"])


def myRebuildAddonsMenu(self):
    global ui_actions
    for m in self._menus:
        if "Chinese_support"==m.title():
            sm=m.addMenu(_("Set dictionary"))
            for d, d_names in dictionaries:
                ui_actions["dict_"+d]=add_action(d_names, sm, set_dict_constructor(d),True)
            sm=m.addMenu(_("Set transcription"))
            for i in transcriptions:
                ui_actions["transcription_"+i]=add_action(i, sm, set_option_constructor("transcription", i), True)
            sm=m.addMenu(_("Set speech language"))
            for i in speech_options:
                ui_actions["speech_"+i]=add_action(i, sm, set_option_constructor("speech", i), True)
            add_action(_("Editor Behavior"), m, edit_logic)
            sm=m.addMenu(_("Help"))
            ### REMINDER : the website addresses are also available in config.py, in some startup tips. Don't forget to update both.
            add_action(_("Setup instructions"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki/Setup-Instructions"))
            add_action(_("Usage instructions"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki"))
            add_action(_("Support forum"), sm, lambda : goto_page("https://groups.google.com/forum/#!msg/anki-addons/YZmzNpmEuaY/OKbqbfGaMA0J"))
            add_action(_("Report a bug"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/issues"))
            add_action(_("About..."), m, lambda : showInfo(u"Chinese support plugin v. " + __init__.__version__ + u"<br>Copyright © 2012 Thomas TEMP&Eacute; and many others.<br><br>Please see source code for additional info."))
            add_action(_("Please rate me on Ankiweb!"), m, lambda : goto_page("https://ankiweb.net/shared/addons/"))
            m.setTitle(_("Chinese support"))
            update_dict_action_checkboxes()
            break


aqt.addons.AddonManager.rebuildAddonsMenu = wrap(aqt.addons.AddonManager.rebuildAddonsMenu, myRebuildAddonsMenu)

display_next_tip()
