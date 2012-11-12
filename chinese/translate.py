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


import re, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, QObject

from aqt import mw
from aqt.utils import showInfo, askUser, showWarning
import Chinese_support
from chinese.config import chinese_support_config
import cjklib.dictionary
import ui


# Automatic translation
##########################################################################

cjkdict = None
installing_dict=None

def transcribe_cjklib(chinese):
    '''Lookup word in current dictionary.
    If a single transcription exists, return it. Else return None.
    '''
    global cjkdict
    if None == cjkdict:
        #No CJKlib dictionary set
        return None
    if 1==len(chinese):
        #Don't use this method if only one character
        return None
    result_set = cjkdict.getForHeadword(chinese)
    ts = None
    for result in result_set:
        t = result[2]
        if ts and ts <> t:
            #Don't return a transcription if multiple exist
            return None
        ts=t
    return ts
    

def translate_cjklib(chinese):
    global cjkdict
    if None == cjkdict:
        #No CJKlib dictionary set
        return ""

    r = ''
    for dd in cjkdict.getForHeadword(chinese):
        r += dd[3]+"/"
    r = re.sub(r"(.)/+(.)", r"\1<br>\2", r)
    r = re.sub(r"/", r"", r)
    return r
    

def translate(chinese):
    chinese = re.sub(r'<.*?>', '', chinese)
    chinese = re.sub(r'\[.*?\]', '', chinese)
    translation = translate_cjklib(chinese)
    return translation

def init_dict(dict_name):
    global cjkdict
    if "CEDICT"==dict_name:
        cjkdict=cjklib.dictionary.CEDICT()
    elif "HanDeDict"==dict_name:
        cjkdict=cjklib.dictionary.HanDeDict()
    elif "CFDICT"== dict_name:
        cjkdict=cjklib.dictionary.CFDICT()

        
def set_dict(dict_name):
    #First, try out the designated dictionary, then save.
    #If it fails, offer the user to install dict
    global installing_dict

    try:
        init_dict(dict_name)
        chinese_support_config.set_option('dictionary', dict_name)
        return True
    except ValueError:
        try:
            if askUser(_("This dictionary will be downloaded from the Internet now.<br>This will take a few minutes<br>Do you want to continue?")):
                installing_dict = dict_name
                install_dict(dict_name)
        except:
            pass
    return False
        


class installerThread(QtCore.QThread):
    def __init__(self, dict):
        self.dict = dict
        QtCore.QThread.__init__(self)

    def run(self):
        from cjklib.dictionary.install import DictionaryInstaller
        try:
            installer = DictionaryInstaller()
            installer.install(self.dict, local=True)
            self.emit(SIGNAL('install_finished'))
        except IOError:
            self.emit(SIGNAL('install_failed'))

        
def install_failed():
    mw.progress.finish()
    showWarning(_("There was an error during dictionary download.<br>Please try again later."))


def install_finished():
    mw.progress.finish()
    showInfo(_("Install succeeded<br>Please restart Anki now for your dictionary settings to take effect."))
    chinese_support_config.set_option('dictionary', installing_dict)
    ui.update_dict_action_checkboxes()


t = None

def install_dict(dict):
    global t
    mw.progress.start(immediate=True)
    t = installerThread(dict)
    QObject.connect(t, SIGNAL('install_finished'), install_finished, QtCore.Qt.QueuedConnection)
    QObject.connect(t, SIGNAL('install_failed'), install_failed, QtCore.Qt.QueuedConnection)
    t.start()

try:
    init_dict(chinese_support_config.options["dictionary"])
except:
    showWarning(_("The current dictionary for Chinese Support Add-on does not seem to be properly installed. Please re-select your dictionary from the list."))
    chinese_support_config.set_option('dictionary', "None")
