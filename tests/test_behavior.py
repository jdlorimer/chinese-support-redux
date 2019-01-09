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
    fill_all_rubies,
    fill_bopomofo,
    fill_color,
    fill_simp,
    fill_sound,
    fill_trad,
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
    expected_pinyin = (
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
        '<!-- mei you , shi wo di yi ci lai shang hai lü you . -->'
    )

    def test_sentences(self):
        for hanzi in ['没有，是我第一次来上海旅游。', '没有， 是 我 第一次 来 上海 旅游。']:
            note = dict.fromkeys(
                ['Reading', 'Pinyin', 'Pinyin (Taiwan)', 'Cantonese'], ''
            )
            fill_transcription(hanzi, note)
            self.assertEqual(note['Reading'], self.expected_pinyin)
            self.assertEqual(note['Pinyin'], self.expected_pinyin)
            self.assertEqual(note['Pinyin (Taiwan)'], self.expected_pinyin)
            # FIXME
            self.assertEqual(
                note['Cantonese'],
                '<span class="tone5">mut</span>6'
                '<span class="tone5">jau5</span>|'
                '<span class="tone5">jau</span>6 , '
                '<span class="tone5">si</span>6 '
                '<span class="tone5">ngo5</span> '
                '<span class="tone5">dai</span>6'
                '<span class="tone1">jat1</span>'
                '<span class="tone3">ci3</span> '
                '<span class="tone4">loi4</span> '
                '<span class="tone5">soeng5</span>|'
                '<span class="tone5">soeng</span>6'
                '<span class="tone2">hoi2</span> '
                '<span class="tone5">leoi5</span>'
                '<span class="tone4">jau4</span> . '
                '<!-- mut 6 jau |5 jau 6 , '
                'si 6 ngo dai 6 jatci loisoeng |5 soeng 6 hoileoijau . -->',
            )

    def test_words(self):
        # TODO: '中国'
        for hanzi in ['上海']:
            note = dict.fromkeys(
                [
                    'Bopomofo',
                    'Cantonese',
                    'Pinyin (Taiwan)',
                    'Pinyin',
                    'Reading',
                ],
                '',
            )
            # self.assertEqual(fill_transcription(hanzi, note), 6)
            fill_transcription(hanzi, note)
            self.assertEqual(
                note['Bopomofo'],
                (
                    '<span class="tone4">ㄕㄤˋ</span>'
                    '<span class="tone3">ㄏㄞˇ</span> '
                    '<!-- ㄕㄤˋㄏㄞˇ -->'
                ),
            )
            # FIXME
            self.assertEqual(
                note['Cantonese'],
                '<span class="tone5">soeng5</span>|'
                '<span class="tone5">soeng</span>6'
                '<span class="tone2">hoi2</span> '
                '<!-- soeng |5 soeng 6 hoi -->',
            )
            pinyin = (
                '<span class="tone4">shàng</span>'
                '<span class="tone3">hǎi</span> '
                '<!-- shang hai -->'
            )
            self.assertEqual(note['Pinyin (Taiwan)'], pinyin)
            self.assertEqual(note['Pinyin'], pinyin)
            self.assertEqual(note['Reading'], pinyin)


class FillBopomofo(ChineseTest):
    expected = (
        '<span class="tone2">ㄇㄟˊ</span>'
        '<span class="tone3">ㄧㄡˇ</span> , '
        '<span class="tone4">ㄕˋ</span> '
        '<span class="tone3">ㄨㄛˇ</span> '
        '<span class="tone4">ㄉㄧˋ</span>'
        '<span class="tone1">ㄧ</span>'
        '<span class="tone4">ㄘˋ</span> '
        '<span class="tone2">ㄌㄞˊ</span> '
        '<span class="tone4">ㄕㄤˋ</span>'
        '<span class="tone3">ㄏㄞˇ</span> '
        '<span class="tone3">ㄌㄩˇ</span>'
        '<span class="tone2">ㄧㄡˊ</span> . '
        '<!-- ㄇㄟˊㄧㄡˇ , ㄕˋㄨㄛˇㄉㄧˋㄧㄘˋㄌㄞˊㄕㄤˋㄏㄞˇㄌㄩˇㄧㄡˊ . -->'
    )

    def test_ungrouped_chars(self):
        note = dict.fromkeys(['Bopomofo'], '')
        fill_bopomofo('没有，是我第一次来上海旅游。', note)
        self.assertEqual(note['Bopomofo'], self.expected)

    def test_grouped_chars(self):
        note = dict.fromkeys(['Bopomofo'], '')
        fill_bopomofo('没有， 是 我 第一次 来 上海 旅游。', note)
        self.assertEqual(note['Bopomofo'], self.expected)


