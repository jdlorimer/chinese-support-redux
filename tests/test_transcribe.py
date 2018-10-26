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

from unittest import skip
from unittest.mock import Mock

from . import ChineseTests


class AccentuateTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.transcribe import accentuate
        self.func = accentuate
        self.config.options = {'transcription': 'Pinyin'}

    def test_pinyin(self):
        self.assertEqual(self.func(['xian4']), ['xiàn'])
        self.assertEqual(self.func(['xian4 zai4']), ['xiàn zài'])
        self.assertEqual(
            self.func(['hen3', 'gao1 xing4']),
            ['hěn', 'gāo xìng']
        )

    def test_cantonese(self):
        self.config.options = {'transcription': 'Cantonese'}
        self.assertEqual(self.func(['xian4']), ['xian4'])


class SeparateTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.transcribe import separate
        self.func = separate
        self.config.options = {'transcription': 'Pinyin'}

    def test_tone_mark(self):
        self.assertEqual(self.func('xiànzài'), ['xiàn zài'])

    def test_tone_number(self):
        self.assertEqual(self.func('xian4zai4'), ['xian4 zai4'])

    def test_muliple_words(self):
        self.assertEqual(
            self.func('hěn gāoxìng'), ['hěn', 'gāo xìng'])

    def test_multisyllabic_words(self):
        self.assertEqual(self.func('túshūguǎn'), ['tú shū guǎn'])

    def test_ungrouped(self):
        self.assertEqual(
            self.func('hěn gāoxìng', grouped=False),
            ['hěn', 'gāo', 'xìng']
        )

    @skip
    def test_you_er_yuan(self):
        self.assertEqual(self.func("yòu'éryuán"), ["yòu ér yuán"])


class TranscribeTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.transcribe import transcribe
        self.func = transcribe

    def test_single_word(self):
        self.dictionary.get_pinyin = Mock(return_value='nǐ')
        self.assertEqual(self.func(['你'], 'Pinyin'), ['nǐ'])

    def test_multiple_words(self):
        self.dictionary.get_pinyin = Mock(side_effect=['tú shū', 'guǎn'])
        self.assertEqual(
            self.func(['图书', '馆'], 'Pinyin'), ['tú shū', 'guǎn'])

    def test_no_chinese(self):
        self.assertEqual(self.func(['foo'], 'Pinyin'), [])

    def test_some_chinese(self):
        self.dictionary.get_pinyin = Mock(return_value='nǐ')
        self.assertEqual(self.func(['foo', '你'], 'Pinyin'), ['nǐ'])


class NoAccentsTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.transcribe import no_accents
        self.func = no_accents

    def test_split_words(self):
        self.assertEqual(self.func('hàn yǔ pīn yīn'), 'han4 yu3 pin1 yin1')

    @skip
    def test_joined_words(self):
        self.assertEqual(self.func('hànyǔ pīnyīn'), 'han4yu3 pin1yin1')

    def test_tone_number(self):
        self.assertEqual(self.func('pin1 yin1'), 'pin1 yin1')

    def test_tone_superscript(self):
        self.assertEqual(self.func('pin¹ yin¹'), 'pin¹ yin¹')


class NoToneTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.transcribe import no_tone
        self.func = no_tone

    def test_tone_number(self):
        self.assertEqual(self.func('ni3'), 'ni')

    def test_tone_superscript(self):
        self.assertEqual(self.func('ni³'), 'ni')

    def test_tone_mark(self):
        self.assertEqual(self.func('má'), 'ma')

    def test_tone_styling(self):
        self.assertEqual(self.func('<span class="tone2">má</span>'), 'ma')
