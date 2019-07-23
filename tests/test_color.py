# Copyright © 2018-2019 Joseph Lorimer <joseph@lorimer.me>
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

from unittest import skip

from hypothesis import given
from hypothesis.strategies import integers

from chinese.color import colorize, colorize_dict, colorize_fuse
from tests import Base


class TestColorize(Base):
    def test_joined_syllables(self):
        self.assertEqual(
            colorize(['xiàn zài']),
            '<span class="tone4">xiàn</span><span class="tone4">zài</span>',
        )

    def test_separate_syllables(self):
        self.assertEqual(
            colorize(['xiàn', 'zài']),
            '<span class="tone4">xiàn</span> <span class="tone4">zài</span>',
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

    def test_mixed_english_chinese(self):
        self.assertEqual(
            colorize(['Brian de']),
            '<span class="tone5">Brian</span><span class="tone5">de</span>',
        )


class TestColorizeDict(Base):
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


class TestColorizeFuse(Base):
    @given(integers(1, 5), integers(1, 5), integers(1, 5))
    def test_tone_number(self, a, b, c):
        self.assertEqual(
            colorize_fuse(['图', '书', '馆'], [f'tu{a}', f'shu{b}', f'guan{c}']),
            (
                '<span class="tone{}">图</span>'
                '<span class="tone{}">书</span>'
                '<span class="tone{}">馆</span>'
            ).format(a, b, c),
        )

    def test_tone_mark(self):
        self.assertEqual(
            colorize_fuse(['图', '书', '馆'], ['tú', 'shū', 'guǎn']),
            (
                '<span class="tone2">图</span>'
                '<span class="tone1">书</span>'
                '<span class="tone3">馆</span>'
            ),
        )

    def test_added_punc(self):
        self.assertEqual(
            colorize_fuse(['图', '书', '馆', '。'], ['tú', 'shū', 'guǎn']),
            (
                '<span class="tone2">图</span>'
                '<span class="tone1">书</span>'
                '<span class="tone3">馆</span>'
            ),
        )

    @skip
    def test_missing_punc(self):
        self.assertEqual(
            colorize_fuse(
                ['没', '有', '是', '我', '第', '一', '次'],
                ['Méi', 'yǒu', ',', 'shì', 'wǒ', 'dì', 'yī', 'cì', '.'],
            ),
            (
                '<span class="tone2">没</span>'
                '<span class="tone3">有</span>，'
                '<span class="tone4">是</span>'
                '<span class="tone3">我</span>'
                '<span class="tone4">第</span>'
                '<span class="tone1">一</span>'
                '<span class="tone4">次</span>。'
            ),
        )

    def test_truncated_hanzi(self):
        """Given truncated hanzi, should still highlight correctly."""
        self.assertEqual(
            colorize_fuse(['图', '书'], ['tú', 'shū', 'guǎn']),
            '<span class="tone2">图</span><span class="tone1">书</span>',
        )

    def test_truncated_transcript(self):
        """Given truncated transcription, should truncate hanzi."""
        self.assertEqual(
            colorize_fuse(['图', '书', '馆'], ['tú', 'shū']),
            '<span class="tone2">图</span><span class="tone1">书</span>',
        )

    def test_mixed_english_chinese(self):
        self.assertEqual(
            colorize_fuse(['Brian', '的'], ['Brian', 'de']),
            '<span class="tone5">Brian</span><span class="tone5">的</span>',
        )
