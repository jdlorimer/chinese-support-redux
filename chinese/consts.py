# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017-2018 Joseph Lorimer <luoliyan@posteo.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

base_letters = {
'ā':'a', 'ē':'e', 'ī':'i', 'ō':'o', 'ū':'u', 'ǖ':'ü',
'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ǘ':'ü',
'ǎ':'a', 'ě':'e', 'ǐ':'i', 'ǒ':'o', 'ǔ':'u', 'ǚ':'ü',
'à':'a', 'è':'e', 'ì':'i', 'ò':'o', 'ù':'u', 'ǜ':'ü',
'a':'a', 'e':'e', 'i':'i', 'o':'o', 'u':'u', 'ü':'ü', 'v':'v'
}

vowel_decorations = [
{ },
{ 'a':'ā', 'e':'ē', 'i':'ī', 'o':'ō', 'u':'ū', 'ü':'ǖ', 'v':'ǖ'},
{ 'a':'á', 'e':'é', 'i':'í', 'o':'ó', 'u':'ú', 'ü':'ǘ', 'v':'ǘ'},
{ 'a':'ǎ', 'e':'ě', 'i':'ǐ', 'o':'ǒ', 'u':'ǔ', 'ü':'ǚ', 'v':'ǚ'},
{ 'a':'à', 'e':'è', 'i':'ì', 'o':'ò', 'u':'ù', 'ü':'ǜ', 'v':'ǜ'},
{ 'a':'a', 'e':'e', 'i':'i', 'o':'o', 'u':'u', 'ü':'ü', 'v':'ü'},
]

accents = 'ɑ̄āĀáɑ́ǎɑ̌ÁǍàɑ̀ÀēĒéÉěĚèÈīĪíÍǐǏìÌōŌóÓǒǑòÒūŪúÚǔǓùÙǖǕǘǗǚǙǜǛ'

vowel_tone_dict = {
    'ā':1, 'ā':1, 'ɑ̄':1, 'ē':1, 'ī':1, 'ō':1, 'ū':1,
    'ǖ':1, 'Ā':1, 'Ē':1, 'Ī':1, 'Ō':1, 'Ū':1, 'Ǖ':1,
    'á':2, 'ɑ́':2, 'é':2, 'í':2, 'ó':2, 'ú':2, 'ǘ':2,
    'Á':2, 'É':2, 'Í':2, 'Ó':2, 'Ú':2, 'Ǘ':2,
    'ǎ':3, 'ɑ̌':3, 'ě':3, 'ǐ':3, 'ǒ':3, 'ǔ':3, 'ǚ':3,
    'Ǎ':3, 'Ě':3, 'Ǐ':3, 'Ǒ':3, 'Ǔ':3, 'Ǚ':3,
    'à':4, 'ɑ̀':4, 'è':4, 'ì':4, 'ò':4, 'ù':4, 'ǜ':4,
    'À':4, 'È':4, 'Ì':4, 'Ò':4, 'Ù':4, 'Ǜ':4
    }

pinyin_inits = "zh|sh|ch|[bpmfdtnlgkhjqxrzscwy]"
pinyin_finals = "i[ōóǒòo]ng|[ūúǔùu]ng|[āáǎàa]ng|[ēéěèe]ng|i[āɑ̄áɑ́ɑ́ǎɑ̌àɑ̀aāáǎàa]ng|[īíǐìi]ng|i[āáǎàa]n|u[āáǎàa]n|[ōóǒòo]ng|[ēéěèe]r|i[āáǎàa]|i[ēéěèe]|i[āáǎàa]o|i[ūúǔùu]|[īíǐìi]n|u[āáǎàa]|u[ōóǒòo]|u[āáǎàa]i|u[īíǐìi]|[ūúǔùu]n|u[ēéěèe]|ü[ēéěèe]|v[ēéěèe]|i[ōóǒòo]|[āáǎàa]i|[ēéěèe]i|[āáǎàa]o|[ōóǒòo]u|[āáǎàa]n|[ēéěèe]n|[āáǎàa]|[ēéěèe]|[ōóǒòo]|[īíǐìi]|[ūúǔùu]|[ǖǘǚǜüv]"
pinyin_standalones = "'[āáǎàa]ng|'[ēéěèe]ng|'[ēéěèe]r|'[āáǎàa]i|'[ēéěèe]i|'[āáǎàa]o|'[ōóǒòo]u|'[āáǎàa]n|'[ēéěèe]n|'[āáǎàa]|'[ēéěèe]|'[ōóǒòo]"
jyutping_inits = "ng|gw|kw|[bpmfdtnlgkhwzcsj]"
jyutping_finals = "i|ip|it|ik|im|in|ing|iu|yu|yut|yun|u|up|ut|uk|um|un|ung|ui|e|ep|et|ek|em|en|eng|ei|eu|eot|eon|eoi|oe|oet|oek|oeng|oei|o|ot|ok|om|on|ong|oi|ou|ap|at|ak|am|an|ang|ai|au|aa|aap|aat|aak|aam|aan|aang|aai|aau|m|ng"
jyutping_standalones = "'uk|'ung|'e|'ei|'oe|'o|'ok|'om|'on|'ong|'oi|'ou|'ap|'at|'ak|'am|'an|'ang|'ai|'au|'aa|'aap|'aat|'aak|'aam|'aan|'aang|'aai|'aau|'m|'ng"

