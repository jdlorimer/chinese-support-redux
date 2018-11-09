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

from chinese.color import colorize, colorize_fuse, local_dict_colorize


class ColorizeTests(ChineseTests):
    def test_add_whitespace(self):
        self.assertEqual(
            colorize(['xiàn', 'zài']),
            '<span class="tone4">xiàn</span> <span class="tone4">zài</span>'
        )

    def test_remove_whitespace(self):
        self.assertEqual(
            colorize(['xiàn zài']),
            '<span class="tone4">xiàn</span><span class="tone4">zài</span>'
        )

    def test_ruby(self):
        self.assertEqual(
            colorize(['你[nǐ]']), '你[<span class="tone3">nǐ</span>]')
        self.assertEqual(
            colorize(['你[nǐ]'], True), '<span class="tone3">你[nǐ]</span>')

    def test_bopomofo(self):
        self.assertEqual(
            colorize(['ㄊㄨˊ', 'ㄕㄨ', 'ㄍㄨㄢˇ']),
            ('<span class="tone2">ㄊㄨˊ</span> '
             '<span class="tone1">ㄕㄨ</span> '
             '<span class="tone3">ㄍㄨㄢˇ</span>')
        )


class ColorizeFuseTests(ChineseTests):
    def test_tone_number(self):
        a = randint(0, 9)
        b = randint(0, 9)
        c = randint(0, 9)
        self.assertEqual(
            colorize_fuse('图书馆', 'tu{} shu{} guan{}'.format(a, b, c)),
            ('<span class="tone{}">图</span>'
             '<span class="tone{}">书</span>'
             '<span class="tone{}">馆</span>').format(a, b, c)
        )

    def test_tone_mark(self):
        self.assertEqual(
            colorize_fuse('图书馆', 'tú shū guǎn'),
            ('<span class="tone2">图</span>'
             '<span class="tone1">书</span>'
             '<span class="tone3">馆</span>')
        )

    def test_unseparated(self):
        self.assertEqual(
            colorize_fuse('图书馆', 'túshūguǎn'),
            ('<span class="tone2">图</span>'
             '<span class="tone1">书</span>'
             '<span class="tone3">馆</span>')
        )


class LocalDictColorizeTests(ChineseTests):
    def test_word(self):
        self.assertEqual(
            local_dict_colorize('图书馆[tu2 shu1 guan3]'),
            ('<span class="tone2"><ruby>图<rt>tú</rt></ruby></span>'
             '<span class="tone1"><ruby>书<rt>shū</rt></ruby></span>'
             '<span class="tone3"><ruby>馆<rt>guǎn</rt></ruby></span>')
        )

    def test_classifier(self):
        self.assertEqual(
            local_dict_colorize('個|个[ge4]'),
            ('<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
             '<span class="tone4">个</span>')
        )
