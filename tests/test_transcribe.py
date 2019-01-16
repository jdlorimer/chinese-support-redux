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

from unittest import skip
from unittest.mock import patch

from chinese.transcribe import (
    accentuate,
    get_tone_number_pinyin,
    is_sentence,
    no_tone,
    replace_tone_marks,
    split_transcript,
    tone_number,
    transcribe,
)
from tests import Base


class Accentuate(Base):
    def test_pinyin(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(accentuate(['xian4']), ['xiàn'])
            self.assertEqual(accentuate(['xian4 zai4']), ['xiàn zài'])
            self.assertEqual(
                accentuate(['hen3', 'gao1 xing4']), ['hěn', 'gāo xìng']
            )

    def test_cantonese(self):
        with patch(
            'chinese.transcribe.config', {'transcription': 'Cantonese'}
        ):
            self.assertEqual(accentuate(['xian4']), ['xian4'])


class SeparateTrans(Base):
    def test_tone_mark(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(split_transcript('xiànzài'), ['xiàn zài'])

    def test_tone_number(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(split_transcript('xian4zai4'), ['xian4 zai4'])

    def test_muliple_words(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(
                split_transcript('hěn gāoxìng'), ['hěn', 'gāo xìng']
            )

    def test_multisyllabic_words(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(split_transcript('túshūguǎn'), ['tú shū guǎn'])

    def test_ungrouped(self):
        with patch('chinese.transcribe.config', {'transcription': 'Pinyin'}):
            self.assertEqual(
                split_transcript('hěn gāoxìng', grouped=False),
                ['hěn', 'gāo', 'xìng'],
            )

    @skip
    def test_apostrophe(self):
        self.assertEqual(
            split_transcript("yīlù píng'ān"), ['yī lù', 'píng ān']
        )

    @skip
    def test_you_er_yuan(self):
        self.assertEqual(split_transcript("yòu'éryuán"), ["yòu ér yuán"])

    def test_punctuation(self):
        self.assertEqual(
            split_transcript('Méiyǒu, méiyǒu.'),
            ['Méi yǒu', ',', 'méi yǒu', '.'],
        )
        self.assertEqual(
            split_transcript('Méi yǒu, méi yǒu.', grouped=False),
            ['Méi', 'yǒu', ',', 'méi', 'yǒu', '.'],
        )
        self.assertEqual(
            split_transcript('(méi) yǒu', grouped=False),
            ['(', 'méi', ')', 'yǒu'],
        )


class Transcribe(Base):
    def test_single_word(self):
        self.assertEqual(transcribe(['你'], 'Pinyin'), ['nǐ'])

    def test_multiple_words(self):
        self.assertEqual(transcribe(['图书', '馆'], 'Pinyin'), ['tú shū', 'guǎn'])

    def test_no_chinese(self):
        self.assertEqual(transcribe(['foo'], 'Pinyin'), [])

    def test_mixed_english_chinese(self):
        self.assertEqual(transcribe(['foo', '你'], 'Pinyin'), ['foo', 'nǐ'])
        self.assertEqual(transcribe(['Brian的'], 'Pinyin'), ['Brian de'])

    def test_bopomofo(self):
        self.assertEqual(transcribe(['你'], 'Bopomofo'), ['ㄋㄧˇ'])

    def test_punctuation_retained_converted(self):
        self.assertEqual(
            transcribe(['没有', '，', '没有', '。'], 'Pinyin'),
            ['méi yǒu', ',', 'méi yǒu', '.'],
        )

    def test_grouped_chars(self):
        self.assertEqual(
            transcribe(['你', '什么', '时候', '能', '来', '？']),
            ['nǐ', 'shén me', 'shí hou', 'néng', 'lái', '？'],
        )

    def test_ungrouped_chars(self):
        self.assertEqual(
            transcribe(['你什么时候能来？']), ['nǐ shén me shí hou néng lái ？']
        )
        self.assertEqual(transcribe(['我要喝湯！']), ['wǒ yào hē tāng ！'])

    def test_punctuation_irrelevant(self):
        self.assertEqual(
            transcribe(['我要喝湯'])[0] + ' ！', transcribe(['我要喝湯！'])[0]
        )


class ReplaceToneMarks(Base):
    def test_split_syllables(self):
        self.assertEqual(
            replace_tone_marks(['hàn', 'yǔ', 'pīn', 'yīn']),
            ['han4', 'yu3', 'pin1', 'yin1'],
        )

    def test_joined_syllables_spaced(self):
        self.assertEqual(
            replace_tone_marks(['hàn yǔ', 'pīn yīn']),
            ['han4 yu3', 'pin1 yin1'],
        )

    def test_joined_syllables_unspaced(self):
        self.assertEqual(
            replace_tone_marks(['hànyǔ', 'pīnyīn']), ['han4 yu3', 'pin1 yin1']
        )

    def test_tone_number(self):
        self.assertEqual(
            replace_tone_marks(['pin1', 'yin1']), ['pin1', 'yin1']
        )

    def test_tone_superscript(self):
        self.assertEqual(
            replace_tone_marks(['pin¹', 'yin¹']), ['pin¹', 'yin¹']
        )

    def test_neutral_tone(self):
        self.assertEqual(replace_tone_marks(['ne']), ['ne5'])

    def test_umlaut(self):
        self.assertEqual(replace_tone_marks(['lǘ']), ['lü2'])

    def test_ruby(self):
        self.assertEqual(replace_tone_marks(['你[nǐ]']), ['你[ni3]'])


class NoTone(Base):
    def test_tone_number(self):
        self.assertEqual(no_tone('ni3'), 'ni')

    def test_tone_superscript(self):
        self.assertEqual(no_tone('ni³'), 'ni')

    def test_tone_mark(self):
        self.assertEqual(no_tone('má'), 'ma')

    def test_tone_styling_spaced(self):
        self.assertEqual(
            no_tone(
                '<span class="tone2">méi</span> <span class="tone3">yǒu</span>'
            ),
            'mei you',
        )

    @skip
    def test_tone_styling_unspaced(self):
        self.assertEqual(
            no_tone(
                '<span class="tone2">méi</span><span class="tone3">yǒu</span>'
            ),
            'meiyou',
        )

    def test_ruby(self):
        self.assertEqual(no_tone('你[nǐ]'), '你[ni]')


class ToneNumber(Base):
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


class IsSentence(Base):
    def test_length(self):
        self.assertFalse(is_sentence('你' * 6))
        self.assertTrue(is_sentence('你' * 7))

    def test_punc(self):
        self.assertFalse(is_sentence('你'))
        self.assertTrue(is_sentence('你。'))


class GetToneNumberPinyin(Base):
    def test_get_tone_number_pinyin(self):
        self.assertEqual(get_tone_number_pinyin('hàn yǔ'), 'han yu3')
        self.assertEqual(get_tone_number_pinyin('hànyǔ'), 'hanyu3')
        self.assertEqual(get_tone_number_pinyin('hàn'), 'han4')
