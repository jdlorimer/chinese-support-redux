# Copyright © 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
#
# This file is part of Chinese Support Redux.
#
# Chinese Support Redux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Chinese Support Redux is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Chinese Support Redux.  If not, see <https://www.gnu.org/licenses/>.

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
from .gui import display_tip, load_menu, unload_menu
from .models import advanced
from .models import basic
from .templates import chinese, ruby


def load():
    ruby.install()
    chinese.install()
    addHook('profileLoaded', load_menu)
    addHook('loadNote', append_tone_styling)
    addHook('unloadProfile', dictionary.conn.close)
    addHook('unloadProfile', unload_menu)
    models.append(('Chinese (Basic)', basic.add_model))
    models.append(('Chinese (Advanced)', advanced.add_model))
    CollectionStats.todayStats = wrap(
        CollectionStats.todayStats, todayStats, 'around')
    EditManager()
    display_tip()
