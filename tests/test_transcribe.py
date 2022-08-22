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
        self.assertEqual(accentuate(['xian4'], 'pinyin'), ['xiàn'])
        self.assertEqual(accentuate(['xian4 zai4'], 'pinyin'), ['xiàn zài'])
        self.assertEqual(
            accentuate(['hen3', 'gao1 xing4'], 'pinyin'), ['hěn', 'gāo xìng']
        )

    def test_cantonese(self):
        self.assertEqual(accentuate(['xian4'], 'jyutping'), ['xian4'])


class SplitTranscript(Base):
    def test_tone_mark(self):
        self.assertEqual(split_transcript('xiànzài', 'pinyin'), ['xiàn zài'])

    def test_tone_number(self):
        self.assertEqual(
            split_transcript('xian4zai4', 'pinyin'), ['xian4 zai4']
        )

    def test_muliple_words(self):
        self.assertEqual(
            split_transcript('hěn gāoxìng', 'pinyin'), ['hěn', 'gāo xìng']
        )

    def test_multisyllabic_words(self):
        self.assertEqual(
            split_transcript('túshūguǎn', 'pinyin'), ['tú shū guǎn']
        )

    def test_ungrouped(self):
        self.assertEqual(
            split_transcript('hěn gāoxìng', 'pinyin', grouped=False),
            ['hěn', 'gāo', 'xìng'],
        )

    def test_apostrophe(self):
        self.assertEqual(
            split_transcript("yīlù píng'ān", 'pinyin'), ['yī lù', 'píng ān']
        )
        self.assertEqual(
            split_transcript("yòu'éryuán", 'pinyin'), ['yòu ér yuán']
        )

    def test_punctuation(self):
        self.assertEqual(
            split_transcript('Méiyǒu, méiyǒu.', 'pinyin'),
            ['Méi yǒu', ',', 'méi yǒu', '.'],
        )
        self.assertEqual(
            split_transcript('Méi yǒu, méi yǒu.', 'pinyin', grouped=False),
            ['Méi', 'yǒu', ',', 'méi', 'yǒu', '.'],
        )
        self.assertEqual(
            split_transcript('(méi) yǒu', 'pinyin', grouped=False),
            ['(', 'méi', ')', 'yǒu'],
        )

    def test_issue_79(self):
        self.assertEqual(split_transcript("xiá ài", 'pinyin'), ['xiá', 'ài'])
        self.assertEqual(split_transcript("xiá'ài", 'pinyin'), ['xiá ài'])
        self.assertEqual(split_transcript("xiáài", 'pinyin'), ['xiá ài'])

    def test_regression_1(self):
        self.assertEqual(
            split_transcript('chuángdān', 'pinyin'), ['chuáng dān']
        )


class Transcribe(Base):
    def test_single_word(self):
        self.assertEqual(transcribe(['你'], 'pinyin', 'simp'), ['nǐ'])

    def test_multiple_words(self):
        self.assertEqual(
            transcribe(['图书', '馆'], 'pinyin', 'simp'), ['tú shū', 'guǎn']
        )

    def test_single_polyphone(self):
        self.assertEqual(transcribe(['说'], 'pinyin', 'simp'), ['shuō'])

    def test_single_zici_polyphone(self):
        self.assertEqual(transcribe(['分子'], 'pinyin', 'simp'), ['fēn zǐ'])

    def test_multiple_polyphones(self):
        self.assertEqual(
            transcribe(['你', '要', '说', '什么'], 'pinyin', 'simp'), ['nǐ', 'yào', 'shuō', 'shén me']
        )

    def test_multiple_zici_polyphones(self):
        self.assertEqual(
            transcribe(['重点', '分子', '便宜'], 'pinyin', 'simp'), ['zhòng diǎn', 'fēn zǐ', 'pián yi']
        )

    def test_no_chinese(self):
        self.assertEqual(transcribe(['foo'], 'pinyin', 'simp'), [])

    def test_mixed_english_chinese(self):
        self.assertEqual(
            transcribe(['foo', '你'], 'pinyin', 'simp'), ['foo', 'nǐ']
        )
        self.assertEqual(
            transcribe(['Brian的'], 'pinyin', 'simp'), ['Brian de']
        )

    def test_bopomofo(self):
        self.assertEqual(transcribe(['你'], 'bopomofo', 'trad'), ['ㄋㄧˇ'])

    def test_punctuation_retained_converted(self):
        self.assertEqual(
            transcribe(['没有', '，', '没有', '。'], 'pinyin', 'simp'),
            ['méi yǒu', ',', 'méi yǒu', '.'],
        )

    def test_grouped_chars(self):
        self.assertEqual(
            transcribe(['你', '什么', '时候', '能', '来', '？'], 'pinyin', 'simp'),
            ['nǐ', 'shén me', 'shí hou', 'néng', 'lái', '？'],
        )

    def test_jyutping_words(self):
        self.assertEqual(transcribe(['上海'], 'jyutping', 'trad'), [None])
        self.assertEqual(
            transcribe(['上海人'], 'jyutping', 'trad'), ['soeng6 hoi2 jan4']
        )

    def test_jyutping_sentence(self):
        self.assertEqual(
            transcribe(['對唔住', '，', '我', '唔係', '李', '太'], 'jyutping', 'trad'),
            ['deoi3 m4 zyu6', ',', None, 'm4 hai6', 'lei5', 'taai3'],
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

    def test_composed_diacritics(self):
        self.assertEqual(
            replace_tone_marks(['shén', 'yùn']), ['shen2', 'yun4']
        )

    def test_decomposed_diacritics(self):
        self.assertEqual(
            replace_tone_marks(['shén', 'yùn']), ['shen2', 'yun4']
        )

    def test_issue_79(self):
        self.assertEqual(replace_tone_marks(['xiá', 'ài']), ['xia2', 'ai4'])
        self.assertEqual(replace_tone_marks(['xiáài']), ['xia2 ai4'])


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
