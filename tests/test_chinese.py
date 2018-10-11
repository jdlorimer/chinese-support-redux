from unittest import skip

from . import ChineseTests


# consumers: colorize, ruby
class AccentuatePinyinTests(ChineseTests):
    def test_accentuate_pinyin(self):
        from chinese.edit_functions import accentuate_pinyin
        self.assertEqual(accentuate_pinyin(['xian4'], True), ['xiàn'])
        self.assertEqual(accentuate_pinyin(['xian4 zai4'], True), ['xiàn zài'])
        self.assertEqual(
            accentuate_pinyin(['hen3', 'gao1 xing4'], True),
            ['hěn', 'gāo xìng']
        )


# consumers: accentuate_pinyin, colorize
class SeparatePinyinTests(ChineseTests):
    def setUp(self):
        super().setUp()
        from chinese.edit_functions import separate_pinyin
        self.func = separate_pinyin

    def test_tone_mark(self):
        self.assertEqual(self.func('xiànzài', force=True), ['xiàn zài'])

    def test_tone_number(self):
        self.assertEqual(self.func('xian4zai4', force=True), ['xian4 zai4'])

    def test_muliple_words(self):
        self.assertEqual(
            self.func('hěn gāoxìng', force=True), ['hěn', 'gāo xìng'])

    def test_multisyllabic_words(self):
        self.assertEqual(self.func('túshūguǎn', force=True), ['tú shū guǎn'])

    @skip
    def test_er_yuan(self):
        self.assertEqual(self.func("yòu'éryuán", force=True), ["yòu ér yuán"])


# consumers: colorize
class TranscribeTests(ChineseTests):
    def test_transcribe(self):
        from chinese.edit_functions import transcribe
        self.assertEqual(transcribe(['你'], 'Pinyin'), ['nǐ'])
        self.assertEqual(
            transcribe(['图书', '馆'], 'Pinyin'), ['tú shū', 'guǎn'])
