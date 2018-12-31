# Copyright © 2018-2019 Joseph Lorimer <luoliyan@posteo.net>
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

from chinese.color import colorize, colorize_dict, colorize_fuse
from tests import ChineseTest


class Colorize(ChineseTest):
    def test_separate_syllables(self):
        self.assertEqual(
            colorize(['xiàn', 'zài']),
            '<span class="tone4">xiàn</span> <span class="tone4">zài</span>',
        )

    def test_joined_syllables(self):
        self.assertEqual(
            colorize(['xiàn zài']),
            '<span class="tone4">xiàn</span><span class="tone4">zài</span>',
        )

    def test_ruby(self):
        self.assertEqual(
            colorize(['你[nǐ]']), '你[<span class="tone3">nǐ</span>]'
        )
        self.assertEqual(
            colorize(['你[nǐ]'], True), '<span class="tone3">你[nǐ]</span>'
        )

    def test_bopomofo(self):
        self.assertEqual(
            colorize(['ㄊㄨˊ', 'ㄕㄨ', 'ㄍㄨㄢˇ']),
            (
                '<span class="tone2">ㄊㄨˊ</span> '
                '<span class="tone1">ㄕㄨ</span> '
                '<span class="tone3">ㄍㄨㄢˇ</span>'
            ),
        )


class ColorizeDict(ChineseTest):
    def test_word(self):
        self.assertEqual(
            colorize_dict('图书馆[tu2 shu1 guan3]'),
            (
                '<span class="tone2"><ruby>图<rt>tú</rt></ruby></span>'
                '<span class="tone1"><ruby>书<rt>shū</rt></ruby></span>'
                '<span class="tone3"><ruby>馆<rt>guǎn</rt></ruby></span>'
            ),
        )

    def test_classifier(self):
        self.assertEqual(
            colorize_dict('個|个[ge4]'),
            (
                '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
                '<span class="tone4">个</span>'
            ),
        )


class ColorizeFuse(ChineseTest):
    def test_tone_number(self):
        a = randint(1, 5)
        b = randint(1, 5)
        c = randint(1, 5)
        self.assertEqual(
            colorize_fuse('图书馆', 'tu{} shu{} guan{}'.format(a, b, c)),
            (
                '<span class="tone{}">图</span>'
                '<span class="tone{}">书</span>'
                '<span class="tone{}">馆</span>'
            ).format(a, b, c),
        )

    def test_tone_mark(self):
        self.assertEqual(
            colorize_fuse('图书馆', 'tú shū guǎn'),
            (
                '<span class="tone2">图</span>'
                '<span class="tone1">书</span>'
                '<span class="tone3">馆</span>'
            ),
        )

    def test_unseparated(self):
        self.assertEqual(
            colorize_fuse('图书馆', 'túshūguǎn'),
            (
                '<span class="tone2">图</span>'
                '<span class="tone1">书</span>'
                '<span class="tone3">馆</span>'
            ),
        )

    def test_added_punc(self):
        self.assertEqual(
            colorize_fuse('图书馆。', 'túshūguǎn'),
            (
                '<span class="tone2">图</span>'
                '<span class="tone1">书</span>'
                '<span class="tone3">馆</span>'
            ),
        )

    def test_truncated_chars(self):
        """Given truncated characters, should still highlight correctly."""
        self.assertEqual(
            colorize_fuse('图书', 'túshūguǎn'),
            '<span class="tone2">图</span><span class="tone1">书</span>',
        )

    def test_truncated_trans(self):
        """Given truncated transcription, should truncate characters."""
        self.assertEqual(
            colorize_fuse('图书馆', 'túshū'),
            '<span class="tone2">图</span><span class="tone1">书</span>',
        )

    def test_sentence(self):
        self.assertEqual(
            colorize_fuse(
                '没有，是我第一次来上海旅游。', 'Méiyǒu, shì wǒ dìyīcì lái shànghǎi lǚyóu.'
            ),
            (
                '<span class="tone2">没</span>'
                '<span class="tone3">有</span>，'
                '<span class="tone4">是</span>'
                '<span class="tone3">我</span>'
                '<span class="tone4">第</span>'
                '<span class="tone1">一</span>'
                '<span class="tone4">次</span>'
                '<span class="tone2">来</span>'
                '<span class="tone4">上</span>'
                '<span class="tone3">海</span>'
                '<span class="tone3">旅</span>'
                '<span class="tone2">游</span>。'
            ),
        )
