from anki.stats import CollectionStats
from anki.hooks import addHook, wrap
from anki.stdmodels import models

from .config import ConfigManager

config_manager = ConfigManager()

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
    models.append(('Chinese (Basic)', basic.add_model))
    models.append(('Chinese (Advanced)', advanced.add_model))
    CollectionStats.todayStats = wrap(
        CollectionStats.todayStats, todayStats, 'around')
    EditManager()
    display_tip()
