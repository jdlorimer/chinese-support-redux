# Copyright © 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright © 2017-2019 Joseph Lorimer <joseph@lorimer.me>
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

PINYIN_VOWELS = 'ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ'

PINYIN_INITIALS = 'zh|sh|ch|chu|[bpmfdtnlgkhjqxrzscwy]'

PINYIN_FINALS = (
    'i[āɑ̄áɑ́ɑ́ǎɑ̌àɑ̀aāáǎàa]ng|'
    'i[ōóǒòo]ng|'
    'u[āáǎàa]ng|'
    '[āáǎàa]ng|'
    '[ēéěèe]ng|'
    '[īíǐìi]ng|'
    '[ōóǒòo]ng|'
    '[ūúǔùu]ng|'
    'i[āáǎàa]n|'
    'i[āáǎàa]o|'
    'u[āáǎàa]i|'
    'u[āáǎàa]n|'
    'i[āáǎàa]|'
    'i[ēéěèe]|'
    'i[ōóǒòo]|'
    'i[ūúǔùu]|'
    'u[āáǎàa]|'
    'u[ēéěèe]|'
    'u[īíǐìi]|'
    'u[ōóǒòo]|'
    'v[ēéěèe]|'
    'ü[ēéěèe]|'
    '[āáǎàa]i|'
    '[āáǎàa]n|'
    '[āáǎàa]o|'
    '[ēéěèe]i|'
    '[ēéěèe]n|'
    '[ēéěèe]r|'
    '[īíǐìi]n|'
    '[ōóǒòo]u|'
    '[ūúǔùu]n|'
    '[āáǎàa]|'
    '[ēéěèe]|'
    '[īíǐìi]|'
    '[ōóǒòo]|'
    '[ūúǔùu]|'
    '[ǖǘǚǜüv]'
)

JYUTPING_INITIALS = 'ng|gw|kw|[bpmfdtnlgkhwzcsj]'

JYUTPING_FINALS = (
    'i|ip|it|ik|im|in|ing|iu|'
    'yu|yut|yun|'
    'u|up|ut|uk|um|un|ung|ui|'
    'e|ep|et|ek|em|en|eng|ei|eu|eot|eon|eoi|'
    'oe|oet|oek|oeng|oei|o|ot|ok|om|on|ong|oi|ou|'
    'ap|at|ak|am|an|ang|ai|au|aa|aap|aat|aak|aam|aan|aang|aai|aau|'
    'm|'
    'ng'
)

JYUTPING_STANDALONES = (
    'uk|'
    'ung|'
    'e|ei|'
    'oe|o|ok|om|on|ong|oi|ou|'
    'ap|at|ak|am|an|ang|ai|au|aa|aap|aat|aak|aam|aan|aang|aai|aau|'
    'm|'
    'ng'
)

HANZI_RANGE = r'\u3400-\u9fff'
BOPOMOFO_RANGE = r'\u3100-\u312F'

HANZI_REGEX = f'[{HANZI_RANGE}]'
BOPOMOFO_REGEX = f'([{BOPOMOFO_RANGE}]+[ˊˇˋ˙]?)'

TONE_SUPERS = '¹²³⁴⁵⁶⁷⁸⁹'
CMN_TONE_NUMBERS = '1-5¹²³⁴⁵'
YUE_TONE_NUMBERS = '1-7¹²³⁴⁵⁶⁷'
TONE_NUMBERS = f'{CMN_TONE_NUMBERS}{YUE_TONE_NUMBERS}'
TONE_NUM_REGEX = f'[{TONE_NUMBERS}]'

RUBY_REGEX = r'[%s]\[\s*([a-zü%s]+[%s]?)(.*?\])' % (
    HANZI_RANGE,
    PINYIN_VOWELS,
    TONE_NUMBERS,
)

HALF_RUBY_REGEX = f'([A-Za-zü{PINYIN_VOWELS}]+[{TONE_NUMBERS}]?)'

NOT_PINYIN_REGEX = (
    f"([^A-Za-zü{BOPOMOFO_RANGE}{PINYIN_VOWELS}{CMN_TONE_NUMBERS}ˊˇˋ˙'])"
)

TRANSCRIPT_REGEX_TEMPLATE = (
    "(({initials})({finals})[{tones}]?|([']?{standalones})[{tones}]?)"
)

PINYIN_REGEX = TRANSCRIPT_REGEX_TEMPLATE.format(
    initials=PINYIN_INITIALS,
    finals=PINYIN_FINALS,
    standalones=PINYIN_FINALS,
    tones=CMN_TONE_NUMBERS,
)

JYUTPING_REGEX = TRANSCRIPT_REGEX_TEMPLATE.format(
    initials=JYUTPING_INITIALS,
    finals=JYUTPING_FINALS,
    standalones=JYUTPING_STANDALONES,
    tones=YUE_TONE_NUMBERS,
)

COLOR_TEMPLATE = '<span class="tone{tone}">{chars}</span>'

COLOR_RUBY_TEMPLATE = ruby_template = (
    '<span class="tone{tone}">'
    '<ruby>{chars}<rt>{trans}</rt></ruby>'
    '</span>'
)

