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
('Thank you for downloading the <b>Chinese Support Add-on</b>.<br>Please remember to select a dictionary in the <tt>Tools-&gt;Chinese support</tt> menu, so that you may have automatic translation.', None),
(None, None),
('Did you know that the <b>Chinese support Add-on</b> offers two types of dictionaries? <br><b>Local dictionaries</b> are great for single-word look-up, and can point out words with multiple possible pronunciations, while <b>on-line translation</b> offers full-sentence translation.<br>Both are available under <tt>Tools-&gt;Chinese support</tt>.', None),
(None, None),
('Did you know that the <b>Chinese Support Add-on</b> can generate pronunciation for your chinese words?<br>Just make sure to select <b>Google TTS</b> in the <tt>Tools-&gt;Chinese</tt> menu, and that you have an Internet connexion when adding new cards.<br>If you missed this feature, no worries! You can still download audio for your existing cards with <tt>Tools-&gt;Chinese support-&gt;Fill missing sounds.</tt>',None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
(None, None),
('Thank you for using the <b>Chinese Support Add-on</b>. Did you know? This is a volunteer project to help you improve your Chinese. Hundreds of hours went into it!<br/>If you like it, please take a moment to rate it in <a href="https://ankiweb.net/shared/info/3448800906">Ankiweb</a>. <br/>If you have questions or comments, don\'t hesitate to post them on the <a href="https://anki.tenderapp.com/discussions/add-ons/1646-chinese-support-add-on">support forum</a>', None)
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

