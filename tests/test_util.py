from . import ChineseTests


class UtilTests(ChineseTests):
    def test_no_hidden(self):
        from chinese.util import no_hidden
        self.assertEqual(no_hidden('a <!-- b --> c'), 'a  c')

    def test_no_sound(self):
        from chinese.util import no_sound
        self.assertEqual(no_sound('a [sound:] b'), 'a  b')
