# -*- coding: utf-8 ; mode: python -*-
# © 2012: Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


import sys
import os
from aqt import mw

sys.path.append(os.path.join(mw.pm.addonFolder(), 'chinese', 'cjklib'))

from pinyin import Pinyinizer, is_han_character, on_focus_lost

__version__ = '0.0a2'
