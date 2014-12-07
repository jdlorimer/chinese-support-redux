# -*- coding: utf-8 -*-
# Copyright 2013 Thomas TEMPE <thomas.tempe@alysse.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from anki.hooks import addHook, wrap
from aqt.editor import Editor
from config import chinese_support_config as config

toggleButton = None
config_file_key = None
editor_instance = None
enable = None #enable editor UI enhancements for the current note type?

def setupToggleButton(editor):
    global toggleButton
    global editor_instance
    editor_instance = editor
    toggleButton = editor_instance._addButton("mybutton", toggleButtonClick, size=False, text=u"汉子", tip="Enable/disable <b>Chinese Support Add-on</b> input fill-up") #check=True

def toggleButtonClick():
    global enable
    enable = not enable
    config.set_option(config_file_key, enable)
    updateToggleButton(editor_instance)

def updateToggleButton(editor):
    global config_file_key
    global enable
    try:
        model_name = editor.note.model()['name']
        model_id = editor.note.model()['id']
    except:
        return
    try:
        model_type = editor.note.model()['addon']
    except:
        model_type = None
    config_file_key = "enable_for_model_"+str(model_id)

    if config_file_key in config.options:
        enable = config.options[config_file_key]
    elif "Chinese (compatibility)" == model_type:
        enable = True
    else:
        enable = False

    if enable:
#        toggleButton.setChecked(True)
        toggleButton.setText(u"✓ 汉子")
    else:
#        toggleButton.setChecked(False)
        toggleButton.setText(u"✕ 汉子")
   

    
addHook("setupEditorButtons", setupToggleButton)
Editor.loadNote=wrap(Editor.loadNote, updateToggleButton)
