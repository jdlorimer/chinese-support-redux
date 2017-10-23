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

import os.path

from anki.hooks import wrap
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, openLink, askUser
import aqt.main

from _version import __version__
from config import chinese_support_config
from fill_missing import fill_sounds, fill_pinyin, fill_translation, fill_simp_trad, fill_silhouette
import edit_behavior
import edit_ui


ui_actions = {}
dictionaries = [
("None", _("None")),
("local_en", _("English")),
("local_de", _("German")),
("local_fr", _("French"))]

transcriptions = [
    "Pinyin", "Pinyin (Taiwan)", "Cantonese", "Bopomofo"]
#    "Pinyin", "WadeGiles", "CantoneseYale", "Jyutping", "Bopomofo"]
speech_options = [ "None", "Google TTS Mandarin", "Google TTS Cantonese", "Baidu Translate"]

msTranslateLanguages = [
("Arabic","ar"),
("Bulgarian","bg"),
("Catalan","ca"),
("Czech","cs"),
("Danish","da"),
("Dutch","nl"),
("English","en"),
("Estonian","et"),
("Persian (Farsi)","fa"),
("Finnish","fi"),
("French","fr"),
("German","de"),
("Greek","el"),
("Haitian Creole","ht"),
("Hebrew","he"),
("Hindi","hi"),
("Hungarian","hu"),
("Indonesian","id"),
("Italian","it"),
("Japanese","ja"),
("Korean","ko"),
("Latvian","lv"),
("Lithuanian","lt"),
("Malay","ms"),
("Hmong Daw","mww"),
("Norwegian","no"),
("Polish","pl"),
("Portuguese","pt"),
("Romanian","ro"),
("Russian","ru"),
("Slovak","sk"),
("Slovenian","sl"),
("Spanish","es"),
("Swedish","sv"),
("Thai","th"),
("Turkish","tr"),
("Ukrainian","uk"),
("Urdu","ur"),
("Vietnamese ","vi")
]


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
        chinese_support_config.set_option("dictionary", dict)
        update_dict_action_checkboxes()
    return set_dict

def set_option_constructor(option, value):
    def set_option():
        chinese_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


edit_window = None


def fill_sounds_logic():
    fill_sounds(mw.col, mw.web.key)

def fill_pinyin_logic():
    fill_pinyin(mw.col, mw.web.key)

def fill_translation_logic():
    fill_translation(mw.col, mw.web.key)

def fill_simp_trad_logic():
    fill_simp_trad(mw.col, mw.web.key)

def fill_silhouette_logic():
    fill_silhouette(mw.col, mw.web.key)

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
    for name, code in msTranslateLanguages:
        ui_actions["dict_"+code].setChecked(code==chinese_support_config.options["dictionary"])
    for t in transcriptions:
        ui_actions["transcription_"+t].setChecked(t==chinese_support_config.options["transcription"])
    for t in speech_options:
        ui_actions["speech_"+t].setChecked(t==chinese_support_config.options["speech"])


def myRebuildAddonsMenu(self):
    global ui_actions
    m = mw.form.menuTools.addMenu("Chinese Support")
    sm=m.addMenu(_("Use local dictionary"))
    for d, d_names in dictionaries:
        ui_actions["dict_"+d]=add_action(d_names, sm, set_dict_constructor(d),True)
    sm=m.addMenu(_("Use Microsoft Translate"))
    for name, code in msTranslateLanguages:
        ui_actions["dict_"+code]=add_action(name, sm, set_dict_constructor(code),True)
    sm=m.addMenu(_("Set transcription"))
    for i in transcriptions:
        ui_actions["transcription_"+i]=add_action(i, sm, set_option_constructor("transcription", i), True)
    sm=m.addMenu(_("Set speech engine"))
    for i in speech_options:
        ui_actions["speech_"+i]=add_action(i, sm, set_option_constructor("speech", i), True)
    sm=m.addMenu(_("Fill incomplete notes"))
    add_action(_("Fill missing sounds"), sm, fill_sounds_logic)
    add_action(_("Fill pinyin and color"), sm, fill_pinyin_logic)
    add_action(_("Fill translation"), sm, fill_translation_logic)
    add_action(_("Fill simplified/traditional"), sm, fill_simp_trad_logic)
    add_action(_("Fill silhouette"), sm, fill_silhouette_logic)
    sm=m.addMenu(_("Help"))
    ### REMINDER : the website addresses are also available in config.py, in some startup tips. Don't forget to update both.
    add_action(_("Setup instructions"), sm, lambda : goto_page("https://ankiweb.net/shared/info/3448800906"))
    add_action(_("Frequently asked questions"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki/Frequently-asked-questions"))
    add_action(_("Learning tips"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki/Learning-tips"))
    add_action(_("Support forum"), sm, lambda : goto_page("https://anki.tenderapp.com/discussions/add-ons/1646-chinese-support-add-on"))
    add_action(_("Development forum"), sm, lambda : goto_page("https://anki.tenderapp.com/discussions/add-ons/2336-chinese-support-add-on-development"))
    add_action(_("Video tutorial"), sm, lambda : goto_page("http://youtu.be/SiGUrrxptpg"))
    add_action(_("Report a bug"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/issues"))
    add_action(_("About..."), m, lambda : showInfo(u"Chinese support plugin v. " + __version__ + u"<br>Copyright © 2012-2014 Thomas TEMP&Eacute; and many others.<br><br>Please see source code for additional info."))
    add_action(_("Please rate me on Ankiweb!"), m, lambda : goto_page("https://ankiweb.net/shared/info/3448800906"))
    update_dict_action_checkboxes()



aqt.addons.AddonManager.rebuildAddonsMenu = wrap(aqt.addons.AddonManager.rebuildAddonsMenu, myRebuildAddonsMenu)

display_next_tip()
