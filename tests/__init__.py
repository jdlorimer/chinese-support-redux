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

from logging import getLogger
from unittest import TestCase
from unittest.mock import MagicMock, patch
import unittest

unittest.util._MAX_LENGTH = 160


class ChineseTests(TestCase):
    def setUp(self):
        self.logger = getLogger()
        self.logger.setLevel('DEBUG')
        modules = {
            'anki': MagicMock(),
            'aqt': MagicMock(),
            'chinese.main': MagicMock(),
            'gtts': MagicMock(),
            'requests': MagicMock(),
        }
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        self.config_patcher = patch('chinese.main.config_manager', MagicMock())
        self.config = self.config_patcher.start()
        self.dictionary_patcher = patch('chinese.main.dictionary', MagicMock())
        self.dictionary = self.dictionary_patcher.start()

    def tearDown(self):
        self.module_patcher.stop()
        self.config_patcher.stop()
        self.dictionary_patcher.stop()
