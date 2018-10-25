# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from anki.stats import CollectionStats
from anki.hooks import addHook, wrap
from anki.stdmodels import models

from .config import ConfigManager

config_manager = ConfigManager()

from .database import DictDB

dictionary = DictDB()
if config_manager.options['firstRun']:
    dictionary.create_indices()
    config_manager.options['firstRun'] = False

from .edit import append_tone_styling, EditManager
from .graph import todayStats
from .models import advanced
from .models import basic
from .templates import chinese, ruby
from .ui import display_tip, load_menu


def load():
    ruby.install()
    chinese.install()
    addHook('profileLoaded', load_menu)
    addHook('loadNote', append_tone_styling)
    addHook('unloadProfile', dictionary.conn.close)
    models.append(('Chinese (Basic)', basic.add_model))
    models.append(('Chinese (Advanced)', advanced.add_model))
    CollectionStats.todayStats = wrap(
        CollectionStats.todayStats, todayStats, 'around')
    EditManager()
    display_tip()
