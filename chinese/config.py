# -*- coding: utf-8 ; mode: python -*-
#
#   Copyright © 2012 by Roland Sieker, <ospalh@gmail.com> 
#   Copyright © 2012 by Thomas TEMPÉ, <thomas.tempe@alysse.org>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import os.path
import json
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
('If you set a dictionary for Chinese translation, it will also be used to fill in you Pinyin more cleverly, saving your time.<br>Do you want to learn how to set one up?', 'https://github.com/ttempe/chinese-support-addon/wiki/Dictionary-Setup-Instructions')
]



class config:
    filepath = ""
    options = {}
    
    def __init__(self):
        #self.filepath = os.path.join(mw.pm.profileFolder(), "chinese_config.json")
        self.filepath = os.path.join(mw.pm.addonFolder(), "chinese", "chinese_addon_config.json")
        self.load()

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
        newer version of this add-on, call this early.'''
        if not name in self.options:
            self.set_option(name, default_value)

    def get_next_tip(self):
        if self.options['startup_tip_number'] < len(startup_tips)-1:
            self.set_option("startup_tip_number", self.options['startup_tip_number']+1)
            return startup_tips[self.options['startup_tip_number']-1]
        else:
            return (None, None)

chinese_support_config = config()
