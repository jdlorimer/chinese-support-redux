from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch


class UtilTests(TestCase):
    def setUp(self):
        modules = {
            'anki': MagicMock(),
            'anki.find': MagicMock(),
            'anki.hooks': MagicMock(),
            'anki.stdmodels': MagicMock(),
            'anki.template': MagicMock(),
            'anki.template.hint': MagicMock(),
            'anki.utils': MagicMock(),
            'aqt': MagicMock(),
            'aqt.qt': MagicMock(),
            'aqt.utils': MagicMock(),
            'chinese.ui': MagicMock(),
            'requests': MagicMock(),
        }
        self.patcher = patch.dict('sys.modules', modules)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_no_hidden(self):
        from chinese.util import no_hidden
        self.assertEqual(no_hidden('a <!-- b --> c'), 'a  c')

    def test_no_sound(self):
        from chinese.util import no_sound
        self.assertEqual(no_sound('a [sound:] b'), 'a  b')

    def test_ruby_top(self):
        from chinese.util import ruby_top
        self.assertEqual(ruby_top('汉[hàn]字[zì]'), 'hàn zì ')

    def test_ruby_bottom(self):
        from chinese.util import ruby_bottom
        self.assertEqual(ruby_bottom('汉[hàn]字[zì]'), '汉 字 ')
