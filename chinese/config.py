# -*- coding: utf-8 -*-
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from anki.hooks import addHook
from aqt import mw


class ConfigManager:
    def __init__(self):
        self.tips = []
        self.options = mw.addonManager.getConfig(__name__)
        addHook('unloadProfile', self.save)

    def save(self):
        mw.addonManager.writeConfig(__name__, self.options)

    def set_option(self, name, value):
        self.options[name] = value

    def get_next_tip(self):
        if self.options['startup_tip_number'] < len(self.tips):
            self.set_option('startup_tip_number',
                            self.options['startup_tip_number'] + 1)
            return self.tips[self.options['startup_tip_number'] - 1]
        else:
            return (None, None)


chinese_support_config = ConfigManager()
