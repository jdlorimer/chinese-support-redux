# Copyright © 2018 Joseph Lorimer <luoliyan@posteo.net>
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

import unittest
from gettext import NullTranslations
from logging import getLogger
from unittest import TestCase
from unittest.mock import MagicMock, patch


NullTranslations().install()
unittest.util._MAX_LENGTH = 160

modules = {
    'PyQt5.QtGui': MagicMock(),
    'PyQt5.QtWidgets': MagicMock(),
    'anki': MagicMock(),
    'anki.find': MagicMock(),
    'anki.hooks': MagicMock(),
    'anki.stats': MagicMock(),
    'anki.stdmodels': MagicMock(),
    'anki.template': MagicMock(),
    'anki.template.hint': MagicMock(),
    'anki.utils': MagicMock(),
    'aqt': MagicMock(),
    'aqt.utils': MagicMock(),
    'gtts': MagicMock(),
    'requests': MagicMock(),
}
patch.dict('sys.modules', modules).start()
patch(
    'aqt.mw.addonManager.getConfig',
    lambda a: {
        'firstRun': False,
        'tip_number': 0,
        'transcription': 'Pinyin',
    }
).start()


class ChineseTests(TestCase):
    def setUp(self):
        self.logger = getLogger()
        self.logger.setLevel('DEBUG')
