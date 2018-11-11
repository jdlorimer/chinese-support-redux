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
from unittest.mock import patch

from . import ChineseTests

from chinese.transcribe import (
    accentuate,
    no_tone,
    replace_tone_marks,
    separate,
    tone_number,
    transcribe
)


class AccentuateTests(ChineseTests):
    def test_pinyin(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(accentuate(['xian4']), ['xiàn'])
            self.assertEqual(accentuate(['xian4 zai4']), ['xiàn zài'])
            self.assertEqual(
                accentuate(['hen3', 'gao1 xing4']),
                ['hěn', 'gāo xìng']
            )

    def test_cantonese(self):
        with patch('chinese.transcribe.config', {'transcription': 'Cantonese'}):
            self.assertEqual(accentuate(['xian4']), ['xian4'])


class SeparateTests(ChineseTests):
    def test_tone_mark(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(separate('xiànzài'), ['xiàn zài'])

    def test_tone_number(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(separate('xian4zai4'), ['xian4 zai4'])

    def test_muliple_words(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(separate('hěn gāoxìng'), ['hěn', 'gāo xìng'])

    def test_multisyllabic_words(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(separate('túshūguǎn'), ['tú shū guǎn'])

    def test_ungrouped(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(
                separate('hěn gāoxìng', grouped=False),
                ['hěn', 'gāo', 'xìng']
            )

    def test_apostrophe(self):
        self.assertEqual(separate("yīlù píng'ān"), ['yī lù', 'píng ān'])

    @skip
    def test_you_er_yuan(self):
        self.assertEqual(separate("yòu'éryuán"), ["yòu ér yuán"])


class TranscribeTests(ChineseTests):
    def test_single_word(self):
        self.assertEqual(transcribe(['你'], 'Pinyin'), ['nǐ'])

    def test_multiple_words(self):
        self.assertEqual(
            transcribe(['图书', '馆'], 'Pinyin'), ['tú shū', 'guǎn'])

    def test_no_chinese(self):
        self.assertEqual(transcribe(['foo'], 'Pinyin'), [])

    def test_some_chinese(self):
        self.assertEqual(transcribe(['foo', '你'], 'Pinyin'), ['nǐ'])


class ReplaceToneMarksTests(ChineseTests):
    def test_split_words(self):
        self.assertEqual(
            replace_tone_marks('hàn yǔ pīn yīn'),
            'han4 yu3 pin1 yin1'
        )

    @skip
    def test_joined_words(self):
        self.assertEqual(replace_tone_marks('hànyǔ pīnyīn'), 'han4yu3 pin1yin1')

    def test_tone_number(self):
        self.assertEqual(replace_tone_marks('pin1 yin1'), 'pin1 yin1')

    def test_tone_superscript(self):
        self.assertEqual(replace_tone_marks('pin¹ yin¹'), 'pin¹ yin¹')

    def test_neutral_tone(self):
        self.assertEqual(replace_tone_marks('ne'), 'ne5')

    def test_umlaut(self):
        self.assertEqual(replace_tone_marks('lǘ'), 'lü2')


class NoToneTests(ChineseTests):
    def test_tone_number(self):
        self.assertEqual(no_tone('ni3'), 'ni')

    def test_tone_superscript(self):
        self.assertEqual(no_tone('ni³'), 'ni')

    def test_tone_mark(self):
        self.assertEqual(no_tone('má'), 'ma')

    def test_tone_styling(self):
        self.assertEqual(no_tone('<span class="tone2">má</span>'), 'ma')


class ToneNumberTests(ChineseTests):
    def test_tone_number(self):
        self.assertEqual(tone_number('ni3'), '3')

    def test_tone_superscript(self):
        self.assertEqual(tone_number('ni³'), '3')

    def test_tone_mark(self):
        self.assertEqual(tone_number('nǐ'), '3')

    def test_tone_styling(self):
        self.assertEqual(tone_number('<span class="tone2">nǐ</span>'), '3')

    def test_bopomofo(self):
        self.assertEqual(tone_number('ㄧㄣ'), '1')
        self.assertEqual(tone_number('ㄖㄨˊ'), '2')
        self.assertEqual(tone_number('ㄋㄧˇ'), '3')
        self.assertEqual(tone_number('ㄓㄨˋ'), '4')
        self.assertEqual(tone_number('ㄋㄜ˙'), '5')
