# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas TEMPÉ, <thomas.tempe@alysse.org>
# 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
import os, sys, os.path
import  md5
from aqt import mw
from aqt.utils import askUser, isWin

from config import chinese_support_config 
from __init__ import __version__
older_versions = ['\xb8\xd2\x9e\x073\x8f\xad\xf6\xe2cip\xdd\xe9;\xa2',
'_\x7f\xfa\xd6=\x95\x89\xd7\x18\xd9A\x9a\xeb_\xf9\xa3']

upgrade_question = _("You have just upgraded <b>Chinese Support add-on</b> from an earlier version.<br>This version comes with a newer Edit Behavior, possibly adding new features or fixing bugs ; however, it seems that you have personalized this file yourself.<br>If you choose to upgrade, your old file will be kept as edit_behavior.py.old.<br>&nbsp;<br>Do you want to use the new Edit Behavior file? (if unsure, say Yes)")

addon_dir = mw.pm.addonFolder()
if isWin:
    addon_dir = addon_dir.encode(sys.getfilesystemencoding())
sys.path.insert(0, os.path.join(addon_dir, "chinese") )

edit_behavior = os.path.join(addon_dir, "chinese", "edit_behavior.py")
edit_behavior_model = os.path.join(addon_dir, "chinese", "edit_behavior_model.py")

def compare_versions():
    return open(edit_behavior_model).read() == open(edit_behavior).read()

def backup():
    open(edit_behavior+".old", "w").write(open(edit_behavior_model).read())

def copy_from_model():
    open(edit_behavior, "w").write(open(edit_behavior_model).read())

def ask_to_upgrade():
    if askUser(upgrade_question):
        backup()
        copy_from_model()

def update_config():
    chinese_support_config.set_option("add-on version", __version__)
    chinese_support_config.set_option("edit_behavior_model.py hash", md5.new(open(edit_behavior_model).read()).hexdigest())

if not os.path.exists(edit_behavior):
    #New install or erased config file
    copy_from_model()
    update_config()
elif not "edit_behavior_model.py hash" in chinese_support_config.options:
    #We are upgrading from 0.6.0 or earlier
    current_hash = md5.new(open(edit_behavior).read()).digest()
    if current_hash not in older_versions:
        #User-modified
        ask_to_upgrade()
    update_config()
elif __version__ <> chinese_support_config.options["add-on version"]:
    #New version. Compare current edit_behavior with former model
    current_hash = md5.new(open(edit_behavior).read()).hexdigest()
    if current_hash <> chinese_support_config.options["edit_behavior_model.py hash"]:
        ask_to_upgrade()
    update_config()
else:
    #Not upgrading. Do nothing.
    pass
