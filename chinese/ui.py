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
from aqt.utils import showInfo, openLink
import aqt.addons 
from anki.hooks import wrap
import __init__
import translate
import dict_setting

def setup_plugin():
    openLink("https://github.com/ttempe/chinese-support-addon/wiki/Setup-Instructions")

def help_plugin():
    openLink("https://github.com/ttempe/chinese-support-addon/wiki")

def about_plugin():
    showInfo(u"Chinese support plugin v. " + __init__.__version__ + u"<br>Copyright © 2012 Thomas TEMP&Eacute; and many others.<br><br>Please see source code for additional info.")

def set_dict_None():
    translate.set_dict("None")
    update_dict_action_checkboxes()

def set_dict_CEDICT():
    translate.set_dict("CEDICT")
    update_dict_action_checkboxes()

def set_dict_HanDeDict():
    translate.set_dict("HanDeDict")
    update_dict_action_checkboxes()

def set_dict_CFDICT():
    translate.set_dict("CFDICT")
    update_dict_action_checkboxes()

def plop():
    pass


def add_action(title, to, funct, checkable=False):
    action = QAction(_(title), mw)
    if checkable:
        action.setCheckable(True)
    mw.connect(action, SIGNAL("triggered()"), funct)
    to.addAction(action)
    return action

dict_setting.dict_action_None=None
dict_setting.dict_action_CEDICT=None
dict_setting.dict_action_HanDeDict=None
dict_setting.dict_action_CFDICT=None

def update_dict_action_checkboxes():
    dict_setting.dict_action_None.setChecked("None"==dict_setting.dict_name)
    dict_setting.dict_action_CEDICT.setChecked("CEDICT"==dict_setting.dict_name)
    dict_setting.dict_action_HanDeDict.setChecked("HanDeDict"==dict_setting.dict_name)
    dict_setting.dict_action_CFDICT.setChecked("CFDICT"==dict_setting.dict_name)


def myRebuildAddonsMenu(self):
    for m in self._menus:
        if "Chinese_support"==m.title():
            sm=m.addMenu(_("Set dictionary"))
            dict_setting.dict_action_None=add_action(_("None"), sm, set_dict_None, True)
            dict_setting.dict_action_CEDICT=add_action(_("English"), sm, set_dict_CEDICT, True)
            dict_setting.dict_action_HanDeDict=add_action(_("Deutsch"), sm, set_dict_HanDeDict, True)
            dict_setting.dict_action_CFDICT=add_action(_("Francais"), sm, set_dict_CFDICT, True)
            update_dict_action_checkboxes()
            add_action(_("Setup instructions"), m, setup_plugin)
            add_action(_("Help"), m, help_plugin)
            add_action(_("About..."), m, about_plugin)
            m.setTitle(_("Chinese support"))
            break

aqt.addons.AddonManager.rebuildAddonsMenu = wrap(aqt.addons.AddonManager.rebuildAddonsMenu, myRebuildAddonsMenu)