# early replacements
bopomofo_replacements = [
    ('jue', 'ㄐㄩㄝ'),
    ('lue', 'ㄌㄩㄝ'),
    ('nue', 'ㄋㄩㄝ'),
    ('que', 'ㄑㄩㄝ'),
    ('v', 'u:'),
    ('w', 'u'),
    ('wong', 'ㄨㄥ'),
    ('wu', 'u'),
    ('xue', 'ㄒㄩㄝ'),
    ('yi', 'i'),
    ('y', 'i'),
    ('you', 'ㄧㄡ'),
    ('yu', 'u:'),
    ('yue', 'ㄩㄝ'),
    ('ü', 'u:'),
]

bopomofo_special = [
    ('chi', 'ㄔ'),
    ('ci', 'ㄘ'),
    ('ju', 'ㄐㄩ'),
    ('qu', 'ㄑㄩ'),
    ('r5', 'ㄦ'),
    ('ri', 'ㄖ'),
    ('shi', 'ㄕ'),
    ('si', 'ㄙ'),
    ('xu', 'ㄒㄩ'),
    ('zhi', 'ㄓ'),
    ('zi', 'ㄗ'),
]

bopomofo_initials = [
    ('b', 'ㄅ'),
    ('c', 'ㄘ'),
    ('ch', 'ㄔ'),
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
    ('sh', 'ㄕ'),
    ('t', 'ㄊ'),
    ('x', 'ㄒ'),
    ('z', 'ㄗ'),
    ('zh', 'ㄓ'),
]

bopomofo_finals = [
    ('a', 'ㄚ'),
    ('ai', 'ㄞ'),
    ('an', 'ㄢ'),
    ('ang', 'ㄤ'),
    ('ao', 'ㄠ'),
    ('e', 'ㄜ'),
    ('ei', 'ㄟ'),
    ('en', 'ㄣ'),
    ('eng', 'ㄥ'),
    ('er', 'ㄦ'),
    ('i', 'ㄧ'),
    ('ia', 'ㄧㄚ'),
    ('iai', 'ㄧㄞ'),
    ('ian', 'ㄧㄢ'),
    ('iang', 'ㄧㄤ'),
    ('iao', 'ㄧㄠ'),
    ('ie', 'ㄧㄝ'),
    ('in', 'ㄧㄣ'),
    ('ing', 'ㄧㄥ'),
    ('io', 'ㄧㄛ'),
    ('iong', 'ㄩㄥ'),
    ('iu', 'ㄧㄡ'),
    ('o', 'ㄛ'),
    ('ong', 'ㄨㄥ'),
    ('ou', 'ㄡ'),
    ('u', 'ㄨ'),
    ('u:', 'ㄩ'),
    ('u:an', 'ㄩㄢ'),
    ('u:e', 'ㄩㄝ'),
    ('u:n', 'ㄩㄣ'),
    ('ua', 'ㄨㄚ'),
    ('uai', 'ㄨㄞ'),
    ('uan', 'ㄨㄢ'),
    ('uang', 'ㄨㄤ'),
    ('ui', 'ㄨㄟ'),
    ('un', 'ㄨㄣ'),
    ('uo', 'ㄨㄛ'),
    ('ê', 'ㄝ'),
]

bopomofo_notes = {'ˊ': '2', 'ˇ': '3', 'ˋ': '4', '˙': '5'}

bopomofo_tones = [
    ('1', ''),
    ('2', 'ˊ'),
    ('3', 'ˇ'),
    ('4', 'ˋ'),
    ('5', '˙')
]

table = bopomofo_special + bopomofo_initials + bopomofo_finals + bopomofo_tones
table.sort(key=lambda pair: len(pair[0]), reverse=True)
bopomofo_replacements.extend(table)