# early replacements
bopomofo_replacements = [
    ('jue', 'ㄐㄩㄝ'),
    ('lue', 'ㄌㄩㄝ'),
    ('nue', 'ㄋㄩㄝ'),
    ('que', 'ㄑㄩㄝ'),
    ('juan', 'ㄐㄩㄢ'),
    ('jun', 'ㄐㄩㄣ'),
    ('quan', 'ㄑㄩㄢ'),
    ('qun', 'ㄑㄩㄣ'),
    ('v', 'u:'),
    ('wong', 'ㄨㄥ'),
    ('wu', 'u'),
    ('w', 'u'),
    ('xue', 'ㄒㄩㄝ'),
    ('xuan', 'ㄒㄩㄢ'),
    ('xun', 'ㄒㄩㄣ'),
    ('yi', 'i'),
    ('you', 'ㄧㄡ'),
    ('yue', 'ㄩㄝ'),
    ('yuan', 'ㄩㄢ'),
    ('yun', 'ㄩㄣ'),
    ('yu', 'u:'),
    ('y', 'i'),
    ('ü', 'u:'),
]

bopomofo_special = [
    ('chi', 'ㄔ'),
    ('shi', 'ㄕ'),
    ('zhi', 'ㄓ'),
    ('ci', 'ㄘ'),
    ('ju', 'ㄐㄩ'),
    ('qu', 'ㄑㄩ'),
    ('er', 'ㄦ'),
    ('ri', 'ㄖ'),
    ('si', 'ㄙ'),
    ('xu', 'ㄒㄩ'),
    ('zi', 'ㄗ'),
]

bopomofo_initials = [
    ('ch', 'ㄔ'),
    ('sh', 'ㄕ'),
    ('zh', 'ㄓ'),
    ('b', 'ㄅ'),
    ('c', 'ㄘ'),
    ('d', 'ㄉ'),
    ('f', 'ㄈ'),
    ('g', 'ㄍ'),
    ('h', 'ㄏ'),
    ('j', 'ㄐ'),
    ('k', 'ㄎ'),
    ('l', 'ㄌ'),
    ('m', 'ㄇ'),
    ('n', 'ㄋ'),
    ('p', 'ㄆ'),
    ('q', 'ㄑ'),
    ('r', 'ㄖ'),
    ('s', 'ㄙ'),
    ('t', 'ㄊ'),
    ('x', 'ㄒ'),
    ('z', 'ㄗ'),
]

bopomofo_finals = [
    ('iang', 'ㄧㄤ'),
    ('iong', 'ㄩㄥ'),
    ('uang', 'ㄨㄤ'),
    ('u:an', 'ㄩㄢ'),
    ('ang', 'ㄤ'),
    ('eng', 'ㄥ'),
    ('iai', 'ㄧㄞ'),
    ('ian', 'ㄧㄢ'),
    ('iao', 'ㄧㄠ'),
    ('ing', 'ㄧㄥ'),
    ('ong', 'ㄨㄥ'),
    ('uai', 'ㄨㄞ'),
    ('uan', 'ㄨㄢ'),
    ('u:e', 'ㄩㄝ'),
    ('u:n', 'ㄩㄣ'),
    ('ai', 'ㄞ'),
    ('an', 'ㄢ'),
    ('ao', 'ㄠ'),
    ('ei', 'ㄟ'),
    ('en', 'ㄣ'),
    ('er', 'ㄦ'),
    ('ia', 'ㄧㄚ'),
    ('ie', 'ㄧㄝ'),
    ('in', 'ㄧㄣ'),
    ('io', 'ㄧㄛ'),
    ('iu', 'ㄧㄡ'),
    ('ou', 'ㄡ'),
    ('ua', 'ㄨㄚ'),
    ('ui', 'ㄨㄟ'),
    ('un', 'ㄨㄣ'),
    ('uo', 'ㄨㄛ'),
    ('u:', 'ㄩ'),
    ('a', 'ㄚ'),
    ('e', 'ㄜ'),
    ('i', 'ㄧ'),
    ('o', 'ㄛ'),
    ('u', 'ㄨ'),
    ('ê', 'ㄝ'),
]

bopomofo_tones = [('1', ''), ('2', 'ˊ'), ('3', 'ˇ'), ('4', 'ˋ'), ('5', '˙')]

table = bopomofo_special + bopomofo_initials + bopomofo_finals + bopomofo_tones
table.sort(key=lambda pair: len(pair[0]), reverse=True)
bopomofo_replacements.extend(table)

CHINESE_PUNC_TO_LATIN = {'。': '.', '，': ','}

DIACRITIC_NAME_TO_NUM = {
    'COMBINING MACRON': '1',
    'COMBINING ACUTE ACCENT': '2',
    'COMBINING CARON': '3',
    'COMBINING GRAVE ACCENT': '4',
}

CLOZE_REGEX = r'\{\{c[0-9]+::(.*?)(::.*?)?\}\}'
SOUND_TAG_REGEX = r'\[sound:.*?\]'
