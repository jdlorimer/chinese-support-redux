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
import dict_setting
import cjklib.dictionary


# Automatic translation
##########################################################################

cjkdict = None


def try_dict():
    pass


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

        
def set_dict(dict_name, second_run="None"):
    #First, try out the designated dictionary, then save.
    #If it fails, offer the user to install dict
    
    try:
        init_dict(dict_name)
    except ValueError:
        if askUser(_("This dictionary will be downloaded from the Internet now.<br>This will take a few minutes<br>Do you want to continue?")):
            install_dict(dict_name)
        else:
            dict_name="None"

    dict_setting.dict_name = dict_name
    fd=open( os.path.join(Chinese_support.addon_dir, "chinese", "dict_setting.py"), "w")
    fd.write("#Name of dictionary to perform lookup from\n")
    fd.write("#This file is generated from the plugin menu\n")
    fd.write("dict_name='"+dict_setting.dict_name+"'\n")
    fd.write("first_run=False\n")
    fd.write("second_run="+second_run+"\n")
    fd.close()


class installerThread(QtCore.QThread):
    def __init__(self, dict):
        self.dict = dict
        QtCore.QThread.__init__(self)

    def run(self):
        from cjklib.dictionary.install import DictionaryInstaller
        try:
            installer = DictionaryInstaller()
            installer.install(self.dict, local=True)
        except IOError:
            self.emit(SIGNAL('install_failed'))
        self.emit(SIGNAL('install_finished'))

        
def install_failed():
    showWarning(_("There was an error during dictionary download.<br>Please try again later."))
    dict_name="None"


def install_finished():
    mw.progress.finish()
    showInfo(_("Download complete.<br>Please restart Anki and re-select your dictionary."))
t = None

def install_dict(dict):
    global t
    mw.progress.start(immediate=True)
    t = installerThread(dict)
    QObject.connect(t, SIGNAL('install_finished'), install_finished, QtCore.Qt.QueuedConnection)
    QObject.connect(t, SIGNAL('install_failed'), install_failed, QtCore.Qt.QueuedConnection)
    t.start()


