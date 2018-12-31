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

from unittest.mock import MagicMock, patch

from chinese.behavior import (
    fill_all_defs,
    fill_color,
    fill_pinyin,
    fill_sound,
    fill_transcription,
)
from tests import ChineseTest


class FillSound(ChineseTest):
    def test_missing_sound(self):
        note = dict.fromkeys(
            ['Sound', 'Sound (Mandarin)', 'Sound (Cantonese)'], ''
        )
        with patch(
            'chinese.behavior.sound',
            MagicMock(side_effect=['foo', 'bar', 'baz']),
        ):
            self.assertEqual(fill_sound('上海', note), (3, 0))
        self.assertEqual(note['Sound'], 'foo')
        self.assertEqual(note['Sound (Mandarin)'], 'bar')
        self.assertEqual(note['Sound (Cantonese)'], 'baz')

    def test_existing_sound(self):
        note = {
            'Sound': 'qux',
            'Sound (Mandarin)': 'qux',
            'Sound (Cantonese)': 'qux',
        }
        with patch(
            'chinese.behavior.sound',
            MagicMock(side_effect=['foo', 'bar', 'baz']),
        ):
            self.assertEqual(fill_sound('上海', note), (0, 0))
        self.assertEqual(note['Sound'], 'qux')
        self.assertEqual(note['Sound (Mandarin)'], 'qux')
        self.assertEqual(note['Sound (Cantonese)'], 'qux')


class FillTranscription(ChineseTest):
    def test_ungrouped_chars(self):
        hanzi = '没有，是我第一次来上海旅游。'
        note = {'Reading': ''}
        self.assertEqual(fill_transcription(hanzi, note), 1)
        self.assertEqual(
            note['Reading'],
            (
                '<span class="tone2">méi</span> '
                '<span class="tone3">yǒu</span> , '
                '<span class="tone4">shì</span> '
                '<span class="tone3">wǒ</span> '
                '<span class="tone4">dì</span> '
                '<span class="tone1">yī</span> '
                '<span class="tone4">cì</span> '
                '<span class="tone2">lái</span> '
                '<span class="tone3">shǎng</span> '
                '<span class="tone3">hǎi</span> '
                '<span class="tone3">lǚ</span> '
                '<span class="tone2">yóu</span> . '
                '<!-- mei you , shi wo di yi ci lai shang hai lü you . -->'
            ),
        )

    def test_grouped_chars(self):
        hanzi = '没有， 是 我 第一次 来 上海 旅游。'
        note = {'Reading': ''}
        self.assertEqual(fill_transcription(hanzi, note), 1)
        self.assertEqual(
            note['Reading'],
            (
                '<span class="tone2">méi</span>'
                '<span class="tone3">yǒu</span> , '
                '<span class="tone4">shì</span> '
                '<span class="tone3">wǒ</span> '
                '<span class="tone4">dì</span>'
                '<span class="tone1">yī</span>'
                '<span class="tone4">cì</span> '
                '<span class="tone2">lái</span> '
                '<span class="tone4">shàng</span>'
                '<span class="tone3">hǎi</span> '
                '<span class="tone3">lǚ</span>'
                '<span class="tone2">yóu</span> . '
                '<!-- meiyou , shi wo diyici lai shanghai lüyou . -->'
            ),
        )


class FillColor(ChineseTest):
    def test_ungrouped_chars_grouped_pinyin(self):
        note = {
            'Color': '',
            'Reading': 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.',
        }
        fill_color('没有，是我第一次来上海旅游。', note)
        self.assertEqual(
            note['Color'],
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

    def test_chars_no_pinyin(self):
        """Should not generate color output if no available reading."""

        note = {'Color': '', 'Reading': ''}
        note = dict.fromkeys(['Color', 'Reading'], '')
        for s in ['没有', '没 有', '没有。']:
            fill_color(s, note)
            self.assertEqual(note['Color'], '')

    def test_mismatched_inputs(self):
        note = {
            'Color': '',
            'Reading': 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.',
        }
        fill_color('（没有，）是我第一次来上海旅游。', note)
        self.assertEqual(
            note['Color'],
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


class FillAllDefs(ChineseTest):
    def test_no_classifier_field(self):
        note = dict.fromkeys(['Meaning', 'English', 'German', 'French'], '')
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        english = ' \tlibrary\n<br><br>Cl: ' + classifier
        german = ' \tBibliothek (S, Lit\n<br><br>Cl: ' + classifier
        french = ' \tbibliothèque\n<br><br>Cl: ' + classifier
        self.assertEqual(fill_all_defs('图书馆', note), 4)
        self.assertEqual(note['Meaning'], english)
        self.assertEqual(note['English'], english)
        self.assertEqual(note['German'], german)
        self.assertEqual(note['French'], french)

    def test_classifier_field(self):
        note = {'Meaning': '', 'Classifier': ''}
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        self.assertEqual(fill_all_defs('图书馆', note), 1)
        self.assertEqual(note['Meaning'], ' \tlibrary\n<br>')
        self.assertEqual(note['Classifier'], classifier)


class FillPinyin(ChineseTest):
    def test_two_character_word(self):
        note = {'Pinyin': ''}
        self.assertEqual(fill_pinyin('中国', note), 1)
        self.assertEqual(
            note['Pinyin'],
            (
                '<span class="tone1">zhōng</span>'
                '<span class="tone2">guó</span> '
                '<!-- zhongguo -->'
            ),
        )
        note = {'Pinyin': ''}
        self.assertEqual(fill_pinyin('上海', note), 1)
        self.assertEqual(
            note['Pinyin'],
            (
                '<span class="tone4">shàng</span>'
                '<span class="tone3">hǎi</span> '
                '<!-- shanghai -->'
            ),
        )
