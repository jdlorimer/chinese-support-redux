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

from unittest.mock import MagicMock, patch
from unittest import skip

from chinese.behavior import (
    fill_all_defs,
    fill_all_rubies,
    fill_classifier,
    fill_bopomofo,
    fill_color,
    fill_simp,
    fill_sound,
    fill_trad,
    fill_transcript,
    update_fields,
)
from tests import Base


class FillSound(Base):
    def test_missing_sound(self):
        note = dict.fromkeys(['Sound (Mandarin)', 'Sound (Cantonese)'], '')
        with patch(
            'chinese.behavior.sound',
            MagicMock(side_effect=['foo', 'bar', 'baz']),
        ):
            self.assertEqual(fill_sound('上海', note), (1, 0))
        self.assertEqual(note['Sound (Mandarin)'], 'foo')
        self.assertEqual(note['Sound (Cantonese)'], '')

    def test_existing_sound(self):
        note = {'Sound (Mandarin)': 'qux', 'Sound (Cantonese)': 'qux'}
        with patch(
            'chinese.behavior.sound',
            MagicMock(side_effect=['foo', 'bar', 'baz']),
        ):
            self.assertEqual(fill_sound('上海', note), (0, 0))
        self.assertEqual(note['Sound (Mandarin)'], 'qux')
        self.assertEqual(note['Sound (Cantonese)'], 'qux')


class FillTranscript(Base):
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
                ['Pinyin', 'Pinyin (Taiwan)', 'Cantonese'], ''
            )
            fill_transcript(hanzi, note)
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
        hanzi = '上海'
        note = dict.fromkeys(
            ['Bopomofo', 'Cantonese', 'Pinyin (Taiwan)', 'Pinyin'], ''
        )
        self.assertEqual(fill_transcript(hanzi, note), 4)
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

    def test_mixed_english_chinese(self):
        note = dict.fromkeys(['Pinyin'], '')
        fill_transcript('Brian的', note)
        self.assertEqual(
            note['Pinyin'],
            '<span class="tone5">Brian</span> '
            '<span class="tone5">de</span> '
            '<!-- Brian de -->',
        )


class FillBopomofo(Base):
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

    def test_grouped_pinyin(self):
        note = dict.fromkeys(['Bopomofo'], '')
        note['Pinyin'] = 'shényùn'
        fill_bopomofo('神韻', note)
        self.assertEqual(
            note['Bopomofo'],
            '<span class="tone2">ㄕㄣˊ</span>'
            '<span class="tone4">ㄩㄣˋ</span>'
            ' <!-- ㄕㄣˊㄩㄣˋ -->',
        )

    def test_ungrouped_pinyin(self):
        note = dict.fromkeys(['Bopomofo'], '')
        note['Pinyin'] = 'shen4 yun4'
        fill_bopomofo('神韻', note)
        self.assertEqual(
            note['Bopomofo'],
            '<span class="tone2">ㄕㄣˊ</span>'
            '<span class="tone4">ㄩㄣˋ</span>'
            ' <!-- ㄕㄣˊㄩㄣˋ -->',
        )


class UpdateFields(Base):
    def test_all(self):
        class Note(dict):
            def model(self):
                return ''

        expected = {
            'Hanzi': '床单',
            'Hanzi (Color)': '<span class="tone2">床</span><span class="tone1">单</span>',
            'Classifier': (
                '<span class="tone2"><ruby>條<rt>tiáo</rt></ruby></span>|'
                '<span class="tone2">条</span>, '
                '<span class="tone4"><ruby>件<rt>jiàn</rt></ruby></span>, '
                '<span class="tone1"><ruby>張<rt>zhāng</rt></ruby></span>|'
                '<span class="tone1">张</span>, '
                '<span class="tone2"><ruby>床<rt>chuáng</rt></ruby></span>'
            ),
            'Pinyin': '<span class="tone2">chuáng</span><span class="tone1">dān</span> <!-- chuang dan -->',
            'Pinyin (Taiwan)': '<span class="tone2">chuáng</span><span class="tone1">dān</span> <!-- chuang dan -->',
            'Bopomofo': '<span class="tone2">ㄔㄨㄤˊ</span><span class="tone1">ㄉㄢ</span> <!-- ㄔㄨㄤˊㄉㄢ -->',
            'Jyutping': '',
            # FIXME
            'English': ' \tbed sheet\n<br>',
            'German': ' \tLaken, Bettlaken, Betttuch (u.E.) (S)\n<br>',
            'French': ' \tdrap de lit\n<br>',
            'Ruby (Pinyin)': '<span class="tone2"><ruby>床<rt>chuáng</rt></ruby></span><span class="tone1"><ruby>单<rt>dān</rt></ruby></span>',
            'Ruby (Taiwan Pinyin)': '<span class="tone2"><ruby>床<rt>chuáng</rt></ruby></span><span class="tone1"><ruby>单<rt>dān</rt></ruby></span>',
            'Ruby (Bopomofo)': '<span class="tone2"><ruby>床<rt>ㄔㄨㄤˊ</rt></ruby></span><span class="tone1"><ruby>单<rt>ㄉㄢ</rt></ruby></span>',
            'Ruby (Jyutping)': '',
            'Silhouette': '_ _',
            'Sound (Mandarin)': '[sound:床单_google_zh-cn.mp3]',
            'Sound (Cantonese)': '',
        }
        fields = expected.keys()
        note = Note.fromkeys(fields, '')
        note['Hanzi'] = '床单'
        update_fields(note, 'Hanzi', fields)
        self.assertEqual(expected, note)

    def test_no_sound(self):
        with patch('chinese.sound.download') as m:
            update_fields(
                {'Hanzi': '床单', 'Pinyin': ''}, 'Hanzi', ('Pinyin', 'Hanzi')
            )
            m.assert_not_called()