class FillAllRubies(ChineseTest):
    def test_words(self):
        for hanzi in ['上海']:
            note = dict.fromkeys(
                [
                    'Ruby',
                    'Ruby (Bopomofo)',
                    'Ruby (Cantonese)',
                    'Ruby (Pinyin)',
                    'Ruby (Taiwan Pinyin)',
                ],
                '',
            )
            note['Reading'] = 'shànghǎi'
            note['Pinyin'] = 'shànghǎi'
            note['Pinyin (Taiwan)'] = 'shànghǎi'
            note['Bopomofo'] = 'ㄕㄤˋ ㄏㄞˇ'  # FIXME: should not require spacing
            note['Cantonese'] = 'soeng6 hoi2'
            pinyin_ruby = (
                '<span class="tone4"><ruby>上<rt>shàng</rt></ruby></span>'
                '<span class="tone3"><ruby>海<rt>hǎi</rt></ruby></span>'
            )
            self.assertEqual(fill_all_rubies('上海', note), None)
            self.assertEqual(note['Ruby'], pinyin_ruby)
            self.assertEqual(note['Ruby (Pinyin)'], pinyin_ruby)
            self.assertEqual(note['Ruby (Taiwan Pinyin)'], pinyin_ruby)
            self.assertEqual(
                note['Ruby (Bopomofo)'],
                '<span class="tone4"><ruby>上<rt>ㄕㄤˋ</rt></ruby></span>'
                '<span class="tone3"><ruby>海<rt>ㄏㄞˇ</rt></ruby></span>',
            )
            # FIXME
            self.assertEqual(
                note['Ruby (Cantonese)'],
                '<span class="tone5"><ruby>上<rt>soeng</rt></ruby></span>'
                '<span class="tone6"><ruby>海<rt>6</rt></ruby></span>',
            )


class FillColor(ChineseTest):
    def test_ungrouped_chars_grouped_pinyin(self):
        note = dict.fromkeys(['Color'], '')
        note['Reading'] = 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.'
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

        note = dict.fromkeys(['Color', 'Reading'], '')
        for s in ['没有', '没 有', '没有。']:
            fill_color(s, note)
            self.assertEqual(note['Color'], '')

    def test_mismatched_inputs(self):
        note = dict.fromkeys(['Color'], '')
        note['Reading'] = 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.'
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
        note = dict.fromkeys(['English', 'German', 'French', 'Meaning'], '')
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        english = ' \tlibrary\n<br><br>Cl: ' + classifier
        # FIXME: truncated definition
        german = ' \tBibliothek (S, Lit\n<br><br>Cl: ' + classifier
        french = ' \tbibliothèque\n<br><br>Cl: ' + classifier
        self.assertEqual(fill_all_defs('图书馆', note), 4)
        self.assertEqual(note['English'], english)
        self.assertEqual(note['French'], french)
        self.assertEqual(note['German'], german)
        self.assertEqual(note['Meaning'], english)

    def test_classifier_field(self):
        note = dict.fromkeys(['Classifier', 'Meaning'], '')
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        self.assertEqual(fill_all_defs('图书馆', note), 1)
        self.assertEqual(note['Classifier'], classifier)
        self.assertEqual(note['Meaning'], ' \tlibrary\n<br>')


class FillSimplifiedTraditionalHanzi(ChineseTest):
    def test_hanzi_simplified_traditional_identical(self):
        hanzi = '人'
        note = {'Hanzi': hanzi, 'Simplified': '', 'Traditional': ''}
        fill_simp(hanzi, note)
        fill_trad(hanzi, note)
        self.assertEqual(note['Simplified'], '')
        self.assertEqual(note['Traditional'], '')

    def test_hanzi_traditional(self):
        hanzi = '简体字'
        note = {'Hanzi': hanzi, 'Simplified': '', 'Traditional': ''}
        fill_trad(hanzi, note)
        self.assertEqual(note['Simplified'], '')
        self.assertEqual(note['Traditional'], '簡體字')

    def test_hanzi_simplified(self):
        hanzi = '繁體字'
        note = {'Hanzi': hanzi, 'Simplified': '', 'Traditional': ''}
        fill_simp(hanzi, note)
        self.assertEqual(note['Simplified'], '繁体字')
        self.assertEqual(note['Traditional'], '')

    def test_hanzi_not_in_database(self):
        """
        Regression test for
        https://github.com/luoliyan/chinese-support-redux/issues/34. Should
        leave both Simplified and Traditional fields blank, not throw an
        exception.
        """
        hanzi = '𠂉'
        note = {'Hanzi': hanzi, 'Simplified': '', 'Traditional': ''}
        fill_simp(hanzi, note)
        fill_trad(hanzi, note)
        self.assertEqual(note['Simplified'], '')
        self.assertEqual(note['Traditional'], '')
