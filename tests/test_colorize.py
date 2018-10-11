from . import ChineseTests

from random import randint


class ColorizeTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.edit_functions import colorize
        self.func = colorize

    def test_add_whitespace(self):
        self.assertEqual(
            self.func(['xiàn', 'zài']),
            '<span class="tone4">xiàn</span> <span class="tone4">zài</span>'
        )

    def test_remove_whitespace(self):
        self.assertEqual(
            self.func(['xiàn zài']),
            '<span class="tone4">xiàn</span><span class="tone4">zài</span>'
        )

    def test_ruby(self):
        self.assertEqual(
            self.func(['你[nǐ]']), '你[<span class="tone3">nǐ</span>]')
        self.assertEqual(
            self.func(['你[nǐ]'], True), '<span class="tone3">你[nǐ]</span>')


class ColorizeFuseTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.edit_functions import colorize_fuse
        self.func = colorize_fuse

    def test_tone_number(self):
        a = randint(0, 9)
        b = randint(0, 9)
        c = randint(0, 9)
        self.assertEqual(
            self.func('图书馆', 'tu{} shu{} guan{}'.format(a, b, c)),
            ('<span class="tone{}">图</span>'
             '<span class="tone{}">书</span>'
             '<span class="tone{}">馆</span>').format(a, b, c)
        )

    def test_tone_mark(self):
        self.assertEqual(
            self.func('图书馆', 'tú shū guǎn'),
            ('<span class="tone2">图</span>'
             '<span class="tone1">书</span>'
             '<span class="tone3">馆</span>')
        )

    def test_unseparated(self):
        self.assertEqual(
            self.func('图书馆', 'túshūguǎn'),
            ('<span class="tone2">图</span>'
             '<span class="tone1">书</span>'
             '<span class="tone3">馆</span>')
        )
