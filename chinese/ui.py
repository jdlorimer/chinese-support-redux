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
from anki.hooks import wrap
import aqt.main
import urllib2
import re

from config import chinese_support_config
import __init__
import Chinese_support
import edit_behavior
from upgrade import edit_behavior_file, do_upgrade
import edit_ui
from fill_missing import fill_sounds, fill_pinyin, fill_translation, fill_simp_trad, fill_silhouette

offer_auto_module_upgrade = False #Broken for now.

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

def check_for_next_version(*args, **kwargs):
    '''Attempt to fetch the __init__.py file from github, and check
    if it corresponds to a new release. If so, warn the user (exactly once
    per version).
    This function is called on exit.'''
    def is_newer(a, b):
        'compares version strings in the form "0.7.3"'
        version_re = r"(\d+)\.(\d+)\.(\d+).*"
        ra = re.search(version_re, a)
        rb = re.search(version_re, b)

        if int(ra.group(1))>int(rb.group(1)):
            return True
        elif int(ra.group(2))>int(rb.group(2)):
            return True
        elif int(ra.group(3))>int(rb.group(3)):
            return True
        else:
            return False
    try:
        #fetch the latest release on Github. This means github must be updated *after* Ankiweb
        latest_data = urllib2.urlopen('https://raw.github.com/ttempe/chinese-support-addon/master/chinese/__init__.py', timeout=7).read()
        latest_version = re.search(r"__version__\s*=\s*\"\"\"(.*?)\"\"\"", latest_data).group(1)
        latest_comment = re.search(r"release_info\s*=\s*\"\"\"(.*?)\"\"\"", latest_data, re.S).group(1)
        import __init__
        local_version = __init__.__version__
        if is_newer(latest_version, local_version):
            if chinese_support_config.options["latest_available_version"] <> latest_version:
                chinese_support_config.set_option("latest_available_version", latest_version)
                if offer_auto_module_upgrade:
                    chinese_support_config.set_option("next_version_message", "A new version of <b>Chinese Support Add-on</b> is available.<br>&nbsp;<br>Do you want Anki to <b>download and install it automatically</b> now?<br>&nbsp;Alternately, you can also download it later through <tt>Tools->Add-ons->Browse and install</tt>.<br>&nbsp;<br><b>Version "+latest_version+":</b><br>"+latest_comment)
                else:
                    chinese_support_config.set_option("next_version_message", 'A new version of <b>Chinese Support Add-on</b> is available.<br>&nbsp;<br>You can download it now through <tt>Tools->Add-ons->Browse and install</tt><br>&nbsp;<br>Add-on code: %s<br>&nbsp;<br><b>Version %s:</div><div>%s</div>' %( __init__.ankiweb_number, latest_version, latest_comment))
    except:
        pass

def display_new_version_message():
    #Only show message on next startup
    if chinese_support_config.options["next_version_message"]:
        if offer_auto_module_upgrade:
            if askUser(chinese_support_config.options["next_version_message"]):
                if do_upgrade():
                #success
                    chinese_support_config.set_option("next_version_message", None)
            else:
            #User does not want to be bothered with upgrades
                chinese_support_config.set_option("next_version_message", None)
        else:
            #no auto upgrade
            showInfo(chinese_support_config.options["next_version_message"])
            chinese_support_config.set_option("next_version_message", None)

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
    add_action(_("Editor Behavior"), m, edit_logic)
    sm=m.addMenu(_("Help"))
    ### REMINDER : the website addresses are also available in config.py, in some startup tips. Don't forget to update both.
    add_action(_("Setup instructions"), sm, lambda : goto_page("https://ankiweb.net/shared/info/3448800906"))
    add_action(_("Frequently asked questions"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki/Frequently-asked-questions"))
    add_action(_("Learning tips"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/wiki/Learning-tips"))
    add_action(_("Support forum"), sm, lambda : goto_page("https://anki.tenderapp.com/discussions/add-ons/1646-chinese-support-add-on"))
    add_action(_("Development forum"), sm, lambda : goto_page("https://anki.tenderapp.com/discussions/add-ons/2336-chinese-support-add-on-development"))
    add_action(_("Video tutorial"), sm, lambda : goto_page("http://youtu.be/SiGUrrxptpg"))
    add_action(_("Report a bug"), sm, lambda : goto_page("https://github.com/ttempe/chinese-support-addon/issues"))
    add_action(_("About..."), m, lambda : showInfo(u"Chinese support plugin v. " + __init__.__version__ + u"<br>Copyright © 2012-2014 Thomas TEMP&Eacute; and many others.<br><br>Please see source code for additional info."))
    add_action(_("Please rate me on Ankiweb!"), m, lambda : goto_page("https://ankiweb.net/shared/info/3448800906"))
    update_dict_action_checkboxes()



aqt.addons.AddonManager.rebuildAddonsMenu = wrap(aqt.addons.AddonManager.rebuildAddonsMenu, myRebuildAddonsMenu)

display_next_tip()
display_new_version_message()
#Check for new version of this plug-in when closing Anki
aqt.main.AnkiQt.onClose = wrap(aqt.main.AnkiQt.onClose, check_for_next_version)

#Uncomment to force display of next version info (debug)
#showInfo('A new version of <b>Chinese Support Add-on</b> is available.<br>&nbsp;<br>You can download it now through <tt>Tools->Add-ons->Browse and install</tt><br>&nbsp;<br>Add-on code: %s<br>&nbsp;<br><b>Version %s:</div><div>%s</div>' %( __init__.ankiweb_number, __init__.__version__, __init__.release_info))
