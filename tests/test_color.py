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

from random import randint
from unittest.mock import Mock, patch

from . import ChineseTests


class ColorizeTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.color import colorize
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

    def test_bopomofo(self):
        self.assertEqual(
            self.func(['ㄊㄨˊ', 'ㄕㄨ', 'ㄍㄨㄢˇ']),
            ('<span class="tone2">ㄊㄨˊ</span> '
             '<span class="tone1">ㄕㄨ</span> '
             '<span class="tone3">ㄍㄨㄢˇ</span>')
        )


class ColorizeFuseTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.color import colorize_fuse
        self.func = colorize_fuse
        self.sanitize = patch(
            'chinese.color.sanitize_pinyin',
            lambda a: a.split()
        )
        self.sanitize.start()

    def tearDown(self):
        super().tearDown()
        self.sanitize.stop()

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
        m = Mock(return_value=['tú', 'shū', 'guǎn'])
        self.sanitize = patch('chinese.color.sanitize_pinyin', m)
        self.sanitize.start()
        self.assertEqual(
            self.func('图书馆', 'túshūguǎn'),
            ('<span class="tone2">图</span>'
             '<span class="tone1">书</span>'
             '<span class="tone3">馆</span>')
        )


class LocalDictColorizeTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.color import local_dict_colorize
        self.func = local_dict_colorize
        self.sanitize = patch(
            'chinese.color.sanitize_pinyin',
            lambda a: a.split()
        )
        self.sanitize.start()

    def tearDown(self):
        super().tearDown()
        self.sanitize.stop()

    def test_word(self):
        self.assertEqual(
            self.func('图书馆[tu2 shu1 gwan3]'),
            ('<span class="tone2"><ruby>图<rt>tu2</rt></ruby></span>'
             '<span class="tone1"><ruby>书<rt>shu1</rt></ruby></span>'
             '<span class="tone3"><ruby>馆<rt>gwan3</rt></ruby></span>')
        )

    def test_classifier(self):
        self.assertEqual(
            self.func('個|个[ge4]'),
            ('<span class="tone4"><ruby>個<rt>ge4</rt></ruby></span>|'
             '<span class="tone4">个</span>')
        )