class FillAllRubies(Base):
    def test_words(self):
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
        note['Pinyin'] = 'shànghǎi'
        note['Pinyin (Taiwan)'] = 'shànghǎi'
        note['Bopomofo'] = 'ㄕㄤˋㄏㄞˇ'
        note['Cantonese'] = 'soeng6 hoi2'
        pinyin_ruby = (
            '<span class="tone4"><ruby>上<rt>shàng</rt></ruby></span>'
            '<span class="tone3"><ruby>海<rt>hǎi</rt></ruby></span>'
        )
        self.assertEqual(fill_all_rubies("上海", note), None)
        self.assertEqual(note["Ruby"], pinyin_ruby)
        self.assertEqual(note["Ruby (Pinyin)"], pinyin_ruby)
        self.assertEqual(note["Ruby (Taiwan Pinyin)"], pinyin_ruby)
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


class FillColor(Base):
    def test_ungrouped_chars_grouped_pinyin(self):
        note = dict.fromkeys(['Color Hanzi'], '')
        note['Pinyin'] = 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.'
        fill_color('没有，是我第一次来上海旅游。', note)
        self.assertEqual(
            note['Color Hanzi'],
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

        note = dict.fromkeys(['Color Hanzi', 'Pinyin'], '')
        for s in ['没有', '没 有', '没有。']:
            fill_color(s, note)
            self.assertEqual(note['Color Hanzi'], '')

    def test_mismatched_inputs(self):
        note = dict.fromkeys(['Color Hanzi'], '')
        note['Pinyin'] = 'Méiyǒu, shì wǒ dìyīcì lái Shànghǎi lǚyóu.'
        fill_color('（没有，）是我第一次来上海旅游。', note)
        self.assertEqual(
            note['Color Hanzi'],
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

    def test_mixed_english_chinese(self):
        note = dict.fromkeys(['Color Hanzi', 'Pinyin'], '')
        note['Pinyin'] = 'Brian de'
        fill_color('Brian的', note)
        self.assertEqual(
            note['Color Hanzi'],
            '<span class="tone5">Brian</span><span class="tone5">的</span>',
        )


class FillAllDefs(Base):
    def test_no_classifier_field(self):
        note = dict.fromkeys(['English', 'German', 'French'], '')
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        english = ' \tlibrary\n<br><br>Cl: ' + classifier
        german = ' \tBibliothek (S, Lit)\n<br><br>Cl: ' + classifier
        french = ' \tbibliothèque (lieu)\n<br><br>Cl: ' + classifier
        self.assertEqual(fill_all_defs('图书馆', note), 3)
        self.assertEqual(note['English'], english)
        self.assertEqual(note['French'], french)
        self.assertEqual(note['German'], german)

    def test_classifier_field(self):
        note = dict.fromkeys(['Classifier', 'English'], '')
        self.assertEqual(fill_all_defs('图书馆', note), 1)
        self.assertEqual(note['Classifier'], '')
        self.assertEqual(note['English'], ' \tlibrary\n<br>')


class FillClassifier(Base):
    def test_fill_classifier(self):
        note = {'Classifier': ''}
        classifier = (
            '<span class="tone1"><ruby>家<rt>jiā</rt></ruby></span>, '
            '<span class="tone4"><ruby>個<rt>gè</rt></ruby></span>|'
            '<span class="tone4">个</span>'
        )
        self.assertEqual(fill_classifier('图书馆', note), 1)
        self.assertEqual(note['Classifier'], classifier)


class FillSimplifiedTraditionalHanzi(Base):
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
