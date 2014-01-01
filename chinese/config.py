# -*- coding: utf-8 ; mode: python -*-
#
#   Copyright © 2012 by Roland Sieker, <ospalh@gmail.com> 
#   Copyright © 2012 by Thomas TEMPÉ, <thomas.tempe@alysse.org>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import os.path
import json
import __init__
from aqt import mw

initial_options =  { 
'startup_tip_number':0, 
'show_startup_tips':True,
'dictionary':'None',
'transcription':'Pinyin',
'speech':'Google TTS Mandarin',
}

startup_tips = [
('Thank you for installing the Chinese Support Add-on<br>&nbsp;<br>Before using it, you will need to create a new note type.<br>Would you like to learn how?','https://github.com/ttempe/chinese-support-addon/wiki/Setup-Instructions'),
("The Chinese Support Add-on allows you to choose and download a dictionary, that will be used to pre-fill your cards data.<br>Would you like to learn more about this feature?",'https://github.com/ttempe/chinese-support-addon/wiki/Dictionary-Setup-Instructions'),
('If you set a dictionary for Chinese translation, it will also be used to fill in you Pinyin more cleverly.<br>To do so, click on Tools->Add-ons->Chinese Support->Set dictionary.', None),
(None, None),
(None, None),
(None, None),
(None, None),
('Thank you for using the <b>Chinese Support Add-on</b>. <br/>If you like it, please take a moment to rate it in <a href="https://ankiweb.net/shared/addons/">Ankiweb</a>. <br/>If you have questions or comments, don\'t hesitate to post them on the <a href="https://groups.google.com/forum/#!msg/anki-addons/YZmzNpmEuaY/OKbqbfGaMA0J">support forum</a>', None)
]



class config:
    filepath = ""
    options = {}
    
    def __init__(self):
        #self.filepath = os.path.join(mw.pm.profileFolder(), "chinese_config.json")
        self.filepath = os.path.join(mw.pm.addonFolder(), "chinese", "chinese_addon_config.json")
        self.load()
        #Options that may be missing in some installs initialized by old versions of this code
        self.add_option("latest_available_version", __init__.__version__)
        self.add_option("next_version_message", None)
        self.add_option("warned_about_MS_translate_long_delays", False)
    def load(self):
        if not os.path.exists(self.filepath):
            self.create_new()
        self.options = json.load(open(self.filepath, 'r')) 

    def save(self):
        json.dump(self.options, open(self.filepath, 'w'))

    def create_new(self):
        self.options = initial_options
        self.save()

    def set_option(self, name, value):
        self.options[name]=value
        self.save()

    def add_option(self, name, default_value):
        '''To make sure an old config file remains compatible with a
        newer version of this add-on, call this in __init__.'''
        if not name in self.options:
            self.set_option(name, default_value)

    def get_next_tip(self):
        if self.options['startup_tip_number'] < len(startup_tips):
            self.set_option("startup_tip_number", self.options['startup_tip_number']+1)
            return startup_tips[self.options['startup_tip_number']-1]
        else:
            return (None, None)

chinese_support_config = config()

