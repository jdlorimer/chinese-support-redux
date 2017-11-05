# -*- coding: utf-8 -*-
# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from os.path import dirname, realpath
import json
import os.path

initial_options = {
    'dictionary': 'local_en',
    'enabledModels': [],
    'show_startup_tips': False,
    'speech': 'Baidu Translate',
    'startup_tip_number': 0,
    'transcription': 'Pinyin',
}

startup_tips = [(None, None)]


class Config:
    filepath = ''
    options = {}

    def __init__(self):
        self.filepath = os.path.join(dirname(realpath(__file__)), 'config.json')
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
        self.options[name] = value
        self.save()

    def add_option(self, name, default_value):
        if name not in self.options:
            self.set_option(name, default_value)

    def get_next_tip(self):
        if self.options['startup_tip_number'] < len(startup_tips):
            self.set_option('startup_tip_number',
                            self.options['startup_tip_number'] + 1)
            return startup_tips[self.options['startup_tip_number'] - 1]
        else:
            return (None, None)


chinese_support_config = Config()
