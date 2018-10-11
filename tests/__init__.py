from unittest import TestCase
from unittest.mock import MagicMock, patch
import unittest

unittest.util._MAX_LENGTH = 160


class ChineseTests(TestCase):
    def setUp(self):
        modules = {
            'anki': MagicMock(),
            'aqt': MagicMock(),
            'chinese.main': MagicMock(),
            'gtts': MagicMock(),
            'requests': MagicMock(),
        }
        self.patcher = patch.dict('sys.modules', modules)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
